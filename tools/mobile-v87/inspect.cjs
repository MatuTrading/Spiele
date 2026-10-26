const fs=require('fs'),http=require('http'),path=require('path');
const {createRequire}=require('module');
const runtime=process.argv[4]||process.env.ODIN_TEST_RUNTIME;
if(!runtime)throw Error('Pass the runtime directory as the fourth argument or ODIN_TEST_RUNTIME');
const req=createRequire(path.join(path.resolve(runtime),'package.json'));
const chromium=req('@sparticuz/chromium').default;
let pw;try{pw=req('playwright').chromium}catch{pw=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright').chromium}
(async()=>{
const input=process.argv[2],out=process.argv[3];fs.mkdirSync(out,{recursive:true});
const server=http.createServer((request,response)=>{response.setHeader('Content-Type','text/html');response.end(fs.readFileSync(input))});await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await pw.launch({executablePath:await chromium.executablePath(),args:chromium.args,headless:true});
const page=await browser.newPage({viewport:{width:412,height:915},deviceScaleFactor:1,isMobile:true,hasTouch:true});
page.on('pageerror',e=>console.log('ERROR:',e.message));
page.on('console',m=>{if(m.type()==='error')console.log('CONSOLE:',m.text().slice(0,300))});
try{
await page.goto('http://127.0.0.1:'+server.address().port);
await page.locator('#playGameBtn').waitFor({state:'visible',timeout:45000});
await page.screenshot({path:path.join(out,'intro.png')});
await page.locator('#playGameBtn').click();
await page.waitForTimeout(1000);
await page.screenshot({path:path.join(out,'mobile.png')});
console.log('STATE',JSON.stringify(await page.evaluate(()=>window.OdinTest?.getState())));
console.log('RECTS',JSON.stringify(await page.evaluate(()=>['stage','hud','bottom','warriorPanel','msg'].map(id=>({id,rect:document.getElementById(id).getBoundingClientRect().toJSON()})))));
await page.setViewportSize({width:1440,height:1000});await page.waitForTimeout(500);await page.screenshot({path:path.join(out,'desktop.png')});
}catch(e){console.log('FAIL:',e.message);await page.screenshot({path:path.join(out,'failure.png')});process.exitCode=1;}
finally{await browser.close();server.close();}
})();
