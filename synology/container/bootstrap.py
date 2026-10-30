"""DSM packaging adapter: upstream files unchanged; native HA onboarding/HTTP APIs only."""
import asyncio, base64, hashlib, io, json, os, pathlib, signal, subprocess, sys, time, zipfile
cfg = pathlib.Path('/var/tmp/home-assistant/config')
if os.getuid() == 0 or os.environ.get('HA_BIND') != '127.0.0.1':
    raise SystemExit('Home Assistant requires package UID and SDK loopback listener')
oidc_port=os.environ.get('OIDC_PORT','')
if not oidc_port.isdigit() or str(int(oidc_port))!=oidc_port or not 1024<=int(oidc_port)<=65535:
    raise SystemExit('Invalid OIDC issuer port')
discovery_url=f'http://127.0.0.1:{oidc_port}/.well-known/openid-configuration'
# The native HTTP trial reverts after five minutes; fail before that boundary.
deadline = time.monotonic() + min(240, int(os.environ['SYNOPKGLAND_STARTUP_BUDGET_SECONDS']))
component = cfg / 'custom_components' / 'auth_oidc'
if not (component / '.component-release').exists():
    data = base64.b64decode(COMPONENT_ARCHIVE_BASE64)
    if hashlib.sha256(data).hexdigest() != 'e5badaaacaa63cfd6fe733924a05e76d75058836190398598fb24de57cd47ccd':
        raise SystemExit('Component checksum mismatch')
    component.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        for item in archive.infolist():
            rel=pathlib.PurePosixPath(item.filename)
            if rel.is_absolute() or '..' in rel.parts or item.file_size>1024*1024: raise SystemExit('Unsafe archive')
            dest=component.joinpath(*rel.parts)
            if item.is_dir():dest.mkdir(parents=True,exist_ok=True)
            else:
                dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(archive.read(item))
    (component/'.component-release').write_text('v1.2.1\n')
marker=cfg/'package-bootstrap.complete'
http_store=cfg/'.storage/http'
def assert_private_http(final=False):
    if not http_store.exists():return
    d=json.loads(http_store.read_text())['data']
    active=d.get('pending') if d.get('pending') and not d['pending'].get('error') else d.get('stable')
    if not active or active.get('server_host')!=['127.0.0.1'] or active.get('server_port') not in ([8123] if final else [8123,8124]) or active.get('use_x_forwarded_for') is not True or active.get('trusted_proxies')!=['127.0.0.1/32']:
        raise RuntimeError('Stored HTTP policy is incompatible')
assert_private_http(final=marker.exists())
def remove_http_yaml(path):
    doc=json.loads(path.read_text())
    doc.pop('http',None)
    path.write_text(json.dumps(doc,indent=2)+'\n')
def sync_discovery_url(path):
    # A reinstall that keeps data may select another issuer port.
    doc=json.loads(path.read_text())
    oidc=doc.get('auth_oidc')
    if oidc and oidc.get('discovery_url')!=discovery_url:
        oidc['discovery_url']=discovery_url
        path.write_text(json.dumps(doc,indent=2)+'\n')
async def configure_core_defaults(ws_call):
    try:
        detected=await ws_call(8124,'config/core/detect')
    except TimeoutError:
        detected={'success':False}
    settings={key:value for key,value in (detected.get('result') or {}).items()
              if key in ('country','time_zone','unit_system','currency','latitude','longitude')}
    if not detected['success'] or not settings.get('country'):
        print('Home Assistant: location detection unavailable; set country, time zone and units in Settings > System > General',flush=True)
    elif not (await ws_call(8124,'config/core/update',**settings))['success']:
        raise RuntimeError('Core configuration failed')
if marker.exists():
    conf=cfg/'configuration.yaml'
    sync_discovery_url(conf)
    print('Home Assistant: retained native configuration ready',flush=True)
    os.execvp('python3',['python3','-m','homeassistant','--config',str(cfg)])
conf=cfg/'configuration.yaml'
if not conf.exists():
    for key in ['OIDC_SECRET','BOOTSTRAP_PASSWORD']:
        if len(os.environ.get(key,''))!=64 or any(c not in '0123456789abcdef' for c in os.environ[key]):raise SystemExit('Invalid runtime secret')
    doc={'zeroconf':None,'frontend':None,'config':None,'history':None,'logbook':None,'person':None,'sun':None,'mobile_app':None,'analytics':None,'my':None,'lovelace':{'mode':'storage'},'automation':[], 'script':{},'scene':[],
         'http':{'server_host':['127.0.0.1'],'server_port':8124,'use_x_forwarded_for':True,'trusted_proxies':['127.0.0.1']},
         'auth_oidc':{'client_id':'homeassistant','client_secret':os.environ['OIDC_SECRET'],
                      'discovery_url':discovery_url,'display_name':'DSM',
                      'roles':{'admin':'admins','user':'users'},'features':{'default_redirect':True,'force_https':True,'automatic_user_linking':False}}}
    conf.write_text(json.dumps(doc,indent=2)+'\n');conf.chmod(0o600)
child=None;phase='start'
def launch():
    global child
    child=subprocess.Popen(['python3','-m','homeassistant','--config',str(cfg)],start_new_session=True)
def stop_child(*_):
    if child and child.poll() is None:
        os.killpg(child.pid,signal.SIGTERM)
        try:child.wait(timeout=55)
        except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
for sig in [signal.SIGTERM,signal.SIGINT]:
    signal.signal(sig,lambda *_:(stop_child(),sys.exit(0)))
async def main():
    global phase
    import aiohttp
    def remaining():
        if time.monotonic()>=deadline:raise RuntimeError('bootstrap deadline')
        return max(1,min(10,deadline-time.monotonic()))
    async with aiohttp.ClientSession() as session:
        async def api(port,path,body=None,token=None,form=None):
            headers={'Authorization':'Bearer '+token} if token else {}
            async with session.request('GET' if body is None and form is None else 'POST',f'http://127.0.0.1:{port}'+path,
                json=body,data=form,headers=headers,timeout=aiohttp.ClientTimeout(total=remaining())) as r:
                if r.status!=200:raise RuntimeError('native api refused')
                return await r.json()
        async def ready(port):
            while True:
                remaining()
                if child.poll() is not None:raise RuntimeError('child exited')
                try:return await api(port,'/api/onboarding')
                except (aiohttp.ClientError,asyncio.TimeoutError):await asyncio.sleep(.25)
        tokenfile=cfg/'package-bootstrap-token.json'
        launch();steps=await ready(8124)
        phase='onboarding'
        client='http://127.0.0.1:8124/'
        if not any(x['step']=='user' and x['done'] for x in steps):
            result=await api(8124,'/api/onboarding/users',body={'name':'Package bootstrap','username':'package_bootstrap',
                'password':os.environ['BOOTSTRAP_PASSWORD'],'client_id':client,'language':'en'})
            tokens=await api(8124,'/auth/token',form={'grant_type':'authorization_code','code':result['auth_code'],'client_id':client})
            tokenfile.write_text(json.dumps({'refresh_token':tokens['refresh_token']}));tokenfile.chmod(0o600)
        else:
            tokens=await api(8124,'/auth/token',form={'grant_type':'refresh_token','refresh_token':json.loads(tokenfile.read_text())['refresh_token'],'client_id':client})
        token=tokens['access_token']
        async def ws_call(port,typ,**args):
            async with session.ws_connect(f'http://127.0.0.1:{port}/api/websocket',timeout=remaining()) as ws:
                await ws.receive_json(timeout=remaining());await ws.send_json({'type':'auth','access_token':token})
                if (await ws.receive_json(timeout=remaining()))['type']!='auth_ok':raise RuntimeError('native auth failed')
                await ws.send_json({'id':1,'type':typ,**args})
                while True:
                    r=await ws.receive_json(timeout=remaining())
                    if r.get('id')==1:return r
        if not any(x['step']=='core_config' and x['done'] for x in steps):
            phase='detect-core-settings'
            await configure_core_defaults(ws_call)
        for step in ['core_config','analytics','integration']:
            if any(x['step']==step and x['done'] for x in steps):continue
            await api(8124,'/api/onboarding/'+step,body={'client_id':client,'redirect_uri':client} if step=='integration' else {},token=token)
        phase='confirm-private-bootstrap-http'
        if not (await ws_call(8124,'http/config/promote'))['success']:raise RuntimeError('HTTP promote failed')
        phase='configure-final-http'
        while True:
            r=await ws_call(8124,'http/config/configure',config={'server_host':['127.0.0.1'],'server_port':8123,
                'use_x_forwarded_for':True,'trusted_proxies':['127.0.0.1']})
            if r['success']:break
            if r.get('error',{}).get('code')!='not_running':raise RuntimeError('native configure failed')
            await asyncio.sleep(.25)
        phase='native-restart'
        while child.poll() is None:remaining();await asyncio.sleep(.1)
        # The promoted native store owns HTTP settings after the first boot.
        assert_private_http();remove_http_yaml(conf);launch()
        # Refresh tokens survive a native HA restart; never expose them in logs/argv.
        while True:
            remaining()
            try:
                tokens=await api(8123,'/auth/token',form={'grant_type':'refresh_token','refresh_token':json.loads(tokenfile.read_text())['refresh_token'],'client_id':client})
                token=tokens['access_token'];break
            except (aiohttp.ClientError,asyncio.TimeoutError):await asyncio.sleep(.25)
        phase='promote-final-http'
        if not (await ws_call(8123,'http/config/promote'))['success']:raise RuntimeError('final promote failed')
        assert_private_http(final=True)
        marker.write_text('native-onboarding-http-confirmed\n')
        tokenfile.unlink()
        print('Home Assistant: native onboarding complete, loopback HTTP confirmed',flush=True)
try:
    asyncio.run(main())
    # Keep the final, promoted HA child serving. Restarting it here would create
    # a listener gap after the SDK has already admitted its healthy endpoint.
    sys.exit(child.wait())
except Exception:
    stop_child()
    print('Home Assistant bootstrap failed at '+phase,flush=True)
    sys.exit(1)
