const STORAGE_KEY='odin-forge-v15-draft';
let history=[],historyIndex=-1,historyTimer=0,restoring=false;
function rememberSoon(){if(!window.__odinReady||restoring)return;clearTimeout(historyTimer);historyTimer=setTimeout(captureHistory,220)}
function captureHistory(){
 if(!window.__odinReady||restoring||currentlyBuilding)return;
 const snapshot=JSON.stringify(buildRecipe());
 if(history[historyIndex]!==snapshot){history=history.slice(0,historyIndex+1);history.push(snapshot);if(history.length>50)history.shift();historyIndex=history.length-1}
 syncHistory();
 try{localStorage.setItem(STORAGE_KEY,snapshot);$('saveState').textContent='Entwurf gesichert'}catch(e){$('saveState').textContent='Nur für diese Sitzung';$('saveState').title='Automatisches Speichern ist in diesem Browser nicht verfügbar.'}
 document.querySelectorAll('[data-preset]').forEach(b=>{const active=b.dataset.preset===selectedPreset;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active))});
}
function syncHistory(){$('undo').disabled=historyIndex<1;$('redo').disabled=historyIndex>=history.length-1}
async function travelHistory(direction){
 clearTimeout(historyTimer);captureHistory();const next=historyIndex+direction;if(next<0||next>=history.length||restoring)return;
 restoring=true;
 try{await applyRecipe(JSON.parse(history[next]));historyIndex=next;try{localStorage.setItem(STORAGE_KEY,history[next])}catch{}feedback(direction<0?'Änderung rückgängig gemacht.':'Änderung wiederholt.','success')}
 catch(e){feedback('Entwurf konnte nicht wiederhergestellt werden: '+e.message,'error')}
 finally{restoring=false;syncHistory()}
}
function filterAnimations(preferred=$('animation').value){
 const query=$('animationSearch').value.trim().toLowerCase();
 const filtered=allClips.filter(c=>c.name.toLowerCase().includes(query));
 const select=$('animation');select.replaceChildren();
 for(const clip of filtered)select.add(new Option(clip.name,clip.name));
 // Filtering is navigation, and must not change the currently playing clip.
 if(preferred&&!filtered.some(c=>c.name===preferred)){const active=allClips.find(c=>c.name===preferred);if(active)select.add(new Option(active.name+' · aktiv',active.name))}
 if(preferred&&[...select.options].some(o=>o.value===preferred))select.value=preferred;
 $('animationCount').textContent=`(${filtered.length} / ${allClips.length})`;
}
function setMobilePage(page){
 document.querySelector('.shell').dataset.page=page;
 document.querySelectorAll('button[data-page]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.page===page)));
}
function initWorkshop(){
 $('feedback').title='Hinweise zur aktuellen Figur';
 for(const b of document.querySelectorAll('button[data-page]'))b.addEventListener('click',()=>setMobilePage(b.dataset.page));
 setMobilePage('figure');
 $('undo').addEventListener('click',()=>travelHistory(-1));$('redo').addEventListener('click',()=>travelHistory(1));
 document.addEventListener('keydown',e=>{
  const edit=e.target.matches('input,textarea,select,[contenteditable=true]');if(edit)return;
  if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='z'){e.preventDefault();travelHistory(e.shiftKey?1:-1)}
  if(e.code==='Space'&&!e.ctrlKey&&!e.metaKey){e.preventDefault();$(isPlaying?'pause':'play').click()}
 });
 $('charName').addEventListener('input',()=>{if(currentModel){const name=$('charName').value.trim()||'Odin_Modular_Character';currentModel.name=name;$('namePreview').textContent=name}rememberSoon()});
 document.addEventListener('change',e=>{if(e.target.matches('input,select')&&e.target.id!=='loadRecipe')rememberSoon()});
 $('animationSearch').addEventListener('input',()=>filterAnimations());
 $('timeline').addEventListener('input',()=>{
  if(!currentAction||!currentClip)return;
  isPlaying=false;currentMixer.timeScale=0;currentAction.time=Math.min(Math.max(0,currentClip.duration-0.000001),Number($('timeline').value)/1000*currentClip.duration);currentMixer.update(0);
  $('timeText').textContent=currentAction.time.toFixed(2)+' s';$('pause').setAttribute('aria-pressed','true');$('play').setAttribute('aria-pressed','false');
 });
 for(const id of ['play','pause'])$(id).addEventListener('click',()=>{for(const b of ['play','pause'])$(b).setAttribute('aria-pressed',String(b===id))});
 $('play').setAttribute('aria-pressed','true');$('pause').setAttribute('aria-pressed','false');
 $('rotate').addEventListener('click',()=>{orbit.autoRotate=!orbit.autoRotate;orbit.autoRotateSpeed=1.4;$('rotate').setAttribute('aria-pressed',String(orbit.autoRotate))});
 $('gridToggle').addEventListener('click',()=>{grid.visible=!grid.visible;$('gridToggle').setAttribute('aria-pressed',String(grid.visible))});
 document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>{
  const distance=5.8;orbit.target.set(0,1.12,0);orbit.autoRotate=false;$('rotate').setAttribute('aria-pressed','false');
  const positions={front:[0,1.6,distance],side:[distance,1.6,0],back:[0,1.6,-distance]};camera.position.set(...positions[b.dataset.view]);orbit.update();
 }));
 $('quality').addEventListener('change',()=>{const quality=$('quality').value;renderer.setPixelRatio(quality==='low'?1:Math.min(devicePixelRatio,quality==='high'?2:1.65));renderer.shadowMap.enabled=quality!=='low';renderer.shadowMap.needsUpdate=true;resize()});
 $('screenshot').addEventListener('click',()=>{renderer.render(scene,camera);renderer.domElement.toBlob(blob=>{if(blob)saveBlob(blob,($('charName').value||'Odin_Charakter').replace(/[^a-z0-9_-]/gi,'_')+'.png')},'image/png')});
 $('downloadAll').addEventListener('click',async()=>{if(currentlyBuilding)return;$('downloadAll').disabled=true;try{await exportGLB('all')}catch(e){status('Export fehlgeschlagen: '+e.message,'error')}finally{$('downloadAll').disabled=false}});
 $('fileInputLabel').addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();$('loadRecipe').click()}});
 addEventListener('pagehide',()=>{clearTimeout(historyTimer);captureHistory()});
 renderer.domElement.addEventListener('webglcontextlost',e=>{e.preventDefault();feedback('3D-Darstellung unterbrochen. Bitte lade die Seite neu; dein Entwurf bleibt gespeichert.','error')});
}
// Read-only diagnostics for repeatable QA against the visible, assembled model.
window.__odinDiagnostics=()=>{
 const box=new THREE.Box3();let finite=true,vertices=0;currentModel?.updateMatrixWorld(true);
 currentModel?.traverse(o=>{if(!o.isMesh)return;const positions=o.geometry.attributes.position;for(let i=0;i<positions.count;i++){const v=new THREE.Vector3().fromBufferAttribute(positions,i);if(o.isSkinnedMesh)o.applyBoneTransform(i,v);v.applyMatrix4(o.matrixWorld);vertices++;if(!Number.isFinite(v.x+v.y+v.z))finite=false;else box.expandByPoint(v)}});
 return {finite,vertices,bounds:{min:box.min.toArray(),max:box.max.toArray()},clip:currentClip?.name,time:currentAction?.time,playing:isPlaying,renderer:{geometries:renderer.info.memory.geometries,textures:renderer.info.memory.textures}};
};
