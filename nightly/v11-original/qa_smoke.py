#!/usr/bin/env python3
"""GitHub Actions browser smoke checks for the reassembled original-based V11.3."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
html=(root/"PrivateMarketsTycoon_V11_3_Nightly_Offline.html").read_text("utf-8")
shot=root/"screenshots"
shot.mkdir(exist_ok=True)
report=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    for width,height in [(360,800),(390,844),(768,1024),(1440,900)]:
        context=browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1,is_mobile=width<400,has_touch=width<400)
        page=context.new_page()
        errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.set_content(html,wait_until="domcontentloaded",timeout=90000)
        page.screenshot(path=str(shot/f"start_{width}.png"),full_page=True)
        assert page.evaluate("document.documentElement.scrollWidth===innerWidth"),f"Start overflow at {width}"
        assert not errors,errors
        page.locator('[data-do="start-fund"]').click()
        if page.locator('#overlay.visible [data-do="close-modal"]').count():
            page.locator('#overlay.visible [data-do="close-modal"]').click()
        assert page.locator(".mission-level").inner_text()=="1/4"
        page.screenshot(path=str(shot/f"game_{width}.png"),full_page=True)
        for tab in ["funds","team","news","play"]:
            page.locator(f'[data-tab="{tab}"]').last.click()
            assert page.evaluate("document.documentElement.scrollWidth===innerWidth"),f"Overflow {width} {tab}"
        assert not errors, errors
        report.append({"viewport":f"{width}x{height}","status":"PASS","navigation":4,"pageerrors":0})
        context.close()
    browser.close()
(shot/"report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print("PASS",len(report),"viewport flows with screenshots and navigation")
