#!/usr/bin/env python3
"""ODIN Nightly browser QA. Tests the branch preview, not the inaccessible V11 upload."""
import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "PrivateMarketsTycoon_NightlyPreview_0_1_Offline.html"
OUT = ROOT / "qa-artifacts"
SIZES = [(360, 800), (390, 844), (768, 1024), (1440, 900)]
PAGES = ["overview", "market", "private", "company", "funds", "journal"]
KEY = "odin-pmt-nightly-v3"

async def test_viewport(browser, width, height):
    name = f"{width}x{height}"
    ctx = await browser.new_context(
        viewport={"width": width, "height": height},
        device_scale_factor=1,
        is_mobile=width <= 390,
        has_touch=width <= 390,
        reduced_motion="reduce")
    page = await ctx.new_page()
    errors = []
    console_errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    result = {"viewport": name, "checks": [], "errors": errors, "console_errors": console_errors}
    async def step(label, fn):
        try:
            await fn()
            result["checks"].append({"name": label, "status": "PASS"})
        except Exception as err:
            result["checks"].append({"name": label, "status": "FAIL", "error": str(err)[:500]})
            raise
    async def start():
        await page.goto(GAME.as_uri(), wait_until="load", timeout=25000)
        await page.locator("#companyInput").wait_for(timeout=15000)
        await page.fill("#companyInput", "ODIN QA")
        await page.locator("#welcomeForm button[type=submit]").click()
        await page.locator("#modalLayer").wait_for(state="hidden", timeout=7000)
        assert "ODIN QA" in await page.locator("#companyBrand").inner_text()
        await page.locator('[data-speed="0"]').click()
    async def nav(target):
        root = "#mobileNavigation" if width <= 640 else "#navigation"
        button = page.locator(f'{root} [data-action="navigate"][data-id="{target}"]')
        await button.click()
        assert await page.locator(f'{root} [data-id="{target}"]').get_attribute("aria-current") == "page"
        assert await page.locator("#screen").is_visible()
    async def navigation():
        if width <= 640:
            count = await page.locator('#mobileNavigation [data-action="navigate"]').count()
            assert count == 6, f"Only {count} mobile tabs found"
            assert await page.locator('#mobileNavigation [data-action="settings"]').is_visible()
        for target in PAGES:
            await nav(target)
            if width == 390:
                await page.screenshot(path=str(OUT / f"{name}-{target}.png"))
        await nav("overview")
        assert await page.locator(".nightly-coach").is_visible()
    async def trading():
        await nav("market")
        await page.locator("#sharesInput").fill("1")
        await page.locator('[data-action="buyStock"]').first.click()
        trades = await page.evaluate(f"JSON.parse(localStorage.getItem('{KEY}')).stats.trades")
        assert trades >= 1, f"Trade count was {trades}"
    async def deal_management():
        await nav("private")
        await page.locator('[data-action="openDeal"]').first.click()
        await page.locator(".modal").wait_for()
        due_diligence = page.locator('.modal [data-action="dd"]')
        if await due_diligence.count() and await due_diligence.is_enabled():
            await due_diligence.click()
            dd = await page.evaluate(f"JSON.parse(localStorage.getItem('{KEY}')).stats.dd")
            assert dd >= 1, f"Due diligence was {dd}"
        await page.keyboard.press("Escape")
    async def time_and_saving():
        before = await page.evaluate(f"JSON.parse(localStorage.getItem('{KEY}')).month")
        await page.locator("#nextMonth").click()
        after = await page.evaluate(f"JSON.parse(localStorage.getItem('{KEY}')).month")
        assert after == before + 1, f"Month {before} -> {after}"
        await page.reload(wait_until="load")
        after_reload = await page.evaluate(f"JSON.parse(localStorage.getItem('{KEY}')).month")
        assert after_reload == after, f"Not persisted: {after_reload}"
        assert await page.locator("#modalLayer.hidden").count() == 1
    async def settings():
        if width <= 640:
            await page.locator('#mobileNavigation [data-action="settings"]').click()
        else:
            await page.locator("#settingsBtn").click()
        await page.locator(".modal").wait_for()
        assert await page.locator('.modal [data-action="export"]').count() >= 1
        await page.keyboard.press("Escape")
    async def layout():
        await nav("overview")
        await page.wait_for_timeout(250)
        overflow = await page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        assert overflow <= 2, f"Body overflows horizontally: {overflow}px"
        if width <= 390:
            nav_metrics = await page.locator("#mobileNavigation button").evaluate_all(
                "(items) => items.map(el => ({w:el.getBoundingClientRect().width,h:el.getBoundingClientRect().height,label:el.getAttribute('aria-label')||el.innerText}))")
            assert all(x["h"] >= 44 and x["w"] >= 42 for x in nav_metrics), str(nav_metrics)
        await page.screenshot(path=str(OUT / f"{name}-overview-final.png"), full_page=True)
    try:
        await step("Startdialog und Spielstart", start)
        await step("Alle sechs Navigationsseiten", navigation)
        await step("Aktienkauf und Buchhaltung", trading)
        await step("Due Diligence", deal_management)
        await step("Zeitfortschritt, Autosave und Reload", time_and_saving)
        await step("Einstellungen/Export", settings)
        await step("Responsive Layout und Screenshot", layout)
        if errors:
            raise AssertionError(f"JavaScript errors: {errors}")
        result["status"] = "PASS"
    except Exception as err:
        result["status"] = "FAIL"
        result["failure"] = str(err)[:1000]
        try:
            await page.screenshot(path=str(OUT / f"{name}-FAILED.png"), full_page=True)
        except Exception:
            pass
    finally:
        await ctx.close()
    return result

async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if not GAME.exists():
        print(f"Missing game file: {GAME}")
        return 2
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        results = [await test_viewport(browser, w, h) for w, h in SIZES]
        await browser.close()
    result = {"game": str(GAME), "viewports": results, "all_pass": all(x["status"] == "PASS" for x in results)}
    (OUT / "browser-results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["all_pass"] else 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
