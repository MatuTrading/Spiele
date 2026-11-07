#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
from pathlib import Path
import json, traceback, time
import os
root=Path(__file__).resolve().parent.parent
html=(root/'PrivateMarketsTycoon_V11_7_Nightly_Offline.html').read_text('utf-8')
out=Path(__file__).resolve().parent/'screenshots';out.mkdir(exist_ok=True)
results=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=os.environ.get('ODIN_CHROMIUM') or None,args=['--no-sandbox'])
    for w,h in [(360,800),(390,844),(768,1024),(1440,900)]:
        t=time.time(); errors=[]
        ctx=browser.new_context(viewport={'width':w,'height':h},is_mobile=w<500,has_touch=w<500,device_scale_factor=1,accept_downloads=True)
        page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        try:
            page.set_content(html,wait_until='domcontentloaded',timeout=90000)
            page.locator('.odin-matu-header img').wait_for(timeout=20000)
            assert page.locator('.odin-matu-header img').evaluate('(x)=>x.complete && x.naturalWidth>0'), 'logo broken'
            assert page.locator('link[rel=icon]').count()>=1
            assert page.locator('.kpis > div').count()==2, 'HUD not condensed'
            assert not page.locator('.status-details').evaluate('(x)=>x.open'), 'status should be collapsed'
            page.screenshot(path=str(out/f'start_{w}.png'),full_page=True)
            page.locator('[data-do="start-fund"]').click()
            if page.locator('#overlay.visible [data-do="close-modal"]').count():page.locator('#overlay.visible [data-do="close-modal"]').click()
            assert page.locator('.odin-time-buttons button').count()==3
            assert page.locator('button.month-inline').count()==0,'duplicate month button'
            assert page.locator('[data-do="talk"]').count()==1
            assert page.locator('.odin-timebar').count()==1
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),f'overflow {w}'
            if w<500:
                bb=page.locator('.odin-timebar').bounding_box()
                assert bb['y']+bb['height']<h-70, 'time bar below fold'
                buttons=page.locator('.odin-time-buttons button').all()
                assert all(b.bounding_box()['height']>=48 for b in buttons), 'small time controls'
            page.screenshot(path=str(out/f'playing_{w}.png'),full_page=True)
            # Independent step-by-step simulation reference. Verify time skips don't jump over intermediate accounting.
            for n in [1,3,12]:
                if page.locator('#overlay.visible [data-do="close-modal"]').count():page.locator('#overlay.visible [data-do="close-modal"]').click()
                if page.evaluate('state.win || state.loss'):break
                expected=page.evaluate('''n=>{
                    const s=structuredClone(state);
                    const origMonth=s.month,origCash=s.gpCash;let steps=0;
                    for(let i=0;i<n;i++){
                        const oldSequence=s.sequence;
                        const beforeReady=s.funds.some(f=>distributeMax(f)>=100);
                        const beforeFundsReady=s.funds.length<8&&!s.funds.some(f=>f.fundraise&&!f.finalClose)&&s.month-s.funds.at(-1).launchMonth>=12;
                        nextMonth(s);steps++;
                        const urgent=s.events.find(e=>e.id>oldSequence&&e.important);
                        const afterReady=!beforeReady&&s.funds.some(f=>distributeMax(f)>=100);
                        const afterFundsReady=!beforeFundsReady&&s.funds.length<8&&!s.funds.some(f=>f.fundraise&&!f.finalClose)&&s.month-s.funds.at(-1).launchMonth>=12;
                        if(urgent||s.win||s.loss||afterReady||afterFundsReady)break;
                    }
                    return {month:s.month,cash:s.gpCash,sequence:s.sequence,history:s.history.length,steps,funds:s.funds.map(f=>({age:f.age,cash:f.cash,feeDue:f.feeDue,dist:f.distributions})),events:s.events.length};
                }''',n)
                page.locator(f'[data-do="odin-advance"][data-months="{n}"]').click()
                actual=page.evaluate('''()=>({month:state.month,cash:state.gpCash,sequence:state.sequence,history:state.history.length,steps:odinV117TimeReport?.done, funds:state.funds.map(f=>({age:f.age,cash:f.cash,feeDue:f.feeDue,dist:f.distributions})),events:state.events.length})''')
                assert actual==expected,(w,n,'time-state mismatch',actual,expected)
                assert page.locator('.odin-time-summary').count()==(0 if actual['month']<1 or page.evaluate('state.win || state.loss') else 1)
                if n==3:page.screenshot(path=str(out/f'time_{w}.png'),full_page=True)
                if page.locator('#overlay.visible [data-do="close-modal"]').count():page.locator('#overlay.visible [data-do="close-modal"]').click()
            # Other tabs, branding in settings; verify no horizontal overflows after navigation.
            for tab in ['funds','team','news','play']:
                page.locator(f'[data-tab="{tab}"]').last.click()
                assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),f'overflow {w} {tab}'
                if tab=='funds':
                    assert 'Geld einsammeln' in page.locator('#screen').inner_text()
                    assert 'Gewinne auszahlen' in page.locator('#screen').inner_text()
            page.locator('[data-do="settings"]').first.click()
            assert page.locator('.odin-settings-brand img').evaluate('(e)=>e.complete && e.naturalWidth>0')
            page.locator('#overlay [data-do="close-modal"]').click()
            assert not errors,errors
            assert not page.evaluate('[...document.images].some(x=>x.complete&&x.naturalWidth===0)'), 'broken images'
            results.append({'viewport':f'{w}x{h}','status':'PASS','timing_reference':'PASS','logo':'PASS','navigation':'PASS','overflow':'PASS','js_errors':0,'seconds':round(time.time()-t,1)})
            print('PASS',w,h,'t=',round(time.time()-t,1))
        except Exception as e:
            print('FAIL',w,h,str(e)[:2000]);traceback.print_exc()
            page.screenshot(path=str(out/f'FAIL_{w}.png'),full_page=True)
            results.append({'viewport':f'{w}x{h}','status':'FAIL','error':str(e)})
            break
        finally:ctx.close()
    browser.close()
(out/'report.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf-8')
assert len(results)==4 and all(x['status']=='PASS' for x in results),results