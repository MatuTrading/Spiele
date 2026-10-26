// Regression fixture: a warrior left on the shared three-branch intersection.
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert/strict'),{createRequire}=require('module');
const [inputArg,outArg,runtimeArg,mode='fixed']=process.argv.slice(2),input=path.resolve(inputArg),out=path.resolve(outArg);
const req=createRequire(path.join(path.resolve(runtimeArg),'package.json')),chromium=req('@sparticuz/chromium').default;
let pw;try{pw=req('playwright').chromium}catch{pw=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright').chromium}
fs.mkdirSync(out,{recursive:true});
const result={status:'running',mode,fixture:'Wave 9, level-1 archer stranded at shared junction [7.00839,-5.07966]',errors:[],passed:0,minSpacing:100,samples:[]};
const passedBranches=new Set();
(async()=>{
 const server=http.createServer((request,response)=>{response.setHeader('Content-Type','text/html');response.end(fs.readFileSync(input))});await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const browser=await pw.launch({executablePath:await chromium.executablePath(),args:chromium.args,headless:true});let page;
 try{
 const context=await browser.newContext({viewport:{width:412,height:915},isMobile:true,hasTouch:true});
 await context.addInitScript(()=>{
  localStorage.setItem('odin-mobile-v87-settings',JSON.stringify({quality:'low',music:false,sound:false}));
  localStorage.setItem('odin-mobile-v87-checkpoint',JSON.stringify({format:'odin-mobile-v87',wave:8,gold:0,hp:20,kills:0,towers:[{type:'archer',level:1,x:7.00839,y:0,z:-5.07966}]}));
 });
 page=await context.newPage();page.on('pageerror',e=>result.errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#continueGameBtn').waitFor({state:'visible',timeout:45000});await page.locator('#continueGameBtn').tap();
 await page.screenshot({path:path.join(out,'before.png')});
 await page.locator('#start').tap();await page.locator('#confirmWaveBtn').tap();
 const start=Date.now();let lastSample=0;
 while(Date.now()-start<90000){
  const data=await page.evaluate(()=>({s:OdinTest.getState(),i:OdinTest.inspect()}));
  const p=data.s.towerPositions[0];
  for(let i=0;i<data.s.enemies;i++){
   const e=data.s.enemyPositions[i],branch=data.s.enemyBranches[i];
   if((branch===0&&e[0]>7.45&&e[2]<-4.1)||(branch===1&&e[0]>7.1&&e[2]<-5.5)||(branch===2&&e[0]<6.55&&e[2]<-4.8)){result.passed++;passedBranches.add(branch);}
   if(Math.abs(e[1]-p[1])<.65)result.minSpacing=Math.min(result.minSpacing,Math.hypot(e[0]-p[0],e[2]-p[2]));
  }
  result.end=data.s;
  if(data.i.simTime-lastSample>.5){result.samples.push({simTime:data.i.simTime,position:p,enemies:data.s.enemies,kills:data.s.kills,yielding:data.i.units[0]?.yielding});lastSample=data.i.simTime;}
  if(data.i.simTime>=16)break;
  await page.waitForTimeout(120);
 }
 await page.screenshot({path:path.join(out,'after.png')});
 const end=result.end.towerPositions[0],moved=Math.hypot(end[0]-7.00839,end[2]+5.07966);result.passedBranches=[...passedBranches];
 result.moved=moved;result.location=await page.evaluate(([x,y,z])=>OdinTest.locationInfo(x,z),end);
 assert(result.samples.at(-1)?.simTime>14,'Insufficient simulation time');assert.equal(result.errors.length,0);
 if(mode==='baseline'){
  assert.equal(result.passed,0,'Baseline did not reproduce roadblock');assert(moved<.03);result.reproduced=true;
 }else{
  assert(result.passed>0,'No barbarian passed the blocked intersection');assert.equal(passedBranches.size,3,'A branch still jammed at the fork');assert(moved>.35,'Stranded warrior did not clear road');assert(result.location.roadDistance>=.57,'Warrior stopped on traffic lane');assert(result.minSpacing>=.34,'Warrior and barbarian intersected');
 }
 result.status='passed';
 }catch(e){result.status='failed';result.failure=e.stack;process.exitCode=1;if(page&&!page.isClosed())await page.screenshot({path:path.join(out,'failure.png')});}
 finally{fs.writeFileSync(path.join(out,'result.json'),JSON.stringify(result,null,2));console.log(JSON.stringify({...result,samples:result.samples.length}));await browser.close();server.close();}
})();
