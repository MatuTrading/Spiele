import assert from 'node:assert/strict';
import {boneStem,layerForTrack,buildRangerRunLayers} from '../animation_layers.mjs';
for(const s of ['upperleg.l.quaternion','upperlegl.quaternion','upperleg_r.rotation','.bones[upperleg.r].quaternion'])assert.equal(boneStem(s),'upperleg');
assert.equal(layerForTrack('foot.l.position'),'lower');
assert.equal(layerForTrack('spine.quaternion'),'upper');
assert.equal(layerForTrack('root.position'),'other');
class Clip{constructor(name,duration,tracks){Object.assign(this,{name,duration,tracks})}}
const make=n=>({name:n,clone(){return make(n)}});
const a=new Clip('run',1,['foot.l.quaternion','spine.quaternion'].map(make)),b=new Clip('bow',1,['foot.l.quaternion','hand.l.quaternion'].map(make));
const r=buildRangerRunLayers({AnimationClip:Clip},a,b);
assert.deepEqual(r.legs.tracks.map(t=>t.name),['foot.l.quaternion']);
assert.deepEqual(r.torso.tracks.map(t=>t.name),['hand.l.quaternion']);
assert.equal(a.tracks.length,2);
console.log('PASS animation masks');
