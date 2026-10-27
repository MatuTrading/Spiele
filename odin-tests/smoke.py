import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8000/'
out=Path('odin-test-results');out.mkdir(exist_ok=True)
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox','--enable-webgl','--use-gl=angle','--use-angle=swiftshader'])
 for name,w,h in [('desktop',1366,768),('mobile',390,844)]:
  page=browser.new_page(viewport={'width':w,'height':h},is_mobile=name=='mobile',has_touch=name=='mobile')
  errors=[]
  page.on('pageerror',lambda e: errors.append(str(e)))
  result={'viewport':name}
  try:
   page.goto(url,wait_until='domcontentloaded',timeout=20000)
   page.wait_for_timeout(1500)
   result.update(title=page.title(),canvases=page.locator('canvas').count(),webgl=page.evaluate("() => !!document.createElement('canvas').getContext('webgl')"),errors=errors)
   page.screenshot(path=str(out/f'{name}.png'))
  except Exception as e: result['error']=str(e)
  results.append(result);page.close()
 browser.close()
(out/'report.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
