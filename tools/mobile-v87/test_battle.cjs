// Scenario tests use explicit saved-game fixtures, not a claimed natural campaign.
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert/strict');
const {createRequire}=require('module');
const runtime=process.argv[4]||process.env.ODIN_TEST_RUNTIME;
if(!runtime)throw Error('Pass the runtime directory as the fourth argument or ODIN_TEST_RUNTIME');
const req=createRequire(path.join(path.resolve(runtime),'package.json'));
const chromium=req('@sparticuz/chromium').default;
let pw;try{pw=req('playwright').chromium}catch{pw=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright').chromium}
const input=path.resolve(process.argv[2]),out=path.resolve(process.argv[3]);fs.mkdirSync(out,{recursive:true});
const result={status:'running',fixture:'Completed wave 4, 650 gold, empty defence; building through real UI',checks:{},errors:[],kinds:[],minEnemySpacing:100,minUnitSpacing:100,samples:[]};
const state=p=>p.evaluate(()=>OdinTest.getState());
(async()=>{
const server=http.createServer((request,response)=>{response.setHeader('Content-Type','text/html');response.end(fs.readFileSync(input))});await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await pw.launch({executablePath:await chromium.executablePath(),args:chromium.args,headless:true});let page;
try{
const context=await browser.newContext({viewport:{width:412,height:915},isMobile:true,hasTouch:true});
await context.addInitScript(()=>{
 localStorage.setItem('odin-mobile-v87-checkpoint',JSON.stringify({format:'odin-mobile-v87',wave:4,gold:650,hp:20,kills:40,towers:[]}));
 localStorage.setItem('odin-mobile-v87-settings',JSON.stringify({quality:'low',music:false,sound:false}));
});
page=await context.newPage();page.on('pageerror',e=>result.errors.push(e.message));
await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#continueGameBtn').waitFor({state:'visible',timeout:45000});await page.locator('#continueGameBtn').tap();
const candidates=[];for(let x=5.6;x<=9.2;x+=.6)for(let z=-2.1;z>=-5.5;z-=.6)candidates.push([+x.toFixed(2),+z.toFixed(2)]);
for(const type of ['archer','mage','knight']){
 await page.locator('[data-unit="'+type+'"]').tap();
 // The initial archer selection is already active; ensure the category is on.
 if((await page.locator('[data-unit="'+type+'"]').getAttribute('aria-pressed'))!=='true')await page.locator('[data-unit="'+type+'"]').tap();
 const sites=await page.evaluate(points=>points.map(([x,z])=>OdinTest.locationInfo(x,z)),candidates);
 const site=sites.filter(p=>p.land&&!p.blocked&&!p.occupied&&p.roadDistance>.44&&p.roadDistance<1.6&&p.visible).sort((a,b)=>Math.hypot(a.x-7,a.z+3.7)-Math.hypot(b.x-7,b.z+3.7)).find(p=>p.screen.y<640);
 assert(site,'No valid '+type+' build site');
 await page.touchscreen.tap(site.screen.x,site.screen.y);
 assert.equal((await state(page)).selectedTower,type,'Build action did not select '+type);
 await page.locator('#upgradeBtn').tap();
 console.log('Built',type,site.x,site.z,JSON.stringify(await state(page)));
}
assert.equal((await state(page)).defenders,3);assert.deepEqual((await state(page)).levels,[2,2,2]);result.checks.threeClasses=true;
await page.locator('#deselectBtn').tap();await page.locator('#start').tap();await page.screenshot({path:path.join(out,'boss-briefing.png')});await page.locator('#confirmWaveBtn').tap();
await page.locator('#speedBtn').tap();await page.locator('#speedBtn').tap();
const seen=new Set();let lastCapture=0,slowSeen=false,moveRequested=false,moveStarted=false,bowRunningSeen=false,detourSeen=false;
const started=Date.now();
while(Date.now()-started<90000){
 const data=await page.evaluate(()=>({state:OdinTest.getState(),inspect:OdinTest.inspect()}));
 if(!moveRequested&&Date.now()-started>7000){
   const p=await page.evaluate(()=>OdinTest.projectPoint(6.8,-3.3,.4));await page.touchscreen.tap(p.x,p.y);
   assert.equal((await state(page)).selectedTower,'archer','Could not select archer with a real touch');await page.locator('#moveTowerBtn').tap();
   const end=await page.evaluate(()=>OdinTest.projectPoint(7.93,-2.47));await page.touchscreen.tap(end.x,end.y);moveRequested=true;
   moveStarted=(await state(page)).movingUnits>0;assert(moveStarted,'Archer did not accept movement in battle');
 }
 if(data.inspect.units.some(t=>t.bowRunning))bowRunningSeen=true;
 if(data.inspect.units.some(t=>t.detouring))detourSeen=true;
 for(const k of data.state.enemyKinds)seen.add(k);
 if(data.inspect.enemies.some(e=>e.slowUntil>data.inspect.simTime))slowSeen=true;
 const e=data.state.enemyPositions,t=data.state.towerPositions;
 for(let i=0;i<e.length;i++)for(let j=i+1;j<e.length;j++)if(Math.abs(e[i][1]-e[j][1])<.65)result.minEnemySpacing=Math.min(result.minEnemySpacing,Math.hypot(e[i][0]-e[j][0],e[i][2]-e[j][2]));
 for(const a of e)for(const b of t)if(Math.abs(a[1]-b[1])<.65)result.minUnitSpacing=Math.min(result.minUnitSpacing,Math.hypot(a[0]-b[0],a[2]-b[2]));
 if(Date.now()-lastCapture>5000){result.samples.push({time:Date.now()-started,hp:data.state.hp,kills:data.state.kills,enemies:data.state.enemies,kinds:data.state.enemyKinds});lastCapture=Date.now();console.log('Battle',JSON.stringify(result.samples.at(-1)));}
 if(seen.has('chief')&&!result.checks.chiefVisible){await page.screenshot({path:path.join(out,'chief.png')});result.checks.chiefVisible=true;}
 if(!data.state.active){result.end=data.state;break;}
 await page.waitForTimeout(250);
}
result.kinds=[...seen];result.checks.frostSlow=slowSeen;
result.checks.bowRunning=bowRunningSeen;result.checks.detourObserved=detourSeen;
assert(seen.has('guard')&&seen.has('runner')&&seen.has('chief'),'Required archetypes never appeared');
assert(slowSeen,'No actual frost slow observed');
assert(result.end,'Wave stalled or exceeded 90-second scenario budget');
assert(moveStarted&&bowRunningSeen,'Movement animation was not observed');
assert.equal(result.end.movingUnits,0,'Archer remained stuck walking after the wave');
result.checks.battleMovement=true;
assert(result.minEnemySpacing>=.34,'Enemies visibly overlapped during scenario');assert(result.minUnitSpacing>=.34,'Enemy walked through defender');
assert.equal(result.errors.length,0);result.checks.waveTerminates=true;await page.screenshot({path:path.join(out,'wave-end.png')});
result.status='passed';
}catch(e){result.status='failed';result.failure=e.stack;process.exitCode=1;if(page){console.log('FailureState',JSON.stringify(await state(page)));await page.screenshot({path:path.join(out,'failure.png')});}}
finally{fs.writeFileSync(path.join(out,'result.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));await browser.close();server.close();}
})();
