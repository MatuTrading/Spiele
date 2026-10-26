"""Build a separate V87 candidate without changing the imported V86 source."""
import argparse
import hashlib
import json
import re
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('source',type=Path)
p.add_argument('destination',type=Path)
a=p.parse_args()
source=a.source.read_text()
s=source
root=Path(__file__).parent
def replace(old,new,count=1):
    global s
    if s.count(old)!=count: raise ValueError(f'Expected {count} occurrence(s): {old[:100]} (found {s.count(old)})')
    s=s.replace(old,new)
def section(start,end,new):
    global s
    x=s.index(start);y=s.index(end,x)
    s=s[:x]+new+'\n'+s[y:]
def icon(shape):
    shapes={
      'bow':'<path d="M6 3c15 6 15 12 0 18L11 12 6 3ZM11 12h11m-4-3 4 3-4 3"/>',
      'frost':'<path d="M12 2v20M3 7l18 10M3 17 21 7M9 4l3 3 3-3M9 20l3-3 3 3M3 11l4-1-1-4m15 7-4 1 1 4M6 18l1-4-4-1m15-7-1 4 4 1"/>',
      'fire':'<path d="M13 2c1 7 7 8 7 14a8 8 0 0 1-16 0c0-4 3-7 5-9-1 5 1 5 2 6 2-3 2-7 2-11Z"/>',
      'home':'<path d="m3 11 9-8 9 8M5 10v11h14V10M10 21v-7h4v7"/>',
      'plus':'<path d="M12 5v14M5 12h14"/>',
      'minus':'<path d="M5 12h14"/>',
      'menu':'<path d="M5 6h14M5 12h14M5 18h14"/>',
      'pause':'<path d="M8 5v14M16 5v14"/>'}
    return '<svg aria-hidden="true" viewBox="0 0 24 24">'+shapes[shape]+'</svg>'

replace('<title>Kampf für Odin – Meine Spielwelt</title>','<title>Kampf für Odin · Mobile Saga V87</title>')
replace('width=device-width,initial-scale=1,user-scalable=no','width=device-width,initial-scale=1,viewport-fit=cover')
replace('Bitte mit Internetverbindung in Chrome oder Edge öffnen.','Bitte in einem aktuellen Chrome oder Edge öffnen.')
replace('Die 3D-Bibliothek antwortet nicht. Prüfe deine Internetverbindung oder CDN-Blockierung.','Die 3D-Welt konnte nicht initialisiert werden. Schließe andere Tabs und öffne die Datei erneut.')
replace('</head>','<meta name="theme-color" content="#102a32"><style>'+root.joinpath('mobile.css').read_text()+'</style></head>')
start=s.index('<div id="hud">');end=s.index('<div id="warriorPanel"',start)
s=s[:start]+'''<div id="stage"><div id="fxLayer"></div><div id="gestureHint">Ziehen: verschieben · Zwei Finger: zoomen &amp; drehen</div><div id="cameraBar">
<button id="zoomIn" aria-label="Heranzoomen">'''+icon('plus')+'''</button><button id="zoomOut" aria-label="Herauszoomen">'''+icon('minus')+'''</button><button id="cameraHome" aria-label="Gesamte Karte anzeigen">'''+icon('home')+'''</button><button id="speedBtn" aria-label="Spieltempo 1-fach">1×</button></div></div>
<header id="hud"><span class="pill"><span>Gold</span><b id="gold">180</b></span><span class="pill"><span>Burg</span><b id="hp">20</b></span><span class="pill"><span>Welle</span><b id="wave">0</b></span><span class="pill"><span>Besiegt</span><b id="kills">0</b></span>
<button id="pause" aria-label="Spiel pausieren">'''+icon('pause')+'''</button><button id="menuOpen" aria-label="Spielmenü öffnen">'''+icon('menu')+'''</button>
<div id="waveInfo"><span id="waveLabel">Die Burg zählt auf dich</span><span id="waveCount">Bestleistung: Welle 0</span><div id="waveTrack"><span id="waveFill"></span></div></div></header>
<div id="msg" role="status" aria-live="polite"></div>
<nav id="bottom" aria-label="Verteidiger bauen">'''+''.join('<button data-unit="'+t+'"'+(' class="active"' if t=='archer' else '')+' aria-pressed="'+str(t=='archer').lower()+'">'+icon(i)+'<strong>'+name+'</strong><small>'+str(cost)+' Gold</small></button>' for t,i,name,role,cost in [('archer','bow','Bogenschütze','Präzision',60),('mage','frost','Frostmagier','Bremst Gegner',90),('knight','fire','Feuermagier','Flächenschaden',75)])+'''<button id="start">Erste Welle vorbereiten</button></nav><button id="reset" hidden>Neustart</button>'''+s[end:]
replace('class="odin-crest">⚔️','class="odin-crest" aria-hidden="true">ᛟ')
replace('<button id="cameraHome"', '<button id="cameraFocus" aria-label="Ausgewählten Krieger zentrieren" hidden><svg aria-hidden="true" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"/><path d="M12 2v5m0 10v5M2 12h5m10 0h5"/></svg></button><button id="cameraHome"')
replace('class="odin-crest" aria-hidden="true">ᛟ','class="odin-crest" aria-hidden="true"><svg viewBox="0 0 50 60"><path d="m25 4 16 18-16 18L9 22 25 4Zm-8 27L9 55m24-24 8 24M25 40v16"/></svg>')
replace('ᚠ ᚢ ᚦ ᚨ ᚱ ᚲ ᚷ','N O R D · S A G A')
replace('ᛟ ᛞ ᛁ ᚾ &nbsp; • &nbsp; Mögen die Götter mit dir sein!','DEIN LAND. DEINE VERTEIDIGUNG.')
replace('<div class="odin-kicker">Ein Abenteuer für Walhalla</div>','<div class="odin-kicker">Mobile Saga · V87</div>')
replace('<h1>Kampf für Odin</h1><p>Beschütze die Burg! Barbaren ziehen auf zwei Wegen zum Tor. Baue deine Verteidiger, verbessere sie und rette den Met.</p>','<h1>Kampf<br>für Odin</h1><p>Drei Wege. Eine Burg. Deine Entscheidung.<br>Führe deine Verteidiger und halte die Horde auf.</p><div class="intro-features"><span>Planen</span><span>Kämpfen</span><span>Verbessern</span></div>')
replace('⚔️ FÜR ODIN! SPIEL STARTEN','Neues Abenteuer beginnen')
replace('id="playGameBtn">Neues Abenteuer beginnen</button>','id="playGameBtn">Neues Abenteuer beginnen</button><button id="continueGameBtn" hidden>Fortsetzen</button>')
replace('<p id="waveWarningText">Barbaren im Anmarsch!</p>','<p id="waveWarningText">Barbaren im Anmarsch!</p><div class="briefing"><div><strong id="briefCount">9</strong><span>Gegner</span></div><div><strong id="briefType">Plünderer</strong><span>Gefahr</span></div><div><strong id="briefReward">36</strong><span>Gold bei Sieg</span></div></div><p id="briefNote"></p>')
replace('⚔️ Kampf!','Verteidigung steht – los!')
replace('</body>', '''<div id="gameMenu" class="odin-overlay" role="dialog" aria-modal="true" aria-labelledby="menuTitle" hidden><div class="odin-intro"><div class="odin-kicker">Eine kurze Rast</div><h2 id="menuTitle">Dein Spiel</h2><div class="settings-row"><span>Grafik</span><select id="qualitySelect" aria-label="Grafikqualität"><option value="low">Sparsam</option><option value="balanced" selected>Ausgewogen</option><option value="high">Hohe Details</option></select></div><div class="settings-row"><span>Musik</span><button id="settingsMusic">An</button></div><div class="settings-row"><span>Geräusche</span><button id="settingsSound">An</button></div><p id="menuDescription">Deine Verteidigung wird zwischen den Wellen auf diesem Gerät gespeichert. Beim Wechsel in eine andere App pausiert das Spiel.</p><div class="menu-actions"><button id="menuClose">Zurück zum Spiel</button><button id="menuReset">Neues Abenteuer</button></div></div></div>
<div id="safeConfirm" class="odin-overlay" role="dialog" aria-modal="true" aria-labelledby="confirmTitle" hidden><div class="odin-intro"><h2 id="confirmTitle">Bist du sicher?</h2><p id="confirmText"></p><div class="confirm-actions"><button id="confirmNo">Abbrechen</button><button id="confirmYes">Bestätigen</button></div></div></div>
<div id="runEnd" class="odin-overlay" role="dialog" aria-modal="true" aria-labelledby="endTitle" hidden><div class="odin-intro"><div class="odin-kicker">Die Saga ist noch nicht zu Ende</div><h2 id="endTitle">Die Burg ist gefallen.</h2><p>Odin zählt auch den Mut. Beim nächsten Mal hält deine Verteidigung länger.</p><div class="result-stats"><div><strong id="endWave">0</strong><small>Wellen gehalten</small></div><div><strong id="endKills">0</strong><small>Gegner besiegt</small></div></div><p>Deine Bestleistung: Welle <b id="endBest">0</b></p><button id="replayBtn">Ein neues Abenteuer</button></div></div></body>''')

replace('document.body.appendChild(renderer.domElement);',"document.getElementById('stage').prepend(renderer.domElement);renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.15;")
replace('scene.background=new THREE.Color(0x9cbac5);scene.fog=new THREE.Fog(0x9cbac5,28,65);','scene.background=new THREE.Color(0xa9c7cc);scene.fog=new THREE.Fog(0xa9c7cc,65,110);')
replace('maybeShowIntro();\n  },e=>',"maybeShowIntro();setQuality(quality);resizeStage(true);\n  },e=>")
section('function notify(s){','const groundY=',r'''function notify(s){
  $('msg').textContent=s;$('msg').classList.add('visible');clearTimeout(notify.timer);
  notify.timer=setTimeout(()=>$('msg').classList.remove('visible'),4300);
}
function ui(){
  $('gold').textContent=gold;$('hp').textContent=hp;$('wave').textContent=wave;$('kills').textContent=kills;
  updateCastleBar();refreshWarriorPanel();refreshMobileHud();
  if(gameStarted&&!active)freshCheckpoint();
}
const groundCache=new Map(),groundRay=new THREE.Raycaster();
''')
section('const groundY=','// Original KayKit',r'''const groundY=(x,z)=>{
  const key=x.toFixed(3)+','+z.toFixed(3);
  if(worldIsReady&&groundCache.has(key))return groundCache.get(key);
  groundRay.set(new THREE.Vector3(x,25,z),new THREE.Vector3(0,-1,0));groundRay.far=50;
  const hits=groundRay.intersectObjects(playableTerrain.length?playableTerrain:terrain,false);
  const y=hits.length?hits[0].point.y:1.1;
  if(worldIsReady&&hits.length){if(groundCache.size>16000)groundCache.clear();groundCache.set(key,y)}
  return y;
};
''')
replace("root.userData.odinBow=bow;","root.userData.odinBow=bow;bow.userData.restQuaternion=bow.quaternion.clone();")
section("  if(bow && state==='run'){","  const staff=",r'''  if(bow){
    if(state==='run'){
      d.character.updateWorldMatrix(true,true);
      const handQ=new THREE.Quaternion(),bodyQ=new THREE.Quaternion();
      bow.parent.getWorldQuaternion(handQ);d.character.getWorldQuaternion(bodyQ);
      bow.quaternion.copy(handQ.invert().multiply(bodyQ));
      bow.userData.wasRunning=true;
    }else if(bow.userData.wasRunning){
      // Restore the authored hand-relative firing grip when leaving the run pose.
      bow.quaternion.copy(bow.userData.restQuaternion);bow.userData.wasRunning=false;
    }
  }
''')
replace("  root.add(character);",r'''  root.add(character);
  const contact=new THREE.Mesh(new THREE.CircleGeometry(.24,20),new THREE.MeshBasicMaterial({color:0x173830,transparent:true,opacity:.18,depthWrite:false}));
  contact.rotation.x=-Math.PI/2;contact.position.y=.018;root.add(contact);
''')
replace("  const panel=$('warriorPanel');panel.hidden=!selectedTower;","  const panel=$('warriorPanel');panel.hidden=!selectedTower;$('cameraFocus').hidden=!selectedTower;document.body.classList.toggle('unit-selected',!!selectedTower);")
replace("  $('upgradeBtn').textContent=t.level>=3?'Max. Stufe':'⬆ Upgrade · '+cost+' Gold';", "  $('upgradeBtn').innerHTML=t.level>=3?'Max. Stufe':'Verbessern<span class=\"amount\">'+cost+' Gold</span>';")
replace("  $('moveTowerBtn').textContent=movingTower?'✕ Abbrechen':'↔ Versetzen';","  $('moveTowerBtn').textContent=movingTower?'Abbrechen':'Versetzen';")
replace("  $('sellTowerBtn').textContent='🪙 Verkaufen · '+Math.round(costs[t.type]*.6+(t.level-1)*costs[t.type]*.35)+' Gold';", "  $('sellTowerBtn').innerHTML='Verkaufen<span class=\"amount\">+'+Math.round(costs[t.type]*.6+(t.level-1)*costs[t.type]*.35)+' Gold</span>';")
replace("opacity:.19,depthWrite:false,depthTest:false","opacity:.06,depthWrite:false,depthTest:false")
replace("  return found;\n}",r'''  if(!found && !choice && matchMedia('(pointer:coarse)').matches){
    for(const t of towers){
      const v=t.mesh.position.clone().add(new THREE.Vector3(0,.35,0)).project(camera);
      const dx=(v.x+1)*rect.width/2+rect.left-clientX,dy=(1-v.y)*rect.height/2+rect.top-clientY;
      const pixels=Math.hypot(dx,dy);if(pixels<22&&pixels<minDist){found=t;minDist=pixels;}
    }
  }
  return found;
}''')
# Make selling reversible at the decision point; remove nothing until confirmed.
replace('  selectedTower=t;\n  movingTower=null;',r'''  selectedTower=t;
  if(t){choice=null;for(const b of document.querySelectorAll('[data-unit]')){b.classList.remove('active');b.setAttribute('aria-pressed','false');}}
  movingTower=null;''')
replace("notify(towerNames[choice]+' platziert! Für Versetzen/Upgrade auf den Krieger klicken.');", "notify(towerNames[tower.type]+' platziert. Tippe ihn zum Verbessern oder Versetzen an.');")
replace("  const refund=Math.round(costs[t.type]*.6+(t.level-1)*costs[t.type]*.35);\n  const idx=", "  const refund=Math.round(costs[t.type]*.6+(t.level-1)*costs[t.type]*.35);\n  openConfirm('Verteidiger verkaufen?',towerNames[t.type]+' wird entfernt. Du erhältst '+refund+' Gold.',()=>{\n  const idx=")
replace("  gold+=refund;ui();sound('build');notify(towerNames[t.type]+' verkauft: +'+refund+' Gold.');\n});", "  gold+=refund;ui();sound('build');notify(towerNames[t.type]+' verkauft: +'+refund+' Gold.');\n  });\n});")
replace("if(gameStarted&&musicEnabled&&!document.hidden)","if(gameStarted&&musicEnabled&&!paused&&!document.hidden)")
replace("  notify('Willkommen! Odin erwartet eine erfolgreiche Verteidigung.');", "  if(restorePending){gold=180;hp=20;wave=0;kills=0;restorePending=null;}\n  ui();freshCheckpoint();resizeStage(true);notify('Wähle einen Verteidiger. Tippe neben einen Weg, um ihn aufzustellen.');")
section('function spawn(){','// ===== Spielsteuerung',r'''function spawn(){
  const routeIndex=(spawned+(wave-1)%3)%3,route=routes[routeIndex],origin=route[0];
  if(enemies.some(e=>!e.siege&&Math.hypot(e.mesh.position.x-origin.x,e.mesh.position.z-origin.z)<.48))return false;
  const kind=profileFor(wave,spawned),profile=enemyKinds[kind],look=randomBarbarianAppearance();
  const mesh=makeUnit('barbarian',look);decorateEnemy(mesh,kind);scene.add(mesh);
  const speed=(.83+wave*.027)*profile.speed;
  const hpEnemy=Math.round((35+wave*10)*Math.pow(1.045,Math.max(0,wave-4))*profile.hp);
  const healthBar=createHealthBar(kind==='chief'?.7:.5,.06);healthBar.position.y=.93;mesh.add(healthBar);
  const e={mesh,route,index:0,t:0,hp:hpEnemy,max:hpEnemy,speed,offset:0,kind,armor:profile.armor,bounty:profile.bounty,castleDamage:profile.damage,
    siege:false,siegeCooldown:0,strikeDelay:-1,siegeSlot:-1,healthBar,appearance:look,routeIndex,slowUntil:0};
  enemies.push(e);mesh.position.set(origin.x,groundY(origin.x,origin.z)+.02,origin.z);showHp(healthBar,e.hp,e.max);return true;
}
''')
replace("  paused=false;\n  $('pause').textContent='⏸ Pause';", "  freshCheckpoint();waveStartHp=hp;downThisWave=0;waveTarget=planFor(wave+1).count;\n  paused=false;updatePauseButton();")
replace("  spawnTimer=.95+Math.random()*.52;","  spawnTimer=Math.max(.68,1.18-wave*.025);")
replace("  $('waveWarningTitle').textContent='Welle '+(wave+1)+' naht!';\n  $('waveWarningText').textContent=nextQuip(scoutWarnings);", "  waveBriefing();")
replace("  if(!worldIsReady) return;\n  paused=!paused;", "  if(!worldIsReady||runEnded||!$('gameMenu').hidden||!$('safeConfirm').hidden) return;\n  paused=!paused;")
replace("  $('pause').textContent=paused?'▶ Weiter':'⏸ Pause';", "  updatePauseButton();syncMusic();")
replace("  notify('Neues Spiel! Platziere deine Verteidiger.');", "  resetExperience();notify('Neues Abenteuer! Platziere deine Verteidiger.');")
replace("    if(choice)notify(choice==='erase'?'Klicke auf einen Krieger zum Entfernen.':towerNames[choice]+' ausgewählt.');", "    if(choice)notify(choice==='erase'?'Klicke auf einen Krieger zum Entfernen.':towerNames[choice]+' ausgewählt. Tippe neben einen Weg.');")
replace('function routeForMoving(start,end){','function routeForMoving(start,end){\n  const connector=nearbyWalkRoute(start,end);if(connector)return connector;')
replace('      edges[a].push([b,d]);edges[b].push([a,d]);','      if(segmentClear(nodes[a],nodes[b],.12)){edges[a].push([b,d]);edges[b].push([a,d]);}')
replace('if(d<.20&&Math.abs(nodes[i].y-nodes[k].y)<.30){','if(d<.20&&Math.abs(nodes[i].y-nodes[k].y)<.30&&segmentClear(nodes[i],nodes[k],.12)){')
section('function moveTowerStep(t,dt){','function snapOffRoad',r'''function moveTowerStep(t,dt){
  const queue=t.moveRoute;if(!queue?.length){t.moveRoute=null;return false;}
  const from=t.mesh.position,to=queue[0],walk=dt*1.65;
  const ahead=queue[Math.min(queue.length-1,5)],forward=ahead.clone().sub(from);forward.y=0;if(forward.lengthSq()<.00001)forward.set(0,0,1);forward.normalize();
  const blockers=[...towers.filter(o=>o!==t),...enemies].filter(o=>Math.abs(o.mesh.position.y-from.y)<.65);
  const blocker=blockers.find(o=>{const d=o.mesh.position.clone().sub(from);return d.length()<1.0&&d.dot(forward)>-.12&&Math.abs(d.x*forward.z-d.z*forward.x)<.48;});
  if(blocker&&!t.yielding&&!t.detouring&&simTime>(t.retryAfter||0)){
    const rejoin=Math.min(queue.length-1,10),goal=queue[rejoin],perp=new THREE.Vector3(-forward.z,0,forward.x),center=blocker.mesh.position;
    let detour=null;
    for(const side of [t.avoidSide||1,-(t.avoidSide||1)]){
      const pts=[from.clone().addScaledVector(perp,.52*side),center.clone().addScaledVector(perp,.66*side),center.clone().addScaledVector(perp,.66*side).addScaledVector(forward,.6),goal.clone()];
      let prev=from,ok=true;
      for(const p of pts){p.y=groundY(p.x,p.z);if(!isLandPoint(p.x,p.z)||Math.abs(p.y-prev.y)>.26||obstacleAt(p.x,p.z,p.y,.12)||!segmentClear(prev,p,.12)){ok=false;break;}prev=p;}
      if(ok){detour=pts;t.avoidSide=side;break;}
    }
    if(detour){queue.splice(0,rejoin+1,...detour);t.detouring=detour[detour.length-1];}
    else {t.retryAfter=simTime+.4;return false;}
  }
  const target=queue[0],direction=target.clone().sub(from);direction.y=0;const dist=direction.length();
  const candidate=dist<=walk?target.clone():from.clone().lerp(target,walk/Math.max(dist,.0001));
  if(obstacleAt(candidate.x,candidate.z,candidate.y,.12)||!segmentClear(from,candidate,.12)){if(!t.resumeDestination&&queue.length)t.resumeDestination=queue[queue.length-1].clone();trafficLog(t,'terrain-stop');t.moveRoute=null;t.detouring=null;t.yielding=false;t.yieldTarget=null;t.resumeNotBefore=simTime+.45;notify('Der Krieger sucht einen freien Straßenanschluss.');return false;}
  for(const other of blockers){
    const p=other.mesh.position,after=Math.hypot(candidate.x-p.x,candidate.z-p.z),before=Math.hypot(from.x-p.x,from.z-p.z);
    if(after<.44&&after<=before+.001){
      if(t.yielding){t.yieldStuck=(t.yieldStuck||0)+dt;if(t.yieldStuck>.45){t.moveRoute=null;t.yielding=false;t.yieldTarget=null;t.yieldRetry=simTime+.18;}}
      return false;
    }
  }
  t.yieldStuck=0;from.copy(candidate);if(dist<=Math.max(walk,.01)){queue.shift();if(t.detouring===target)t.detouring=null;}
  if(dist>.001){const yaw=Math.atan2(direction.x,direction.z),delta=Math.atan2(Math.sin(yaw-t.mesh.rotation.y),Math.cos(yaw-t.mesh.rotation.y));t.mesh.rotation.y+=delta*Math.min(1,dt*14);}
  if(selectedTower===t)updateRangePreview(t);
  if(!queue.length){
    trafficLog(t,t.yielding?'yield-complete':'arrived');
    t.moveRoute=null;t.detouring=null;const yielded=t.yielding;t.yielding=false;t.yieldTarget=null;
    if(yielded){t.resumeNotBefore=simTime+.65;if(selectedTower===t)notify(t.resumeDestination?'Wartet am Rand und läuft danach weiter.':'Die Straße ist frei.');}
    else {t.resumeDestination=null;notify(towerNames[t.type]+' ist angekommen.');}
    freshCheckpoint();
  }
  return true;
}
''')
replace("function placeAt(clientX,clientY){", "function placeAt(clientX,clientY){\n  if(!gameStarted||runEnded||!$('gameMenu').hidden||!$('safeConfirm').hidden)return;")
replace('  if(pathDistance(pos.x,pos.z)<.40){','  if(pathDistance(pos.x,pos.z)<.62){')
section('function snapOffRoad(p){','function placeAt',r'''function snapOffRoad(p){
  if(pathDistance(p.x,p.z)>=.62)return p;
  for(let radius=.12;radius<=1.2;radius+=.12){
    let best=null,score=Infinity;
    for(let j=0;j<32;j++){
      const ang=j*Math.PI/16,x=p.x+Math.cos(ang)*radius,z=p.z+Math.sin(ang)*radius,y=groundY(x,z);
      if(pathDistance(x,z)<.62||!isLandPoint(x,z)||Math.abs(y-p.y)>.23||obstacleAt(x,z,y,.18))continue;
      if(unitOccupantAt(new THREE.Vector3(x,y,z),movingTower,true,.58))continue;
      const value=radius+Math.abs(y-p.y)*2;if(value<score){score=value;best=new THREE.Vector3(x,y,z);}
    }
    if(best)return best;
  }
  return null;
}
''')
replace('    moved.moveRoute=walking.filter(p=>Number.isFinite(p.x)&&Number.isFinite(p.z));','    moved.moveRoute=walking.filter(p=>Number.isFinite(p.x)&&Number.isFinite(p.z));moved.resumeDestination=null;moved.yielding=false;moved.yieldTarget=null;')
replace("  // Road hexagon tiles are valid; actual route centerlines are kept clear.","  if(towers.length>=40){notify('Deine Armee ist vollständig. Verbessere oder versetze deine 40 Verteidiger.');return;}\n  // Road hexagon tiles are valid; actual route centerlines are kept clear.")
# Keep all touch pointers: a two-finger gesture must never place a warrior.
section("renderer.domElement.addEventListener('pointerdown'",'// Expose a small safe diagnostic',r'''const activePointers=new Set();
renderer.domElement.addEventListener('pointerdown',e=>{
  activePointers.add(e.pointerId);
  if(activePointers.size>1){if(pointerDown)pointerDown.cancelled=true;return;}
  if(e.button!==0)return;pointerDown={x:e.clientX,y:e.clientY,id:e.pointerId,time:performance.now(),cancelled:false};
});
renderer.domElement.addEventListener('pointermove',e=>{
  if(pointerDown&&Math.hypot(e.clientX-pointerDown.x,e.clientY-pointerDown.y)>8)pointerDown.cancelled=true;
});
renderer.domElement.addEventListener('pointerup',e=>{
  activePointers.delete(e.pointerId);const start=pointerDown;
  if(!start||e.pointerId!==start.id)return;pointerDown=null;
  if(start.cancelled||activePointers.size||e.button!==0||performance.now()-start.time>700)return;
  if(editingRoutes){addEditorPoint(e.clientX,e.clientY);return;}
  try{placeAt(e.clientX,e.clientY);}catch(err){console.error('Platzieren fehlgeschlagen',err);notify('Platzieren fehlgeschlagen: '+err.message);}
});
renderer.domElement.addEventListener('pointercancel',e=>{activePointers.delete(e.pointerId);pointerDown=null;});
''')
replace('worldIsReady,terrainMeshes:',"version:'87-mobile-saga',gameSpeed,waveTarget,downThisWave,runEnded,enemyKinds:enemies.map(e=>e.kind),enemyPositions:enemies.map(e=>[e.mesh.position.x,e.mesh.position.y,e.mesh.position.z]),worldIsReady,terrainMeshes:")
replace('movingUnits:towers.filter(t=>t.moveRoute?.length).length,','movingUnits:towers.filter(t=>t.moveRoute?.length).length,pendingRelocations:towers.filter(t=>t.resumeDestination).length,')
replace('enemyBranches:enemies.map(e=>e.routeIndex),paused,moveQueueLengths:', 'enemyBranches:enemies.map(e=>e.routeIndex),moveQueueLengths:')
replace('  placeAt, selectTower, pickGround, upgradeCost',r'''  placeAt, selectTower, pickGround, upgradeCost,
  locationInfo:(x,z)=>{const y=groundY(x,z),p=new THREE.Vector3(x,y,z),v=p.clone().project(camera),r=renderer.domElement.getBoundingClientRect(),screen={x:r.left+(v.x+1)*r.width/2,y:r.top+(1-v.y)*r.height/2},hit=pickGround(screen.x,screen.y);return {x,z,y,screen,land:isLandPoint(x,z),blocked:obstacleAt(x,z,y,.18),roadDistance:pathDistance(x,z),occupied:unitOccupantAt(p,null,true,.6),visible:!!hit&&hit.point.distanceTo(p)<.2};},
  projectPoint:(x,z,above=0)=>{const r=renderer.domElement.getBoundingClientRect(),v=new THREE.Vector3(x,groundY(x,z)+above,z).project(camera);return {x:r.left+(v.x+1)*r.width/2,y:r.top+(1-v.y)*r.height/2};},
  inspect:()=>({enemies:enemies.map(e=>({kind:e.kind,hp:e.hp,max:e.max,slowUntil:e.slowUntil,armor:e.armor,siege:e.siege})),units:towers.map(t=>({state:t.mesh.userData.state,bowRunning:!!t.mesh.userData.character?.userData.odinBow?.userData.wasRunning,detouring:!!t.detouring,yielding:!!t.yielding,resumePending:!!t.resumeDestination,trafficHistory:t.trafficHistory||[]})),simTime,quality})''')
replace('  updateCastleBar();\n  // Ein vom Spieler',"  updateCastleBar();\n  if(paused||runEnded)return;simTime+=dt;clearRoadPriority();\n  // Ein vom Spieler")
replace("    t.didMoveThisFrame=Boolean(t.moveRoute?.length);\n    if(t.didMoveThisFrame){\n      moveTowerStep(t,dt);\n      animateUnit(t.mesh,'run',tNow,dt);\n    }", "    t.didMoveThisFrame=Boolean(t.moveRoute?.length);\n    if(t.didMoveThisFrame){\n      const moved=moveTowerStep(t,dt);animateUnit(t.mesh,moved?'run':'idle',tNow,dt);\n    }")
replace('spawned<Math.min(8+wave*3,45)','spawned<waveTarget')
replace("        spawn();\n        spawned++;\n        spawnTimer=Math.max(.55,1.0-wave*.012+Math.random()*.5);", "        if(spawn())spawned++;\n        spawnTimer=Math.max(.62,1.18-wave*.025);")
section('    if(spawned>=Math.min(8+wave*3,45)','  for(let e of [...enemies])',"    if(spawned>=waveTarget&&!enemies.length)waveVictory();\n  }\n\n")
replace('    let remaining=e.siege?0:dt*e.speed;', '    const oldIndex=e.index,oldT=e.t;\n    let remaining=e.siege?0:dt*e.speed*(e.slowUntil>simTime?(e.slowFactor||1):1);')
replace('    // Small stagger in each branch:', '    if(!e.siege&&queueLeaderAhead(e))remaining=0;\n    // Small stagger in each branch:')
replace('    // Stop at the gate: do not walk through the castle or disappear on arrival.',r'''    if(!e.siege){
      const a=e.route[e.index],b=e.route[Math.min(e.index+1,e.route.length-1)],next=a.clone().lerp(b,e.t);next.y=groundY(next.x,next.z)+.02;
      const occupants=[...enemies.filter(o=>o!==e),...towers];
      const blocked=occupants.some(o=>Math.abs(o.mesh.position.y-next.y)<.65&&Math.hypot(o.mesh.position.x-next.x,o.mesh.position.z-next.z)<.40&&Math.hypot(o.mesh.position.x-next.x,o.mesh.position.z-next.z)<Math.hypot(o.mesh.position.x-e.mesh.position.x,o.mesh.position.z-e.mesh.position.z)-.0001);
      if(blocked){e.index=oldIndex;e.t=oldT;}
    }
    // Stop at the gate: do not walk through the castle or disappear on arrival.''')
replace('        e.siegeSlot=arrivedAtCastle++ % 5;',r'''        const slot=[0,1,2,3,4].find(n=>!enemies.some(o=>o!==e&&o.siege&&o.siegeSlot===n));
        if(slot===undefined){e.siege=false;e.index=oldIndex;e.t=oldT;continue;}
        e.siegeSlot=slot;arrivedAtCastle++;''')
replace('const lane=(e.siegeSlot-2)*.12;','const lane=(e.siegeSlot-2)*.44;')
replace('Math.floor(e.siegeSlot/2)*.12','Math.floor(e.siegeSlot/3)*.42')
replace('hp=Math.max(0,hp-1);ui();sound(\'hit\');',"hp=Math.max(0,hp-e.castleDamage);ui();sound('hit');")
replace("            active=false;\n            notify('Die Barbaren haben das Burgtor zerstört!');", "            finishRun();notify('Die Burg ist gefallen. Odin vergisst deinen Mut nicht.');return;")
replace('    e.mesh.rotation.y=Math.atan2(b.x-a.x,b.z-a.z);', '    const yaw=Math.atan2(b.x-a.x,b.z-a.z),turn=Math.atan2(Math.sin(yaw-e.mesh.rotation.y),Math.cos(yaw-e.mesh.rotation.y));e.mesh.rotation.y+=turn*Math.min(1,dt*12);')
section("        s.victim.hp=Math.max(0,s.victim.hp-s.damage);",'      }\n      scene.remove(s.mesh);shots.splice',r'''        const center=s.victim.mesh.position.clone();damageEnemy(s.victim,s.damage,s.type);
        if(s.type==='knight')for(const other of [...enemies])if(other!==s.victim&&other.mesh.position.distanceTo(center)<.8)damageEnemy(other,Math.round(s.damage*.55),'splash');
''')
enhance=root.joinpath('experience.js').read_text()+'\n'+root.joinpath('traffic.js').read_text()
replace('let last=performance.now();function loop(now){',enhance+'\nlet last=performance.now();function loop(now){')
replace('last=now;\n  try{update(dt);}', 'last=now;dt*=gameSpeed;\n  try{update(dt);mobileTick();}')
replace("camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight)","resizeStage(true)")
a.destination.parent.mkdir(parents=True,exist_ok=True)
s=s.replace('87-mobile-saga','88-mobile-saga').replace('Mobile Saga V87','Mobile Saga V88').replace('Mobile Saga · V87','Mobile Saga · V88')
a.destination.write_text(s)
manifest={'version':'88-mobile-saga','source_sha256':hashlib.sha256(source.encode()).hexdigest(),'predecessor_sha256':'814bcc48b9eb060fbc4a5ec528f11bee262e887f6e66e2220232d898594e128e','candidate_sha256':hashlib.sha256(s.encode()).hexdigest(),'live_published':False}
a.destination.with_name('build.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest))
