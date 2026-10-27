from pathlib import Path
import re,sys
src=Path(sys.argv[1]).read_text()
s=src.replace('KayKit Charakter-Baukasten V14','Character Forge V15')
slots=re.search(r'<div class="slotgrid">(.*?)</div></div><p class="color-help">',s,re.S).group(1)+'</div>'
options=re.search(r'<select id="categoryPreset".*?>(.*?)</select>',s,re.S).group(1)
presets=re.search(r'<div class="presetgrid">(.*?)</div><div class="sectiontitle">2',s,re.S).group(1)
body='''<body><div class="shell"><header class="top"><div class="brand"><div class="sigil">O</div><div><h1>ODIN <span>CHARACTER FORGE</span></h1><p>Deine Helden. Dein Stil. <span class="version">V15 · Offline</span></p></div></div><div class="historybar"><button class="tool" id="undo" disabled aria-label="Rückgängig" title="Rückgängig (Strg+Z)">↶</button><button class="tool" id="redo" disabled aria-label="Wiederholen" title="Wiederholen (Strg+Umschalt+Z)">↷</button><span id="saveState" role="status">Startet …</span></div></header>
<main class="layout"><aside class="pane left"><section data-panel="figure"><div class="sectiontitle">01 / Dein Charakter</div><label for="charName">Figurenname</label><input id="charName" type="text" value="Odin_Waldlaeufer" maxlength="100" autocomplete="off"><div class="category-wrap"><label for="categoryPreset">Startfigur auswählen</label><select id="categoryPreset">OPTIONS</select><p class="familyNote">Wähle eine Vorlage und passe danach jedes Teil an.</p></div><div class="sectiontitle">Schnellvorlagen</div><div class="presetgrid">PRESETS</div><button class="sub" id="shuffle">Neue Kombination würfeln</button><details class="promptBox"><summary>Figur mit Text zusammenstellen</summary><p class="smallText">Lokale Befehle wählen vorhandene Teile aus.</p><textarea id="prompt" placeholder="Kopf vom Ritter, Torso vom Magier, Arme vom Ranger, Beine vom Rogue"></textarea><button class="primary" id="createPrompt">Beschreibung anwenden</button></details></section>
<section data-panel="parts"><div class="sectiontitle">02 / Bauteile &amp; Farben</div><label for="family">Körperfamilie</label><select id="family"><option value="living">Menschliche Figuren</option><option value="skeleton">Skelett-Figuren</option></select><p class="familyNote">Teile innerhalb einer Familie frei kombinieren.</p><div class="slotgrid">SLOTS</div><p class="color-help">0 % erhält die Originaloberfläche. 100 % färbt das ganze Bauteil ein, einschließlich Haut und Kleidung.</p><button class="sub" id="resetColors">Originalfarben wiederherstellen</button></section></aside>
<section class="center" aria-label="3D-Vorschau"><div id="stage" class="stage"><div class="corner"><strong id="namePreview">Dein Held entsteht …</strong><span id="presetName">Originale KayKit-Komponenten</span></div><div class="viewTools" aria-label="Kamera"><button class="tool" data-view="front" title="Vorderansicht">Vorn</button><button class="tool" data-view="side" title="Seitenansicht">Seite</button><button class="tool" data-view="back" title="Rückansicht">Hinten</button><button class="tool" id="resetView" title="Kamera zurücksetzen">↺</button></div><div class="stageOptions"><button class="tool" id="rotate" aria-pressed="false">360°</button><button class="tool" id="gridToggle" aria-pressed="true">Raster</button><button class="tool" id="screenshot">Bild</button></div><div class="hint">Ziehen zum Drehen · Zwei Finger zum Verschieben und Zoomen</div><div id="loading" role="status">Die Schmiede wird vorbereitet …</div></div><div class="infoBar"><span class="mini" id="partsCount">Lade Teile …</span><span class="mini" id="rigCount">23 Bones</span><span class="mini" id="familyPill">Menschlich</span><span class="mini" id="activeAnimation">Idle_A</span></div><div id="feedback" role="status" aria-live="polite">Lade deine Werkstatt …</div></section>
<aside class="pane right"><section data-panel="motion"><div class="sectiontitle">03 / Bewegung</div><label for="animationSearch">Animation suchen</label><input type="search" id="animationSearch" placeholder="z. B. Walk, Sword, Idle"><label for="animation">Animation <span id="animationCount"></span></label><select id="animation"></select><div class="btnRow"><button class="sub" id="play">Abspielen</button><button class="sub" id="pause">Pause</button></div><label for="timeline">Animationsposition <span id="timeText">0.00 s</span></label><input type="range" id="timeline" min="0" max="1000" value="0" step="1"><label for="speed">Tempo <span id="speedText">1.0×</span></label><input id="speed" type="range" min="10" max="200" value="100" step="10"><p class="smallText">Die Zeitleiste pausiert die Bewegung zur genauen Ansicht. Waffen sind in dieser Version nicht enthalten.</p><label for="quality">Darstellungsqualität</label><select id="quality"><option value="auto">Automatisch</option><option value="high">Hoch</option><option value="low">Sparsam</option></select></section>
<section data-panel="export"><div class="sectiontitle">04 / Bereit fürs Spiel</div><p>Deine Figur als 3D-Datei mit gemeinsamem KayKit-Skelett.</p><button class="primary" id="download" disabled>GLB · Modell</button><button class="sub" id="downloadAnim" disabled>GLB · aktuelle Animation</button><button class="sub" id="downloadAll" disabled>GLB · alle Animationen</button><button class="sub" id="selfCheck">Export und Reimport prüfen</button><p id="status" role="status">Initialisiere die 3D-Vorschau …</p><div class="divider"></div><button class="sub" id="saveRecipe">Bauplan speichern (.json)</button><label id="fileInputLabel" for="loadRecipe" tabindex="0">Bauplan laden (.json)</label><input type="file" id="loadRecipe" accept=".json,application/json"><p class="smallText">Der letzte Entwurf wird auf diesem Gerät automatisch gespeichert. Mit dem Bauplan kannst du ihn auf ein anderes Gerät übertragen.</p><div class="divider"></div><details><summary>Über die Bauteile</summary><p><span id="totalParts">0</span> Originalteile aus 10 KayKit-Figuren · <span id="totalAnimations">0</span> Animationen.</p><p id="readyNote">Modelle werden aus dieser Datei geladen.</p><p class="smallText">KayKit-Bauteile und Animationen bleiben erhalten. Textbefehle kombinieren vorhandene Modelle; neue 3D-Geometrie wird nicht durch eine KI erzeugt.</p></details></section></aside></main><nav class="mobileNav" aria-label="Werkstattbereiche"><button data-page="figure" aria-pressed="true">Figur</button><button data-page="parts" aria-pressed="false">Bauteile</button><button data-page="motion" aria-pressed="false">Bewegung</button><button data-page="export" aria-pressed="false">Export</button></nav></div>'''.replace('OPTIONS',options).replace('PRESETS',presets).replace('SLOTS',slots)
s=s[:s.index('<body>')]+body+s[s.index('<script id="asset-data"'):]
for icon in ['🏹 ','🛡 ','✦ ','⚔ ','🌲 ','☠ ','♜ ','◆ ','✎ ']:s=s.replace(icon,'')
css='''
/* V15: a persistent preview and independently scrollable work areas. */
:root{font-family:Inter,ui-sans-serif,system-ui,sans-serif;--gold:#dfb77e;--line:#334250}
body{overflow:hidden;background:#0c1420}.shell{height:100vh;height:100dvh;min-height:0;grid-template-rows:70px minmax(0,1fr)}
.top{padding:10px 20px;background:#111d2a}.top h1{font-size:18px;letter-spacing:2px}.top h1 span{font-size:12px;letter-spacing:1.5px;color:#d8c19f;margin-left:6px}.top p{font-size:11px}.sigil{font-family:Georgia,serif;border:1px solid #d9b981;background:transparent;color:#e4bd82;border-radius:50%;font-size:25px}.version{margin-left:10px;color:#b9a37e}
.layout{display:grid;grid-template-columns:320px minmax(280px,1fr) 280px;overflow:hidden}.pane{padding:18px;background:#111d2a;scrollbar-width:thin;scrollbar-color:#4b5b6b transparent;min-height:0;overscroll-behavior:contain}.right{display:block;border-top:0;grid-column:auto}.sectiontitle{margin-top:22px;font-size:10px;letter-spacing:1.8px;color:#dcbd8f}.sectiontitle:first-child{margin-top:0}section[data-panel]+section[data-panel]{margin-top:24px;border-top:1px solid #304052;padding-top:22px}
input[type=search]{width:100%;font:inherit;font-size:13px;padding:11px;color:#eef4fd;border:1px solid #35475e;background:#1d2d41;border-radius:8px;margin-bottom:12px}
input[type=range]{width:100%;accent-color:#dfb77e;min-height:28px;cursor:pointer}label{margin-top:10px}.partControl{padding:10px}.partControl .partHeader label{margin:0}.partControl select{min-height:42px}.partControl .slideLabels{font-size:10px}.partControl input[type=color]{height:40px}.category-wrap{margin-top:15px;background:#192b3c}.category-wrap label{margin-top:0}button.preset{min-height:44px;font-size:12px}button.preset.active{border-color:#dfb77e;background:#3d382f;color:#ffe1b0}.presetgrid{margin-bottom:12px}.promptBox{margin-top:15px;padding-top:13px;border-top:1px solid #304052}summary{font-size:12px;cursor:pointer;color:#dac3a3;padding:6px 0}.promptBox textarea{margin:10px 0}.right .sub,.right .primary{margin-top:8px;font-size:12px;min-height:42px}.btnRow{margin:8px 0 16px}button.primary{background:#e1ba81;color:#171d26}.center{background:radial-gradient(ellipse at 50% 40%,#25354a,#0b1421);min-width:0;min-height:0}.stage{height:auto;min-height:0;flex:1}.corner{max-width:calc(100% - 25px)}.corner strong{max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.stage .corner{top:18px}.stage .corner strong{font-size:15px}.stage .hint{bottom:54px;font-size:10px;max-width:calc(100% - 24px);white-space:normal;text-align:center;padding:7px 10px}.viewTools{position:absolute;bottom:12px;left:12px;display:flex;gap:5px}.stageOptions{position:absolute;bottom:12px;right:12px;display:flex;gap:5px}.tool{border:1px solid #4b5b6d;background:#132338e8;color:#d9e5f2;border-radius:7px;min-height:34px;padding:6px 10px;font-size:11px}.tool:hover,.tool[aria-pressed=true]{background:#66503a;color:#ffe0ad}.tool:focus-visible,button:focus-visible,summary:focus-visible,#fileInputLabel:focus-visible{outline:2px solid #f1c68c;outline-offset:3px}.historybar{display:flex;align-items:center;gap:6px}.historybar .tool{font-size:20px;min-width:35px;padding:0}#saveState{font-size:10px;color:#9eafba;max-width:140px;margin-left:5px}.infoBar{padding:9px 12px;gap:6px}.mini{font-size:10px;padding:5px 8px;border-radius:5px;background:#1d3045}#feedback{margin:0;border-radius:0;border:0;border-top:1px solid #304052;padding:9px 14px;min-height:36px;font-size:11px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;background:#122333}#feedback[data-kind=error]{white-space:normal}.mobileNav{display:none}#loading{position:absolute;inset:0;background:#111c2ced;display:grid;place-content:center;text-align:center;color:#dfb77e;font-size:13px;padding:30px;z-index:3}#loading[hidden]{display:none}#fileInputLabel{margin-top:12px}#loadRecipe{display:none}
@media(min-width:721px) and (max-width:1100px){.layout{grid-template-columns:240px minmax(220px,1fr) 220px}.pane{padding:12px}.top h1 span{font-size:10px}.stageOptions #gridToggle{display:none}.stageOptions{bottom:54px}.stage .hint{display:none}}
@media(max-width:720px), (max-width:950px) and (max-height:500px){.shell{grid-template-rows:58px minmax(0,1fr) 55px}.top{padding:6px 12px}.top h1{font-size:14px;letter-spacing:1px}.top h1 span{display:block;margin:2px 0 0;font-size:9px}.top p{display:none}.sigil{width:31px;height:31px;font-size:22px}.historybar{gap:4px}#saveState{display:none}.layout{display:grid;grid-template-columns:1fr;grid-template-rows:minmax(205px,43%) minmax(0,1fr)}.center{grid-row:1;height:auto;order:0;border-bottom:1px solid #3b4b5d}.pane{grid-row:2;grid-column:1;padding:13px 14px;border:0;overflow:auto}.left{order:0}.right{display:none}.stage{height:auto;min-height:0}.stage .corner{top:10px;left:12px}.stage .corner strong{font-size:12px}.stage .corner span{font-size:9px}.stage .hint{display:none}.viewTools{left:8px;bottom:8px;gap:4px}.stageOptions{right:8px;bottom:8px;gap:4px}.tool{padding:4px 8px;min-height:32px;font-size:10px}.infoBar{padding:5px 8px;flex-wrap:nowrap;overflow:hidden}.mini{white-space:nowrap;font-size:9px;padding:4px 6px}#rigCount{display:none}#feedback{min-height:28px;padding:6px 10px;font-size:10px}.mobileNav{display:grid;grid-template-columns:repeat(4,1fr);background:#111d2a;border-top:1px solid #3b4b5d;padding-bottom:env(safe-area-inset-bottom)}.mobileNav button{background:none;border:0;border-top:2px solid transparent;color:#a5b6c8;font-size:11px;font-weight:700}.mobileNav button[aria-pressed=true]{color:#f2cc93;background:#26313b;border-top-color:#dfb77e}.left [data-panel=parts]{display:none}.shell[data-page=parts] .left [data-panel=figure]{display:none}.shell[data-page=parts] .left [data-panel=parts]{display:block;border:0;padding:0;margin:0}.shell[data-page=motion] .left,.shell[data-page=export] .left{display:none}.shell[data-page=motion] .right,.shell[data-page=export] .right{display:block}.shell[data-page=motion] [data-panel=export],.shell[data-page=export] [data-panel=motion]{display:none}.shell[data-page=export] [data-panel=export]{margin:0;padding:0;border:0}button,input,select{touch-action:manipulation}input[type=text],input[type=search],textarea,select{font-size:16px}.partControl select{font-size:14px}.partControl input[type=range]{min-height:32px}.btnRow .sub{margin:0}.partControl{margin-top:10px}}
@media(max-width:950px) and (max-height:500px){.layout{grid-template-columns:48% 52%;grid-template-rows:1fr}.center{grid-row:1;grid-column:1}.pane{grid-column:2;grid-row:1}.infoBar,#feedback,.stageOptions{display:none}.viewTools{left:5px;right:5px;justify-content:center}.stage .corner span{display:none}.shell{grid-template-rows:48px minmax(0,1fr) 43px}}
'''
s=s.replace('</style>',css+'</style>',1)
# Shadow acne on the original meshes, especially faces and hair.
s=s.replace('mainLight.castShadow=true;','mainLight.castShadow=true;mainLight.shadow.normalBias=0.035;mainLight.shadow.bias=-0.00015;')
s=s.replace('preserveDrawingBuffer:true','preserveDrawingBuffer:false')
s=s.replace("orbit.minDistance=2.5;", "orbit.minDistance=1.7;")
s=s.replace("$('partsCount').textContent=`${assembled.length} originale Komponenten`;", "$('partsCount').textContent=`${assembled.length} Bauteile`;")
s=s.replace("if(resetCamera)resetView();", "if(resetCamera)resetView();\n  rememberSoon();")
s=s.replace("const old=currentModel;", "const old=currentModel;const previousTime=currentAction?.time||0;")
s=s.replace("setAnimation($('animation').value);\n  if(resetCamera)", "setAnimation($('animation').value);if(currentAction&&currentClip){currentAction.time=previousTime%currentClip.duration;currentMixer.update(0)}\n  if(resetCamera)")
# Keep a skinned model in bind pose when exporting; selected animation is separately embedded.
a=s.index('async function exportGLB(animated)');b=s.index('function parsePrompt(text)',a)
s=s[:a]+'''function exportRoot(){
 const root=cloneSkinned(currentModel);root.name=$('charName').value.trim()||'Odin_Modular_Character';
 root.traverse(o=>{if(o.isSkinnedMesh)o.pose();o.userData=o.isMesh?{odinSlot:o.userData.odinSlot,odinSource:o.userData.odinSource}:{}});root.updateMatrixWorld(true);return root;
}
async function exportGLB(animated){
 if(!currentModel)throw Error('Kein Modell geladen');
 const root=exportRoot();
 const animations=animated==='all'?allClips:(animated&&currentClip?[currentClip]:[]);
 const buffer=await new GLTFExporter().parseAsync(root,{binary:true,trs:true,onlyVisible:true,animations});
 lastExport=buffer;
 const fileName=root.name.replace(/[^a-z0-9_-]/gi,'_')+(animated==='all'?'_alle_Animationen':animated?'_anim':'')+'.glb';
 saveBlob(new Blob([buffer],{type:'model/gltf-binary'}),fileName);
 status(`${fileName} exportiert (${Math.round(buffer.byteLength/1024)} KB)`,'ok');return buffer;
}
async function roundtripTest(animated){
 const root=exportRoot();
 const clips=animated==='all'?allClips:(animated&&currentClip?[currentClip]:[]);
 const buffer=await new GLTFExporter().parseAsync(root,{binary:true,trs:true,onlyVisible:true,animations:clips});
 const parsed=await new Promise((resolve,reject)=>loader.parse(buffer,'',resolve,reject));
 let bones=0,skinned=0,meshes=0,finite=true;
 parsed.scene.traverse(o=>{if(o.isBone)bones++;if(o.isMesh){meshes++;if(o.isSkinnedMesh){skinned++;for(let i=0;i<o.geometry.attributes.position.count;i++){const v=new THREE.Vector3().fromBufferAttribute(o.geometry.attributes.position,i);o.applyBoneTransform(i,v);if(!Number.isFinite(v.x+v.y+v.z))finite=false}}}});
 return {ok:meshes>0&&skinned>=6&&bones===23&&finite&&parsed.animations.length===clips.length,bytes:buffer.byteLength,meshes,skinned,bones,finite,animations:parsed.animations.map(c=>c.name)};
}
function buildRecipe(){return {format:'odin-modular-v1',family:selectFamily(),name:$('charName').value,parts:{...selection},animation:$('animation').value,tints:structuredClone(partColors)}}
function validateRecipe(o){
 if(!o||o.format!=='odin-modular-v1'||!['living','skeleton'].includes(o.family)||!o.parts||typeof o.parts!=='object')throw Error('Ungültiges Bauplanformat');
 for(const slot of slots){const name=o.parts[slot];if((slot==='headwear'||slot==='back')&&name==='')continue;const part=meshInfo.get(name);if(!part||part.slot!==slot||part.family!==o.family)throw Error('Unpassendes Bauteil: '+slot);}
 if(o.animation&&!allClips.some(c=>c.name===o.animation))throw Error('Unbekannte Animation');
 for(const slot of slots){const t=o.tints?.[slot];if(t&&(!/^#[0-9a-f]{6}$/i.test(t.color||'')||!Number.isFinite(t.strength)||t.strength<0||t.strength>1))throw Error('Ungültige Teilfarbe: '+slot);}
 return o;
}
async function applyRecipe(o){
 validateRecipe(o);
 $('family').value=o.family;$('charName').value=String(o.name||'Odin_Modular_Character').slice(0,100);
 selection=Object.fromEntries(slots.map(slot=>[slot,o.parts[slot]]));
 for(const slot of slots)partColors[slot]=o.tints?.[slot]?{...o.tints[slot]}:{color:'#ffffff',strength:0};
 $('animationSearch').value='';filterAnimations(o.animation||'Idle_A');
 fillSlotSelectors();markCustom();await buildCharacter();setAnimation($('animation').value);
}
''' +s[b:]
# Restoration should be atomic; file validation completes before any UI change.
s=s.replace("const file=e.target.files[0];if(!file)return;", "const file=e.target.files[0];if(!file)return;if(file.size>200000)throw Error('Bauplan ist zu groß (max. 200 KB)');")
# Replace color multiplication by real per-texture interpolation. A shared atlas may contain skin, cloth and hair.
a=s.index('function applyPartColors(');b=s.index('function requestPartBuild()',a)
s=s[:a]+'''const tintTextures=new Map();
function tintedTexture(map,color,strength){
 if(!map?.image)return null;
 const key=map.uuid+color+strength;
 if(tintTextures.has(key))return tintTextures.get(key);
 const canvas=document.createElement('canvas');canvas.width=map.image.width;canvas.height=map.image.height;
 const ctx=canvas.getContext('2d',{willReadFrequently:true});ctx.drawImage(map.image,0,0);
 const image=ctx.getImageData(0,0,canvas.width,canvas.height),rgb=new THREE.Color(color);
 // ImageData is sRGB; THREE.Color is linear, so convert back for byte interpolation.
 rgb.convertLinearToSRGB();
 for(let i=0;i<image.data.length;i+=4)for(let j=0;j<3;j++)image.data[i+j]=Math.round(image.data[i+j]*(1-strength)+[rgb.r,rgb.g,rgb.b][j]*255*strength);
 ctx.putImageData(image,0,0);const texture=new THREE.CanvasTexture(canvas);
 texture.colorSpace=map.colorSpace;texture.flipY=map.flipY;texture.wrapS=map.wrapS;texture.wrapT=map.wrapT;texture.magFilter=map.magFilter;texture.minFilter=map.minFilter;texture.offset.copy(map.offset);texture.repeat.copy(map.repeat);texture.rotation=map.rotation;texture.center.copy(map.center);
 tintTextures.set(key,texture);
 // Bound the palette cache; live materials keep their textures until next recolor.
 if(tintTextures.size>64){const [oldKey,oldTexture]=tintTextures.entries().next().value;oldTexture.dispose();tintTextures.delete(oldKey)}
 return texture;
}
function applyPartColors(root=currentModel){
 if(!root)return;
 root.traverse(o=>{
  if(!o.isMesh||!o.userData.odinSlot)return;const colors=partColors[o.userData.odinSlot];if(!colors)return;
  const old=originalMaterialFor(o);
  if(o.userData.odinOwnedMats){o.userData.odinOwnedMats.forEach(mat=>mat.dispose());o.userData.odinOwnedMats=null}
  if(colors.strength<=0){o.material=old.length===1?old[0]:old;return;}
  const target=new THREE.Color(colors.color);
  const fresh=old.map(orig=>{const m=orig.clone();if(orig.map){m.map=tintedTexture(orig.map,colors.color,colors.strength);if(m.color)m.color.copy(orig.color)}else if(m.color)m.color.copy(orig.color).lerp(target,colors.strength);return m});
  o.userData.odinOwnedMats=fresh;o.material=fresh.length===1?fresh[0]:fresh;
 });
 if(window.__odinReady)rememberSoon();
}
''' + s[b:]
# More faithful selection labels and source presets.
s=s.replace("$('presetName').textContent=presets[selectedPreset]?.label||'Individuelle Figur';", "$('presetName').textContent=presets[selectedPreset]?.label||(selectedPreset.startsWith('source:')?'Original: '+prettySource(selectedPreset.slice(7)):'Individuelle Figur');")
s=s.replace("selectedPreset='custom';\n  $('charName').value='Odin_'+source;", "selectedPreset=value;\n  $('charName').value='Odin_'+source;")
# Startup locking, autosave restore, camera sizing.
s=s.replace("initUI();", "initUI();initWorkshop();")
s=s.replace("for(const key of characterNames){const gltf=await loadAsset(key);registerParts(key,gltf)}", "for(const [i,key] of characterNames.entries()){const gltf=await loadAsset(key);registerParts(key,gltf);$('loading').textContent=`Lade Figur ${i+1} / ${characterNames.length} …`}")
s=s.replace("window.__odinReady=true;", "window.__odinReady=true;$('loading').hidden=true;$('downloadAll').disabled=false;\n  resetView();filterAnimations($('animation').value);\n  try{const saved=localStorage.getItem(STORAGE_KEY);if(saved){await applyRecipe(JSON.parse(saved));feedback('Dein letzter Entwurf wurde wiederhergestellt.','success')}}catch(e){feedback('Letzter Entwurf konnte nicht geladen werden: '+e.message,'error')}\n  captureHistory();")
s=s.replace("console.error(e);status('Initialisierung fehlgeschlagen:","$('loading').textContent='Die 3D-Vorschau konnte nicht geladen werden. '+e.message;console.error(e);status('Initialisierung fehlgeschlagen:")
s=s.replace("function resetView(){camera.position.set(2.9,2.5,5.15);orbit.target.set(0,1.12,0);orbit.update()}", "function resetView(){const distance=camera.aspect<0.9?6.2:5.8;camera.position.set(distance*.43,2.35,distance*.86);orbit.target.set(0,1.12,0);orbit.update()}")
s=s.replace("if(currentMixer)currentMixer.update(dt);orbit.update();renderer.render(scene,camera)","if(currentMixer&&!document.hidden)currentMixer.update(dt);orbit.update();if(!document.hidden){renderer.render(scene,camera);if(currentClip&&currentAction){$('timeline').value=Math.round((currentAction.time/currentClip.duration)*1000);$('timeText').textContent=currentAction.time.toFixed(2)+' s'}}")
# Extra UI logic lives inside the same module so it acts on the actual scene.
extra=Path(__file__).with_name('workshop.js').read_text()
s=s.replace('initialize();\n</script>',extra+'\ninitialize();\n</script>')
output=Path(__file__).resolve().parents[2]/'Odin_Character_Forge.html';output.write_text(s)
print(output,output.stat().st_size)
