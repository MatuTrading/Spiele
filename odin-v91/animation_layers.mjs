// ODIN V91 – normalized KayKit animation track mask, independent of game source.
export const LOWER=new Set(['hips','upperleg','lowerleg','foot','toes']);
export const UPPER=new Set(['spine','chest','head','neck','upperarm','lowerarm','hand','handslot','wrist','shoulder','clavicle']);
export function boneStem(trackName){
 let s=String(trackName);
 const bracketed=s.match(/\[([^\]]+)\]/);
 if(bracketed)s=bracketed[1];
 else{s=s.replace(/\.(position|quaternion|rotation|scale)$/i,'');s=s.split('/').pop();}
 s=s.replace(/^(?:mixamorig:|rig:)/i,'');
 return s.toLowerCase().replace(/[^a-z0-9]/g,'').replace(/(?:left|right|[lr])$/,'');
}
export function layerForTrack(trackName){
 const stem=boneStem(trackName);
 return LOWER.has(stem)?'lower':UPPER.has(stem)?'upper':'other';
}
export function maskedClip(THREE,src,layer,name){
 if(!src || !Array.isArray(src.tracks) || !['lower','upper'].includes(layer))throw new TypeError('Invalid clip or layer');
 const tracks=src.tracks.filter(t=>layerForTrack(t.name)===layer).map(t=>t.clone());
 if(!tracks.length)throw new Error('No tracks for '+layer);
 return new THREE.AnimationClip(name||src.name+'_ODIN_'+layer,src.duration,tracks);
}
export function buildRangerRunLayers(THREE,run,bowIdle){
 const legs=maskedClip(THREE,run,'lower','ODIN_Run_Lower'),torso=maskedClip(THREE,bowIdle,'upper','ODIN_BowRun_Upper');
 const set=new Set(legs.tracks.map(t=>t.name));
 if(torso.tracks.some(t=>set.has(t.name)))throw new Error('Overlapping skeleton tracks');
 return {legs,torso};
}
