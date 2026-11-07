
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
const canvas=document.getElementById('canvas'),panel=document.getElementById('viewport');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,powerPreference:'high-performance'});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;
const scene=new THREE.Scene();scene.background=new THREE.Color('#101927');
scene.add(new THREE.HemisphereLight(0xcddff9,0x29313c,2));
const sun=new THREE.DirectionalLight(0xffe4b9,3.4);sun.position.set(3,7,5);sun.castShadow=true;sun.shadow.mapSize.set(1024,1024);scene.add(sun);
const ground=new THREE.Mesh(new THREE.CircleGeometry(24,64),new THREE.MeshStandardMaterial({color:0x223644,roughness:1}));ground.rotation.x=-Math.PI/2;ground.receiveShadow=true;ground.position.y=-.03;scene.add(ground);
const grid=new THREE.GridHelper(20,20,0x4a647b,0x233548);scene.add(grid);
const camera=new THREE.PerspectiveCamera(38,1,.05,300);camera.position.set(4,3,6);
const controls=new OrbitControls(camera,canvas);controls.enableDamping=true;controls.target.set(0,1,0);controls.maxPolarAngle=Math.PI*.91;
const clock=new THREE.Clock();let model=null,mixer=null,actions=[],current=null,paused=false,objectUrl=null;
const status=document.getElementById('status');const animationSelect=document.getElementById('animations');
function resize(){const w=panel.clientWidth,h=panel.clientHeight;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix()}new ResizeObserver(resize).observe(panel);resize();
function view(name){const r=model?Math.max(3,model.userData.radius*2.6):5;const c=controls.target;const offsets={front:[0,r*.35,r],side:[r,r*.32,0],back:[0,r*.35,-r],iso:[r*.75,r*.65,r*.75]};const o=offsets[name]||offsets.iso;camera.position.set(c.x+o[0],c.y+o[1],c.z+o[2]);controls.update()}
for(const b of document.querySelectorAll('[data-view]'))b.onclick=()=>view(b.dataset.view);
function play(index){if(!mixer||!actions[index])return;const next=actions[index];if(current&&next!==current)current.fadeOut(.18);next.reset().fadeIn(.18).play();current=next;status.textContent='Animation: '+next.getClip().name}
animationSelect.onchange=()=>play(Number(animationSelect.value));
document.getElementById('speed').oninput=e=>{const v=Number(e.target.value);document.getElementById('speedValue').textContent=v.toFixed(1)+'×';if(mixer)mixer.timeScale=v};
document.getElementById('pause').onclick=()=>{paused=!paused;document.getElementById('pause').textContent=paused?'Animation fortsetzen':'Animation pausieren'};
async function openGLB(file){if(!file)return;status.textContent='Lade '+file.name+' …';if(model){scene.remove(model);model.traverse(o=>{if(o.geometry)o.geometry.dispose();if(o.material){for(const m of (Array.isArray(o.material)?o.material:[o.material]))m.dispose()}})}if(objectUrl)URL.revokeObjectURL(objectUrl);model=null;mixer=null;actions=[];animationSelect.disabled=true;
objectUrl=URL.createObjectURL(file);
new GLTFLoader().load(objectUrl,gltf=>{model=gltf.scene;scene.add(model);model.traverse(o=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=true}});
const box=new THREE.Box3().setFromObject(model),center=box.getCenter(new THREE.Vector3()),size=box.getSize(new THREE.Vector3());
model.position.sub(new THREE.Vector3(center.x,box.min.y,center.z));controls.target.set(0,Math.max(.4,size.y*.5),0);model.userData.radius=Math.max(size.x,size.y,size.z);camera.near=.05;camera.far=Math.max(100,model.userData.radius*20);camera.updateProjectionMatrix();view('iso');
mixer=new THREE.AnimationMixer(model);actions=gltf.animations.map(c=>mixer.clipAction(c));animationSelect.innerHTML='';gltf.animations.forEach((clip,i)=>{const opt=document.createElement('option');opt.value=i;opt.textContent=clip.name;animationSelect.appendChild(opt)});animationSelect.disabled=!actions.length;
if(actions.length)play(0);else status.textContent='Modell geladen – keine Animationen vorhanden';
document.getElementById('details').textContent=`${file.name} · ${THREE.MathUtils.roundTo(file.size/1024,1)} KiB · ${actions.length} Animation(en)`;
},undefined,error=>{status.textContent='GLB-Ladefehler: '+error.message;console.error(error)});
}
document.getElementById('glb').onchange=e=>openGLB(e.target.files[0]);
panel.addEventListener('dragover',e=>e.preventDefault());panel.addEventListener('drop',e=>{e.preventDefault();openGLB(e.dataTransfer.files[0])});
function animate(){requestAnimationFrame(animate);const dt=Math.min(clock.getDelta(),.1);if(mixer&&!paused)mixer.update(dt);controls.update();renderer.render(scene,camera)}animate();

// Load the adjacent generated model when hosted over HTTP; preserve local file picker.
if(location.protocol !== 'file:') {
  fetch('./asset-manifest.json', {cache:'no-store'}).then(r => r.ok ? r.json() : null).then(async manifest => {
    if(!manifest?.model)return;
    const resp=await fetch('./'+encodeURIComponent(manifest.model));
    if(!resp.ok)throw new Error('Beispielmodell nicht gefunden');
    const blob=await resp.blob();
    await openGLB(new File([blob],manifest.model,{type:'model/gltf-binary'}));
  }).catch(e=>{status.textContent='Beispielmodell: '+e.message+' – GLB manuell wählen';});
}
