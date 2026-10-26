const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert/strict'),{createRequire}=require('module');
const input=path.resolve(process.argv[2]),out=path.resolve(process.argv[3]),req=createRequire(path.join(path.resolve(process.argv[4]),'package.json'));
const chromium=req('@sparticuz/chromium').default;let pw;try{pw=req('playwright').chromium}catch{pw=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright').chromium}
fs.mkdirSync(out,{recursive:true});const result={status:'running',checks:{},errors:[],motionSamples:[],fixture:'Saved-game motion and one-HP defeat scenarios'};
const state=p=>p.evaluate(()=>OdinTest.getState());
(async()=>{
const server=http.createServer((request,response)=>{response.setHeader('Content-Type','text/html');response.end(fs.readFileSync(input))});await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await pw.launch({executablePath:await chromium.executablePath(),args:chromium.args,headless:true});let page;
try{
const context=await browser.newContext({viewport:{width:412,height:915},isMobile:true,hasTouch:true});
await context.addInitScript(()=>{
 const defeat=location.pathname==='/defeat';
 localStorage.setItem('odin-mobile-v87-checkpoint',JSON.stringify({format:'odin-mobile-v87',wave:0,gold:120,hp:defeat?1:20,kills:0,towers:defeat?[]:[{type:'archer',level:1,x:7.93,y:0,z:-2.47}]}));
 localStorage.setItem('odin-mobile-v87-settings',JSON.stringify({quality:'low',music:false,sound:false}));
});
page=await context.newPage();page.on('pageerror',e=>result.errors.push(e.message));
const url='http://127.0.0.1:'+server.address().port;
await page.goto(url+'/motion');await page.locator('#continueGameBtn').waitFor({state:'visible',timeout:45000});await page.locator('#continueGameBtn').tap();
await page.waitForFunction(()=>!OdinTest.getState().movingUnits&&!OdinTest.getState().pendingRelocations,{timeout:15000});
await page.locator('#start').tap();await page.locator('#confirmWaveBtn').tap();
const unit=await page.evaluate(()=>{const p=OdinTest.getState().towerPositions[0];return OdinTest.projectPoint(p[0],p[2],.4)});await page.touchscreen.tap(unit.x,unit.y);assert.equal((await state(page)).selectedTower,'archer');assert.equal((await state(page)).defenders,1);
await page.locator('#moveTowerBtn').tap();const goal=await page.evaluate(()=>OdinTest.projectPoint(6.2,-2.7));await page.touchscreen.tap(goal.x,goal.y);
assert((await state(page)).movingUnits>0);let detourSeen=false,minDistance=100,bowRun=false;
const started=Date.now();
while(Date.now()-started<35000){
 const d=await page.evaluate(()=>({s:OdinTest.getState(),i:OdinTest.inspect()}));const t=d.s.towerPositions[0];
 if(d.i.units.some(u=>u.bowRunning))bowRun=true;
 if(d.i.units.some(u=>u.detouring)&&!detourSeen){detourSeen=true;await page.screenshot({path:path.join(out,'detour.png')});}
 for(const e of d.s.enemyPositions)if(Math.abs(e[1]-t[1])<.65)minDistance=Math.min(minDistance,Math.hypot(e[0]-t[0],e[2]-t[2]));
 result.motionSamples.push({time:Date.now()-started,position:t,queue:d.s.moveQueueLengths[0],detour:d.i.units[0].detouring,traffic:d.i.units[0]});
 if(!d.s.movingUnits&&!d.s.pendingRelocations){result.motionEnd=d.s;break;}
 await page.waitForTimeout(160);
}
result.detourSeen=detourSeen;result.minDistance=minDistance;
assert(result.motionEnd,'Archer remained stuck or circled for 35 seconds');
assert(Math.hypot(result.motionEnd.towerPositions[0][0]-6.2,result.motionEnd.towerPositions[0][2]+2.7)<.35,'Archer stopped before its target');
assert(bowRun,'Bow run state absent');assert(minDistance>=.34,'Motion crossed an enemy');result.checks.motion=true;
await page.screenshot({path:path.join(out,'motion-arrived.png')});
await page.goto(url+'/defeat');await page.locator('#continueGameBtn').waitFor({state:'visible',timeout:45000});await page.locator('#continueGameBtn').tap();
await page.locator('#start').tap();await page.locator('#confirmWaveBtn').tap();await page.locator('#speedBtn').tap();await page.locator('#speedBtn').tap();
await page.locator('#runEnd').waitFor({state:'visible',timeout:75000});result.defeat=await state(page);assert(result.defeat.runEnded&&result.defeat.hp===0&&!result.defeat.active);result.checks.defeat=true;
await page.screenshot({path:path.join(out,'defeat.png')});await page.locator('#replayBtn').tap();const reset=await state(page);assert.equal(reset.hp,20);assert.equal(reset.wave,0);assert(!reset.runEnded);assert.equal(reset.defenders,0);result.checks.replay=true;
assert.equal(result.errors.length,0);result.status='passed';
}catch(e){result.status='failed';result.failure=e.stack;process.exitCode=1;if(page&&!page.isClosed()){console.log('Fail',JSON.stringify(await state(page)));await page.screenshot({path:path.join(out,'failure.png')});}}
finally{fs.writeFileSync(path.join(out,'result.json'),JSON.stringify(result,null,2));console.log(JSON.stringify({...result,motionSamples:result.motionSamples.length}));await browser.close();server.close();}
})();
