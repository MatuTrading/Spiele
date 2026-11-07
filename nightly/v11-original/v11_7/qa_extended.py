#!/usr/bin/env python3
"""Interactive save/reload, image asset audit, event interruption, import/export of original-based V11.7."""
from playwright.sync_api import sync_playwright
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import threading, json, time, tempfile
from urllib.parse import quote
import os
root=Path(__file__).resolve().parent.parent
site=root/'PrivateMarketsTycoon_V11_7_Nightly_Offline.html'
shots=Path(__file__).resolve().parent/'screenshots';shots.mkdir(exist_ok=True)
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(root)))
thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
url=f'http://127.0.0.1:{server.server_address[1]}/{quote(site.name)}'
results={}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.environ.get('ODIN_CHROMIUM') or None,args=['--no-sandbox'])
 ctx=browser.new_context(viewport={'width':390,'height':844},has_touch=True,is_mobile=True,accept_downloads=True)
 page=ctx.new_page();errors=[];failed_requests=[]
 page.on('pageerror',lambda e: errors.append(str(e)))
 page.on('requestfailed',lambda req: failed_requests.append(req.url))
 try:
  page.goto(url,wait_until='domcontentloaded',timeout=90000)
  origin_loaded=True
 except Exception:
  page.set_content(site.read_text('utf-8'),wait_until='domcontentloaded',timeout=90000)
  origin_loaded=False
 page.locator('[data-do="start-fund"]').click()
 if page.locator('#overlay.visible [data-do="close-modal"]').count():page.locator('#overlay.visible [data-do="close-modal"]').click()
 page.locator('[data-do="talk"]').click()
 assert page.locator('#overlay.visible [data-do="answer"]').count()>0,'No investor response choices'
 page.screenshot(path=str(shots/'investor_dialog.png'))
 page.locator('#overlay.visible [data-do="answer"]').first.click()
 assert not errors,errors
 results['investor_dialog']='PASS'
 # Echte Origin-Navigation ist in dieser Umgebung administrativ blockiert.
 # Export/Import testet stattdessen den praktischen Sicherungspfad.
 page.locator('[data-do="odin-advance"][data-months="1"]').click()
 current=page.evaluate('''()=>({month:state.month, cash:state.gpCash,sequence:state.sequence})''')
 if origin_loaded:
  page.reload(wait_until='domcontentloaded')
  actual=page.evaluate('''()=>({month:state.month,cash:state.gpCash,sequence:state.sequence})''')
  assert actual==current, (actual,current)
  results['real_url_reload']='PASS'
 else:
  results['real_url_reload']='BLOCKED (browser denies localhost and synthetic HTTPS origins)'
 page.locator('[data-do="settings"]').click()
 with page.expect_download() as d:
  page.locator('#overlay.visible [data-do="export"]').click()
 download=d.value
 path=shots/'export.json'; download.save_as(str(path))
 data=json.loads(path.read_text('utf-8'))
 assert data['month']==current['month']
 page.locator('#overlay.visible [data-do="import"]').click()
 page.locator('#savefile').set_input_files(str(path))
 assert page.evaluate('state.month')==current['month']
 results['export_import']='PASS'
 # World plots are directly usable with touch; selecting one does not make changes to economics.
 page.locator('[data-tab="play"]').last.click()
 before=page.evaluate('state.month')
 page.locator('.world-plot[role="button"]').first.click()
 assert page.evaluate('state.month')==before
 assert page.locator('[data-do="focus-deal"].chosen').count()==1
 results['interactive_world']='PASS'
 # Full image table encoded in offline build: all inline images decode.
 image_audit=page.evaluate('''async ()=>{
 const keys=Object.keys(STORY_ART);const broken=[];let small=0;
 for(const key of keys){
   const u=STORY_ART[key];
   if(!u.startsWith('data:image/')){broken.push(key+':not_inline');continue;}
   const loaded=await new Promise(resolve=>{const im=new Image();im.onload=()=>resolve([im.naturalWidth,im.naturalHeight]);im.onerror=()=>resolve(null);im.src=u;});
   if(!loaded)broken.push(key);else if(loaded[0]<96||loaded[1]<96)small++;
 }
 return {count:keys.length,broken,small};}''')
 assert image_audit['count']>20 and not image_audit['broken'],image_audit
 results['all_illustration_assets']=image_audit
 # Induce an important economy event, fast-forward must pause after first month, showing the event.
 page.evaluate('''()=>{
  const f=state.funds[0];f.age=17;f.fundraise=true;f.commitmentTotal=0;
  state.gpCash=800000;state.loss=false;state.win=false;render();save();}''')
 pre=page.evaluate('state.month')
 page.locator('[data-do="odin-advance"][data-months="12"]').click()
 actual=page.evaluate('''()=>({month:state.month,done:odinV117TimeReport.done,paused:odinV117TimeReport.paused,important:state.events.some(e=>e.month===state.month&&e.important),modal:currentModal})''')
 assert actual['month']==pre+1 and actual['done']==1 and actual['paused'] and actual['important'] and actual['modal']=='important',actual
 page.screenshot(path=str(shots/'critical_event_390.png'),full_page=True)
 results['early_pause_on_critical_event']='PASS'
 assert not errors and not failed_requests,(errors,failed_requests)
 results['js_errors']=0;results['failed_network_requests']=0
 ctx.close();browser.close()
server.shutdown();server.server_close()
(shots/'extended_report.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf-8')
print('EXTENDED',json.dumps(results,ensure_ascii=False))