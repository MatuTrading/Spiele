const fs=require('fs'),http=require('http'),path=require('path'),assert=require('assert/strict'),crypto=require('crypto');
const {createRequire}=require('module');
const runtime=process.argv[4]||process.env.ODIN_TEST_RUNTIME;
if(!runtime)throw Error('Pass the runtime directory as the fourth argument or ODIN_TEST_RUNTIME');
const req=createRequire(path.join(path.resolve(runtime),'package.json'));
const chromium=req('@sparticuz/chromium').default;
let pw;try{pw=req('playwright').chromium}catch{pw=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright').chromium}
const input=path.resolve(process.argv[2]),out=path.resolve(process.argv[3]);fs.mkdirSync(out,{recursive:true});
const result={status:'running',sha256:crypto.createHash('sha256').update(fs.readFileSync(input)).digest('hex'),checks:{},errors:[],screens:[]};
const state=page=>page.evaluate(()=>OdinTest.getState());
async function shot(page,name){await page.screenshot({path:path.join(out,name+'.png')});result.screens.push(name);}
async function tapWorld(page,x,z){
 const p=await page.evaluate(([x,z])=>OdinTest.projectPoint(x,z),[x,z]);
 const tag=await page.evaluate(p=>document.elementFromPoint(p.x,p.y)?.tagName,p);
 assert.equal(tag,'CANVAS','Intended world input is obscured at '+JSON.stringify(p)+' by '+tag);
 await page.touchscreen.tap(p.x,p.y);return p;
}
(async()=>{
 const server=http.createServer((request,response)=>{response.setHeader('Content-Type','text/html');response.end(fs.readFileSync(input))});await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const browser=await pw.launch({executablePath:await chromium.executablePath(),args:chromium.args,headless:true});
 let page;
 try{
  const ctx=await browser.newContext({viewport:{width:412,height:915},isMobile:true,hasTouch:true,deviceScaleFactor:1});
  page=await ctx.newPage();page.on('pageerror',e=>result.errors.push(e.message));
  const url='http://127.0.0.1:'+server.address().port;
  await page.goto(url);await page.locator('#playGameBtn').waitFor({state:'visible',timeout:45000});
  await shot(page,'01-intro');await page.locator('#playGameBtn').tap();
  result.initial=await state(page);assert.equal(result.initial.version,'87-mobile-saga');
  assert(await page.evaluate(()=>!!document.querySelector('canvas').getContext('webgl2')));result.checks.webgl=true;
  await ctx.setOffline(true); // No CDN fetch is permitted after the initial document.
  await shot(page,'02-mobile-world');
  await tapWorld(page,7.93,-2.47);
  result.built=await state(page);assert.equal(result.built.defenders,1);assert.equal(result.built.gold,120);result.checks.build=true;
  await shot(page,'03-selected');
  await page.locator('#upgradeBtn').tap();assert.equal((await state(page)).levels[0],2);assert.equal((await state(page)).gold,57);result.checks.upgrade=true;
  await page.locator('#sellTowerBtn').tap();assert(await page.locator('#safeConfirm').isVisible());
  await page.locator('#confirmNo').tap();assert.equal((await state(page)).defenders,1);result.checks.saleCancel=true;
  await page.locator('#moveTowerBtn').tap();
  await tapWorld(page,7.39,-2.27);
  result.moveStart=await state(page);assert(result.moveStart.movingUnits>0,'Movement request failed');
  await page.waitForFunction(()=>OdinTest.getState().movingUnits===0,{timeout:30000});
  result.moveEnd=await state(page);assert(Math.hypot(result.moveEnd.towerPositions[0][0]-result.built.towerPositions[0][0],result.moveEnd.towerPositions[0][2]-result.built.towerPositions[0][2])>.1);
  result.checks.move=true;
  await page.locator('#cameraFocus').tap();for(let i=0;i<7;i++)await page.locator('#zoomIn').tap();await shot(page,'04-archer-close');
  await page.locator('#cameraHome').tap();
  await ctx.setOffline(false);await page.reload();await page.locator('#continueGameBtn').waitFor({state:'visible',timeout:45000});
  await page.locator('#continueGameBtn').tap();result.restored=await state(page);
  assert.equal(result.restored.gold,57);assert.equal(result.restored.levels[0],2);assert.equal(result.restored.defenders,1);result.checks.restore=true;
  await page.locator('#start').tap();await shot(page,'05-briefing');await page.locator('#confirmWaveBtn').tap();
  result.wave=await state(page);assert.equal(result.wave.waveTarget,9);assert(result.wave.enemies>0);result.checks.wave=true;
  await page.locator('#pause').tap();const pause=await page.evaluate(()=>({state:OdinTest.getState(),simTime:OdinTest.inspect().simTime}));
  await page.waitForTimeout(450);const pausedAfter=await page.evaluate(()=>({state:OdinTest.getState(),simTime:OdinTest.inspect().simTime}));
  assert.equal(pausedAfter.simTime,pause.simTime);assert.deepEqual(pausedAfter.state.enemyPositions,pause.state.enemyPositions);result.checks.pauseFreezes=true;
  await page.locator('#menuOpen').tap();await page.locator('#qualitySelect').selectOption('low');await shot(page,'06-settings');await page.locator('#menuClose').tap();
  assert((await state(page)).paused,'Opening and closing menu changed an existing pause');result.checks.menuPause=true;
  await page.locator('#pause').tap();await page.locator('#speedBtn').tap();await page.locator('#speedBtn').tap();assert.equal((await state(page)).gameSpeed,2);
  await page.waitForTimeout(3000);await shot(page,'07-battle');
  await page.locator('#pause').tap();
  for(const [width,height] of [[360,800],[740,360],[1440,1000]]){
    await page.setViewportSize({width,height});await page.waitForTimeout(200);
    const layout=await page.evaluate(()=>{
      const r=id=>document.getElementById(id).getBoundingClientRect().toJSON();
      const buttons=[...document.querySelectorAll('#bottom button,#hud button')].filter(b=>b.getClientRects().length).map(b=>({id:b.id,text:b.textContent,w:b.getBoundingClientRect().width,h:b.getBoundingClientRect().height}));
      return {stage:r('stage'),hud:r('hud'),bottom:r('bottom'),overflow:document.documentElement.scrollWidth>innerWidth,buttons};
    });
    assert(!layout.overflow,'Horizontal overflow at '+width);assert(layout.stage.height>80);assert(layout.stage.top>=layout.hud.bottom);assert(layout.stage.bottom<=layout.bottom.top+1);
    assert(layout.buttons.every(b=>b.h>=43.9&&b.w>=43.9),'Touch target too small at '+width+': '+JSON.stringify(layout.buttons));
    result.checks['layout'+width]=true;result['layout'+width]=layout;await shot(page,'08-layout-'+width);
  }
  // A camera drag with a building category selected must never buy a unit.
  await page.setViewportSize({width:412,height:915});await page.locator('#cameraHome').tap();
  const beforeDrag=await state(page),r=await page.locator('#stage').boundingBox();
  await page.mouse.move(r.x+r.width*.5,r.y+r.height*.45);await page.mouse.down();await page.mouse.move(r.x+r.width*.7,r.y+r.height*.45,{steps:8});await page.mouse.up();
  assert.equal((await state(page)).defenders,beforeDrag.defenders);result.checks.dragNoBuild=true;
  await page.locator('#cameraHome').tap();
  const cdp=await ctx.newCDPSession(page);
  await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:140,y:350,id:1},{x:260,y:350,id:2}]});
  await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:120,y:350,id:1},{x:280,y:350,id:2}]});
  await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
  assert.equal((await state(page)).defenders,beforeDrag.defenders);result.checks.pinchNoBuild=true;
  await page.locator('#cameraHome').tap();
  await ctx.setOffline(true);
  await page.goto(require('url').pathToFileURL(input).href);
  await page.locator('#playGameBtn').waitFor({state:'visible',timeout:45000});await page.locator('#playGameBtn').tap();
  assert((await state(page)).worldIsReady);result.checks.offlineFileStart=true;await shot(page,'09-offline');
  assert.equal(result.errors.length,0,'JavaScript errors');result.status='passed';
 }catch(e){result.status='failed';result.failure=e.stack;process.exitCode=1;if(page&&!page.isClosed()){try{await shot(page,'failure');console.log('STATE ON FAILURE',JSON.stringify(await page.evaluate(()=>({state:window.OdinTest?.getState(),msg:document.getElementById('msg')?.textContent}))));}catch{}}}
 finally{fs.writeFileSync(path.join(out,'result.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));await browser.close();server.close();}
})();
