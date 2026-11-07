#!/usr/bin/env python3
"""Chromium visual/banking regression for original-based V11.5. No synthetic PASS counts."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
root=Path(__file__).resolve().parent.parent
html=(root/"PrivateMarketsTycoon_V11_5_Nightly_Offline.html").read_text("utf-8")
out=root/"v11_5"/"screenshots";out.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    for w,h in [(360,800),(390,844),(768,1024),(1440,900)]:
        ctx=browser.new_context(viewport={"width":w,"height":h},is_mobile=w<400,has_touch=w<400,accept_downloads=True)
        page=ctx.new_page();errors=[]
        page.on("pageerror",lambda e: errors.append(str(e)))
        page.set_content(html,wait_until="domcontentloaded",timeout=90000)
        page.screenshot(path=str(out/f"start_{w}.png"),full_page=True)
        assert not errors,errors
        assert page.evaluate("document.documentElement.scrollWidth<=innerWidth"),f"Start overflow {w}"
        assert not page.evaluate("[...document.images].some(i=>i.complete && i.naturalWidth===0)"),"Broken images"
        page.locator('[data-do="start-fund"]').click()
        if page.locator('#overlay.visible [data-do="close-modal"]').count():
            page.locator('#overlay.visible [data-do="close-modal"]').click()
        assert page.locator(".mission-level").inner_text()=="1/4"
        hint = page.locator(".decision-head p").first.inner_text()
        assert hint and "Ein gutes Urteil." not in hint, f"Contextual help not shown: {hint}"
        assert page.locator(".mission-level").inner_text()=="1/4"
        page.screenshot(path=str(out/f"playing_{w}.png"),full_page=True)
        for tab in ["funds","team","news","play"]:
            page.locator(f'[data-tab="{tab}"]').last.click()
            if tab == "funds":
                assert "Anlegerkapital abrufen" in page.locator("#screen").inner_text(), "Unclear legacy LP label"
                assert "An Anleger auszahlen" in page.locator("#screen").inner_text(), "Payout button not simplified"
            assert page.evaluate("document.documentElement.scrollWidth<=innerWidth"),f"Overflow {w}: {tab}"
        # A formerly hidden payout on an older fund must now be visible/actionable.
        v=page.evaluate("""() => { const f=state.funds[0];f.realized=50000;f.cash=50000;f.feeDue=0;tab='play';render();return {amount:distributeMax(f),hasAlert:!!document.querySelector('.odin-payout-alert')}; }""")
        assert v["amount"]==50000 and v["hasAlert"],f"Payout banner missing: {v}"
        page.screenshot(path=str(out/f"payout_{w}.png"),full_page=True)
        page.locator('[data-do="jump-payout"]').click()
        back=page.evaluate("""() => ({tab,selected:state.selected,amount:distributeMax(state.funds[0])})""")
        assert back=={"tab":"funds","selected":"own1","amount":50000},f"Wrong fund navigation: {back}"
        assert page.locator(".odin-ready-pill").count()>0,"Missing visible payout badge"
        mission_hidden = page.evaluate("""() => {
            const f=state.funds[0], oldMonth=state.month, oldHolds=f.holdings, oldCommit=f.commitmentTotal;
            f.holdings=[{name:'Test'}]; f.commitmentTotal=1000; state.month=3;
            const result=odinMission();
            f.holdings=oldHolds; f.commitmentTotal=oldCommit; state.month=oldMonth;
            return result==='';
        }""")
        assert mission_hidden, "Completed tutorial still clutters playing view"
        assert not errors,errors
        results.append({"viewport":f"{w}x{h}","start":"PASS","navigation":"PASS","payoutBanner":"PASS","clickThrough":"PASS","guidedNextStep":"PASS","simpleFundLabels":"PASS","missionAutoHide":"PASS","brokenImages":0,"pageerrors":0})
        ctx.close()
    browser.close()
(out/"report.json").write_text(json.dumps(results,indent=2),encoding="utf-8")
print("PASS 4/4 viewport flows; payout, fund navigation, simple labels and guided steps")
