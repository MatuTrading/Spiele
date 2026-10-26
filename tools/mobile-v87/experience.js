// V87 Mobile Saga: interaction, waves, persistence and visual feedback.
let gameSpeed=1,simTime=0,waveTarget=0,downThisWave=0,waveStartHp=20;
let runEnded=false,restorePending=null,lastHudUpdate=0,confirmAction=null,menuWasPaused=false,confirmWasPaused=false;
let quality='balanced',bestWave=0,lastCheckpoint=null;
const stage=$('stage'),stageBounds=new THREE.Box3();
const waveTitles=['Die Vorhut','Schnelle Klingen','Der Schildwall','Drei Wege, eine Burg','Der Kriegsherr'];
const enemyKinds={
  raider:{name:'Plünderer',hp:1,speed:1,armor:0,bounty:9,damage:1,color:0xd2b17c},
  runner:{name:'Späher',hp:.72,speed:1.32,armor:0,bounty:10,damage:1,color:0x73d7bc},
  guard:{name:'Schildträger',hp:1.7,speed:.79,armor:.22,bounty:15,damage:1,color:0x9bb6c8},
  chief:{name:'Kriegsherr',hp:4.0,speed:.73,armor:.12,bounty:38,damage:2,color:0xe9aa50}
};
const saveKey='odin-mobile-v87-checkpoint';
function readStored(key){try{return JSON.parse(localStorage.getItem(key)||'null')}catch{return null}}
function writeStored(key,value){try{localStorage.setItem(key,JSON.stringify(value));return true}catch{return false}}
const storedSettings=readStored('odin-mobile-v87-settings');
if(['low','balanced','high'].includes(storedSettings?.quality))quality=storedSettings.quality;
bestWave=Math.max(0,Number(readStored('odin-mobile-v87-best'))||0);
function profileFor(n,index){
  const total=Math.min(7+n*2,39);
  if(n%5===0&&index===total-1)return 'chief';
  if(n>=3&&index%4===2)return 'guard';
  if(n>=2&&index%3===1)return 'runner';
  return 'raider';
}
function planFor(n){const count=Math.min(7+n*2,39),counts={raider:0,runner:0,guard:0,chief:0};for(let i=0;i<count;i++)counts[profileFor(n,i)]++;return {count,counts,title:waveTitles[(n-1)%5]};}
function updatePauseButton(){
  $('pause').innerHTML=paused?'<svg viewBox="0 0 24 24"><path d="m9 5 11 7-11 7Z"/></svg>':'<svg viewBox="0 0 24 24"><path d="M8 5v14M16 5v14"/></svg>';
  $('pause').setAttribute('aria-label',paused?'Spiel fortsetzen':'Spiel pausieren');$('pause').setAttribute('aria-pressed',String(paused));
}
function refreshMobileHud(){
  if(!$('waveLabel'))return;
  const plan=planFor(Math.max(1,wave));
  $('waveLabel').textContent=active?'Welle '+wave+' · '+plan.title:wave?'Welle '+wave+' geschafft':'Die Burg zählt auf dich';
  $('waveCount').textContent=active?Math.max(0,waveTarget-downThisWave)+' Gegner verbleiben':'Bestleistung: Welle '+bestWave;
  $('waveFill').style.width=active?(100*downThisWave/Math.max(1,waveTarget))+'%':wave?'100%':'0%';
  $('start').disabled=active||runEnded;
  if(!active&&!runEnded)$('start').textContent=wave?'Welle '+(wave+1)+' vorbereiten':'Erste Welle vorbereiten';
  $('start').setAttribute('aria-label',$('start').textContent);
  document.body.classList.toggle('low-hp',hp<=7);
  stage.classList.toggle('threat',enemies.some(e=>e.siege));
  for(const b of document.querySelectorAll('[data-unit]')){
    if(b.dataset.unit==='erase')continue;
    b.classList.toggle('unaffordable',gold<costs[b.dataset.unit]);
    b.setAttribute('aria-label',towerNames[b.dataset.unit]+', '+costs[b.dataset.unit]+' Gold'+(gold<costs[b.dataset.unit]?', nicht genug Gold':''));
  }
}
function setQuality(value){
  quality=value;const max={low:1,balanced:1.5,high:2}[value]||1.5;
  renderer.setPixelRatio(Math.min(devicePixelRatio,max));
  renderer.shadowMap.enabled=value==='high';
  sun.castShadow=value==='high';sun.shadow.mapSize.set(1024,1024);sun.shadow.camera.left=-15;sun.shadow.camera.right=15;sun.shadow.camera.top=15;sun.shadow.camera.bottom=-15;sun.shadow.camera.far=70;sun.shadow.bias=-.001;
  terrain.forEach(m=>{m.receiveShadow=true;m.castShadow=value==='high'});
  writeStored('odin-mobile-v87-settings',{quality,music:musicEnabled,sound:fxEnabled});
  $('qualitySelect').value=value;resizeStage(false);
}
function resizeStage(fit=false){
  const top=$('hud').getBoundingClientRect().bottom;
  const bottom=$('bottom').getBoundingClientRect().height;
  document.documentElement.style.setProperty('--top',(top+1)+'px');
  document.documentElement.style.setProperty('--dock',bottom+'px');
  const rect=stage.getBoundingClientRect();if(rect.width<1||rect.height<1)return;
  camera.aspect=rect.width/rect.height;camera.updateProjectionMatrix();renderer.setSize(rect.width,rect.height);
  if(fit&&terrain.length)fitMap();
}
function fitMap(){
  if(!terrain.length)return;
  stageBounds.makeEmpty();for(const mesh of terrain)stageBounds.expandByObject(mesh);
  const center=stageBounds.getCenter(new THREE.Vector3());
  const direction=new THREE.Vector3(.44,.76,.61).normalize();
  // Fit all eight terrain corners into the actual, unobstructed canvas.
  const up=new THREE.Vector3(0,1,0),right=new THREE.Vector3().crossVectors(up,direction).normalize(),vertical=new THREE.Vector3().crossVectors(direction,right).normalize();
  const v=Math.tan(THREE.MathUtils.degToRad(camera.fov/2));let distance=0;
  for(const mesh of terrain){
    mesh.geometry.computeBoundingBox();const box=mesh.geometry.boundingBox;if(!box)continue;
    for(const x of [box.min.x,box.max.x])for(const y of [box.min.y,box.max.y])for(const z of [box.min.z,box.max.z]){
      const corner=new THREE.Vector3(x,y,z).applyMatrix4(mesh.matrixWorld).sub(center);
      distance=Math.max(distance,corner.dot(direction)+Math.max(Math.abs(corner.dot(vertical))/v,Math.abs(corner.dot(right))/(v*camera.aspect)));
    }
  }
  distance*=1.035;controls.target.copy(center);camera.position.copy(center).addScaledVector(direction,distance);
  controls.maxDistance=Math.max(50,distance*1.7);controls.minDistance=5.5;controls.update();
}
function setupStage(){
  renderer.domElement.setAttribute('aria-label','3D-Spielfeld. Ziehen verschiebt die Karte, zwei Finger zoomen und drehen.');
  renderer.domElement.tabIndex=0;
  controls.touches.ONE=THREE.TOUCH.PAN;controls.touches.TWO=THREE.TOUCH.DOLLY_ROTATE;
  controls.screenSpacePanning=true;controls.enableDamping=true;controls.dampingFactor=.11;
  controls.maxPolarAngle=1.23;controls.minPolarAngle=.25;
  const ro=new ResizeObserver(()=>resizeStage(false));ro.observe($('hud'));ro.observe($('bottom'));
  addEventListener('resize',()=>resizeStage(true));
  $('zoomIn').onclick=()=>{camera.position.sub(controls.target).multiplyScalar(.82).add(controls.target);controls.update()};
  $('zoomOut').onclick=()=>{camera.position.sub(controls.target).multiplyScalar(1.2).add(controls.target);controls.update()};
  $('cameraHome').onclick=fitMap;
  $('cameraFocus').onclick=()=>{if(!selectedTower)return;const delta=camera.position.clone().sub(controls.target);controls.target.copy(selectedTower.mesh.position).add(new THREE.Vector3(0,.4,0));camera.position.copy(controls.target).add(delta);controls.update()};
  $('speedBtn').onclick=()=>{gameSpeed=gameSpeed===1?1.5:gameSpeed===1.5?2:1;$('speedBtn').textContent=gameSpeed+'×';$('speedBtn').setAttribute('aria-label','Spieltempo '+gameSpeed+'-fach')};
  setQuality(quality);resizeStage(true);
}
function freshCheckpoint(){
  if(!gameStarted||active||hp<=0||movingTower||towers.some(t=>t.moveRoute?.length))return;
  const data={format:'odin-mobile-v87',wave,gold,hp,kills,towers:towers.map(t=>({type:t.type,level:t.level,x:t.mesh.position.x,y:t.mesh.position.y,z:t.mesh.position.z}))};
  if(data.towers.some(t=>!Number.isFinite(t.x)||!Number.isFinite(t.z)))return;
  lastCheckpoint=data;writeStored(saveKey,data);
}
function validCheckpoint(s){
  return s&&s.format==='odin-mobile-v87'&&Number.isInteger(s.wave)&&s.wave>=0&&s.wave<1000&&Number.isFinite(s.gold)&&s.gold>=0&&s.gold<10000000&&Number.isInteger(s.hp)&&s.hp>0&&s.hp<=20&&Number.isInteger(s.kills)&&s.kills>=0&&Array.isArray(s.towers)&&s.towers.length<=80&&s.towers.every(t=>['archer','mage','knight'].includes(t.type)&&Number.isInteger(t.level)&&t.level>=1&&t.level<=3&&[t.x,t.y,t.z].every(Number.isFinite)&&Math.abs(t.x)<30&&Math.abs(t.z)<30);
}
function restoreCheckpoint(){
  if(!validCheckpoint(restorePending))return;
  const s=restorePending;gold=s.gold;hp=s.hp;wave=s.wave;kills=s.kills;gameStarted=true;active=false;paused=false;runEnded=false;
  towers.forEach(t=>scene.remove(t.mesh));towers=[];
  for(const spec of s.towers){
    if(!isLandPoint(spec.x,spec.z))continue;
    const mesh=makeUnit(spec.type);mesh.position.set(spec.x,groundY(spec.x,spec.z),spec.z);scene.add(mesh);
    const ring=makeSelectionRing();mesh.add(ring);const t={mesh,type:spec.type,level:spec.level,ring,cd:0,anim:0,moveRoute:null};makeUpgradeCape(t);towers.push(t);
  }
  $('introOverlay').hidden=true;selectTower(null);updatePauseButton();ui();syncMusic();notify('Willkommen zurück! Welle '+(wave+1)+' wartet.');freshCheckpoint();
}
function setupCheckpoint(){
  restorePending=readStored(saveKey);
  $('continueGameBtn').hidden=!validCheckpoint(restorePending);
  if(validCheckpoint(restorePending))$('continueGameBtn').textContent='Fortsetzen · Welle '+(restorePending.wave+1);
  $('continueGameBtn').onclick=restoreCheckpoint;
}
function openConfirm(title,text,action){confirmWasPaused=paused;paused=true;updatePauseButton();syncMusic();confirmAction=action;$('confirmTitle').textContent=title;$('confirmText').textContent=text;$('safeConfirm').hidden=false;$('confirmNo').focus();}
function closeConfirm(){const wasOpen=!$('safeConfirm').hidden;confirmAction=null;$('safeConfirm').hidden=true;if(wasOpen){paused=confirmWasPaused;updatePauseButton();syncMusic();}}
function finishRun(){
  if(runEnded)return;runEnded=true;active=false;paused=true;bestWave=Math.max(bestWave,wave-1);writeStored('odin-mobile-v87-best',bestWave);
  $('endWave').textContent=Math.max(0,wave-1);$('endKills').textContent=kills;$('endBest').textContent=bestWave;
  $('runEnd').hidden=false;$('replayBtn').focus();updatePauseButton();refreshMobileHud();syncMusic();
  // Never offer the checkpoint of a defeated run as if the defeat had not happened.
  try{localStorage.removeItem(saveKey)}catch{}restorePending=null;$('continueGameBtn').hidden=true;
}
function resetExperience(){
  runEnded=false;waveTarget=0;downThisWave=0;gameSpeed=1;simTime=0;$('speedBtn').textContent='1×';$('runEnd').hidden=true;$('gameMenu').hidden=true;closeConfirm();
  choice='archer';for(const b of document.querySelectorAll('[data-unit]'))b.classList.toggle('active',b.dataset.unit==='archer');
  document.body.classList.remove('unit-selected');freshCheckpoint();updatePauseButton();refreshMobileHud();fitMap();syncMusic();
}
function waveBriefing(){
  const p=planFor(wave+1),chief=p.counts.chief;
  $('waveWarningTitle').textContent='Welle '+(wave+1)+' · '+p.title;
  $('waveWarningText').textContent=nextQuip(scoutWarnings);
  $('briefCount').textContent=p.count;$('briefReward').textContent=30+(wave+1)*6;$('briefType').textContent=chief?'Kriegsherr':p.counts.guard?'Schilde':p.counts.runner?'Späher':'Plünderer';
  $('briefNote').textContent=chief?'Ein Kriegsherr führt den letzten Trupp an. Er trifft die Burg doppelt so hart.':p.counts.guard?'Schildträger widerstehen Pfeilen. Feuer trifft auch nahe Begleiter.':p.counts.runner?'Späher sind schneller. Frost verlangsamt sie vor der Burg.':'Pfeile treffen einzelne Gegner. Frost bremst, Feuer trifft Gruppen.';
}
function waveVictory(){
  active=false;const reward=30+wave*6;gold+=reward;bestWave=Math.max(bestWave,wave);writeStored('odin-mobile-v87-best',bestWave);
  const stars=hp===waveStartHp?'Makellos':hp>=waveStartHp-2?'Gut verteidigt':'Burg gehalten';
  notify(stars+'! +'+reward+' Gold. '+nextQuip(victoryQuips));sound('build');ui();freshCheckpoint();
}
function floatAt(position,text,isGold=false){
  if($('fxLayer').childElementCount>=12||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  const p=position.clone().add(new THREE.Vector3(0,.8,0)).project(camera);if(Math.abs(p.x)>1||Math.abs(p.y)>1||p.z>1)return;
  const rect=stage.getBoundingClientRect(),el=document.createElement('span');el.className='damage-float'+(isGold?' gold':'');el.textContent=text;el.style.left=((p.x+1)*rect.width/2)+'px';el.style.top=((1-p.y)*rect.height/2)+'px';$('fxLayer').appendChild(el);setTimeout(()=>el.remove(),800);
}
function damageEnemy(enemy,amount,type){
  if(!enemies.includes(enemy))return;
  const armor=type==='archer'?enemy.armor:0,hit=Math.max(1,Math.round(amount*(1-armor)));
  enemy.hp=Math.max(0,enemy.hp-hit);floatAt(enemy.mesh.position,'−'+hit);showHp(enemy.healthBar,enemy.hp,enemy.max);
  if(type==='mage'){enemy.slowUntil=simTime+1.8;enemy.slowFactor=.58;}
  if(enemy.hp<=0){
    const reward=enemy.bounty||9;floatAt(enemy.mesh.position,'+'+reward,true);scene.remove(enemy.mesh);enemies.splice(enemies.indexOf(enemy),1);
    enemy.healthBar?.geometry.dispose();enemy.healthBar?.material.map?.dispose();enemy.healthBar?.material.dispose();
    gold+=reward;kills++;downThisWave++;ui();
  }
}
function mobileTick(){
  if(performance.now()-lastHudUpdate>180){lastHudUpdate=performance.now();refreshMobileHud();}
}
function decorateEnemy(mesh,kind){
  if(kind==='raider')return;
  const color=enemyKinds[kind].color;
  const band=new THREE.Mesh(new THREE.RingGeometry(.24,.28,24),new THREE.MeshBasicMaterial({color,transparent:true,opacity:.7,side:THREE.DoubleSide,depthWrite:false}));band.rotation.x=-Math.PI/2;band.position.y=.025;mesh.add(band);
  if(kind==='chief')mesh.scale.multiplyScalar(1.16);
  if(kind==='guard'){
    const char=mesh.userData.character,hand=boneNamed(char,'handslot.l')||boneNamed(char,'hand.l');
    if(hand){const shield=new THREE.Mesh(new THREE.CylinderGeometry(.26,.26,.06,12),new THREE.MeshStandardMaterial({color:0x506e80,metalness:.25,roughness:.6}));shield.rotation.x=Math.PI/2;shield.position.z=.05;hand.add(shield);}
  }
}
function setupMenus(){
  $('menuOpen').onclick=()=>{menuWasPaused=paused;paused=true;updatePauseButton();syncMusic();$('gameMenu').hidden=false;$('menuClose').focus()};
  $('menuClose').onclick=()=>{$('gameMenu').hidden=true;paused=menuWasPaused;updatePauseButton();syncMusic();$('menuOpen').focus()};
  $('menuReset').onclick=()=>openConfirm('Neues Spiel?','Deine aktuelle Verteidigung wird zurückgesetzt. Deine Bestleistung bleibt erhalten.',()=>{$('reset').click()});
  $('confirmYes').onclick=()=>{const fn=confirmAction;closeConfirm();fn?.()};$('confirmNo').onclick=closeConfirm;
  $('replayBtn').onclick=()=>{$('reset').click()};
  $('qualitySelect').onchange=e=>setQuality(e.target.value);
  $('settingsMusic').onclick=()=>{$('musicToggle').click();$('settingsMusic').textContent=musicEnabled?'An':'Aus';writeStored('odin-mobile-v87-settings',{quality,music:musicEnabled,sound:fxEnabled})};
  $('settingsSound').onclick=()=>{$('soundToggle').click();$('settingsSound').textContent=fxEnabled?'An':'Aus';writeStored('odin-mobile-v87-settings',{quality,music:musicEnabled,sound:fxEnabled})};
  if(storedSettings?.music===false){musicEnabled=false;syncMusic()}
  if(storedSettings?.sound===false){fxEnabled=false;window.gameSound?.setEnabled(false)}
  $('settingsMusic').textContent=musicEnabled?'An':'Aus';$('settingsSound').textContent=fxEnabled?'An':'Aus';
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&gameStarted&&!paused){paused=true;updatePauseButton();notify('Automatisch pausiert. Tippe auf Weiter.');syncMusic()}});
}
setupMenus();setupCheckpoint();setupStage();refreshMobileHud();updatePauseButton();
