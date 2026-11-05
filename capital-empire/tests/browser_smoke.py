import json, os, traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent
def bundled_html(saved=None):
    html=(ROOT/'dev.html').read_text()
    css=(ROOT/'styles.css').read_text()
    source=[]
    import re
    for name in ['data.mjs','engine.mjs','office.mjs','app.mjs']:
        js=(ROOT/name).read_text()
        js=re.sub(r'^import .*?;\s*$', '',js,flags=re.MULTILINE)
        js=re.sub(r'^export ', '',js,flags=re.MULTILINE)
        source.append(js)
    shim='''<script>const __store=new Map(Object.entries(INIT_DATA));Object.defineProperty(window,'localStorage',{value:{getItem:k=>__store.has(k)?__store.get(k):null,setItem:(k,v)=>__store.set(k,String(v)),removeItem:k=>__store.delete(k),clear:()=>__store.clear()}, configurable:true});</script>'''.replace('INIT_DATA',json.dumps({'capital-empire-v3':json.dumps(saved)} if saved else {}))
    html=html.replace('<link rel="stylesheet" href="styles.css">','<style>'+css+'</style>')
    html=html.replace('<script type="module" src="app.mjs"></script>',shim+'<script>\n'+'\n'.join(source)+'\n</script>')
    return html
SHOT=ROOT/'tests'/'screenshots';SHOT.mkdir(exist_ok=True)
errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--use-gl=swiftshader'])
 context=browser.new_context(viewport={'width':1440,'height':900},device_scale_factor=1)
 page=context.new_page()
 page.on('pageerror',lambda ex:errors.append(str(ex)))
 page.on('console',lambda msg:errors.append('console error: '+msg.text) if msg.type=='error' else None)
 page.set_content(bundled_html(),wait_until='load')
 page.screenshot(path=str(SHOT/'desktop-welcome.png'),full_page=True)
 print('TITLE',page.title())
 print('WELCOME',page.locator('#welcomeForm').count())
 page.locator('#companyInput').fill('Matu Capital');page.locator('#welcomeForm button').click()
 page.wait_for_timeout(1200)
 page.screenshot(path=str(SHOT/'desktop-overview.png'),full_page=True)
 assert page.locator('#officeCanvas').count()==1
 assert page.get_by_text('Dein Weg an die Spitze').count()==1
 frames=page.evaluate('''async () => await new Promise(resolve => {let n=0,start=performance.now();function f(){n++;if(performance.now()-start>1100)resolve(Math.round(n*1000/(performance.now()-start)));else requestAnimationFrame(f)}requestAnimationFrame(f)})''')
 print('HEADLESS FPS',frames)
 assert frames>=15
 page.locator('[data-action="navigate"][data-id="market"]').first.click()
 page.wait_for_timeout(200)
 page.screenshot(path=str(SHOT/'desktop-stock.png'),full_page=True)
 state=lambda:page.evaluate("JSON.parse(localStorage.getItem('capital-empire-v3'))")
 before=state()
 page.locator('#sharesInput').fill('5')
 page.locator('[data-action="buyStock"]').click()
 after=state();print('STOCK BUY',before['cash'],after['cash'],after['stock']['NRVA']['shares'])
 assert after['stock']['NRVA']['shares']==5
 page.locator('#sharesInput').fill('2');page.locator('[data-action="sellStock"]').click()
 assert state()['stock']['NRVA']['shares']==3
 page.locator('[data-action="navigate"][data-id="private"]').first.click()
 page.wait_for_timeout(100)
 page.screenshot(path=str(SHOT/'desktop-private.png'),full_page=True)
 page.locator('[data-action="openDeal"][data-id="pd1"]').first.click()
 page.locator('[data-action="dd"][data-id="pd1"]').click()
 assert state()['dueDiligence']==['pd1']
 page.locator('[data-action="invest"][data-id="pd1"]').click()
 assert state()['deals'][0]['id']=='pd1'
 page.locator('[data-action="close"]').first.click()
 page.locator('[data-action="navigate"][data-id="company"]').first.click()
 page.screenshot(path=str(SHOT/'desktop-company.png'),full_page=True)
 page.locator('[data-action="hire"][data-id="manager"]').click()
 assert 'manager' in state()['staff']
 # reputation gained 8 + 3 +9 +7=37
 print('REP',state()['reputation'],'CASH',state()['cash'])
 page.locator('[data-action="upgrade"]').click()
 assert state()['office']==1
 page.locator('[data-action="navigate"][data-id="funds"]').first.click()
 page.screenshot(path=str(SHOT/'desktop-funds-before.png'),full_page=True)
 page.locator('#fundName').fill('Matu Private Credit Fund I')
 page.locator('#fundClass').select_option('Private Debt')
 page.locator('#fundForm button').click()
 assert len(state()['funds'])==1
 print('FUND',state()['funds'][0]['commitment'],state()['cash'])
 fund_id=state()['funds'][0]['id']
 page.locator('[data-action="call"]').first.click()
 assert state()['funds'][0]['assets']>0
 page.screenshot(path=str(SHOT/'desktop-funds-active.png'),full_page=True)
 page.locator('[data-action="navigate"][data-id="overview"]').first.click()
 page.locator('.speed[data-speed="0"]').click()
 page.locator('#nextMonth').click()
 old_month=state()['month']
 # The real browser export/import UI must preserve the exact saved month and balances.
 page.locator('#settingsBtn').click()
 with page.expect_download() as downloaded:
  page.locator('[data-action="export"]').click()
 savefile=SHOT/'reimport.json';downloaded.value.save_as(str(savefile))
 page.locator('[data-action="close"]').first.click()
 page.locator('#nextMonth').click()
 assert state()['month']==old_month+1
 page.locator('#settingsBtn').click()
 page.locator('#importFile').set_input_files(str(savefile))
 page.wait_for_function('(m) => JSON.parse(localStorage.getItem("capital-empire-v3")).month===m',arg=old_month,timeout=5000)
 assert state()['month']==old_month
 page.locator('[data-action="navigate"][data-id="overview"]').first.click()
 saved=state()
 reload_page=context.new_page();reload_page.on('pageerror',lambda ex:errors.append('reload '+str(ex)))
 reload_page.set_content(bundled_html(saved),wait_until='load')
 assert reload_page.evaluate("JSON.parse(localStorage.getItem('capital-empire-v3')).month")==old_month
 assert reload_page.locator('#companyBrand').inner_text()=='MATU CAPITAL'
 print('SAVE RELOAD OK',old_month)
 # Mobile new context, same game state via localStorage injection.
 mob=browser.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)
 mobile=mob.new_page();mobile.on('pageerror',lambda ex:errors.append('mobile '+str(ex)))
 mobile.set_content(bundled_html(),wait_until='load')
 mobile.locator('#welcomeForm button').click()
 mobile.wait_for_timeout(700)
 mobile.screenshot(path=str(SHOT/'mobile-overview.png'),full_page=True)
 overflow=mobile.evaluate('({scroll:document.documentElement.scrollWidth,view:window.innerWidth})')
 print('MOBILE OVERFLOW',overflow)
 assert overflow['scroll']<=overflow['view']+2
 mobile.locator('.mobile-nav [data-id="market"]').click()
 mobile.wait_for_timeout(200)
 mobile.screenshot(path=str(SHOT/'mobile-stock.png'),full_page=True)
 mobile.locator('.mobile-nav [data-id="private"]').click()
 mobile.screenshot(path=str(SHOT/'mobile-private.png'),full_page=True)
 mobile.locator('.mobile-nav [data-id="company"]').click()
 mobile.screenshot(path=str(SHOT/'mobile-company.png'),full_page=True)
 for width in [320,360,480,768]:
  mobile.set_viewport_size({'width':width,'height':844})
  mobile.wait_for_timeout(60)
  bound=mobile.evaluate('({scroll:document.documentElement.scrollWidth,view:window.innerWidth})')
  print('MOBILE WIDTH',width,bound)
  assert bound['scroll']<=bound['view']+2,bound
 print('BROWSER ERRORS',errors)
 assert not errors,errors
 mob.close();context.close();browser.close()
 print('PASS desktop and mobile UI scenario')