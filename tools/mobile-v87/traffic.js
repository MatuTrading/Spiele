// V88: the authored barbarian lanes have right of way, including at junctions.
// Keep collisions physical. Move a stranded defender to a walkable shoulder;
// never resolve a deadlock by making the barbarians walk through the defender.
const ROAD_SHOULDER=.62;
function nearbyWalkRoute(start,end){
  // Prefer a short, physically walkable connector for nearby destinations.
  // This also avoids joining a road on the wrong side of a scenery obstacle.
  if(Math.hypot(start.x-end.x,start.z-end.z)>3.0)return null;
  const cell=.18,key=(x,z)=>x+','+z,queue=[{x:0,z:0,cost:0,score:start.distanceTo(end)}],visited=new Set(),parent=new Map(),best=new Map([['0,0',0]]),points=new Map([['0,0',start.clone()]]);
  const clear=(from,p)=>Math.abs(from.y-p.y)<=.22&&isLandPoint(p.x,p.z)&&!obstacleAt(p.x,p.z,p.y,.12)&&segmentClear(from,p,.12);
  while(queue.length&&visited.size<700){
    queue.sort((a,b)=>a.score-b.score);const cur=queue.shift(),k=key(cur.x,cur.z);if(visited.has(k))continue;visited.add(k);
    const from=points.get(k);
    if(Math.hypot(from.x-end.x,from.z-end.z)<.27&&clear(from,end)){
      const path=[end.clone()];let cursor=k;while(cursor!=='0,0'){path.push(points.get(cursor).clone());cursor=parent.get(cursor);}return path.reverse();
    }
    for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]){
      const x=cur.x+dx,z=cur.z+dz,nk=key(x,z);if(visited.has(nk)||Math.hypot(x*cell,z*cell)>4)continue;
      const p=new THREE.Vector3(start.x+x*cell,0,start.z+z*cell);p.y=groundY(p.x,p.z);if(!clear(from,p))continue;
      const step=Math.hypot(dx,dz)*cell,cost=cur.cost+step*(pathDistance(p.x,p.z)<.45?1:1.12);
      if(cost>=(best.get(nk)??Infinity))continue;best.set(nk,cost);points.set(nk,p);parent.set(nk,k);
      queue.push({x,z,cost,score:cost+Math.hypot(p.x-end.x,p.z-end.z)});
    }
  }
  return null;
}
function trafficLog(t,event){t.trafficHistory=t.trafficHistory||[];t.trafficHistory.push({event,time:simTime,resume:t.resumeDestination?.toArray()||null,end:t.moveRoute?.at(-1)?.toArray()||null});if(t.trafficHistory.length>10)t.trafficHistory.shift();}
const routeDistances=new WeakMap();
function trafficDistances(route){
  let values=routeDistances.get(route);
  if(!values||values.length!==route.length){values=[0];for(let i=1;i<route.length;i++)values.push(values[i-1]+Math.hypot(route[i].x-route[i-1].x,route[i].z-route[i-1].z));routeDistances.set(route,values);}
  return values;
}
function queueLeaderAhead(enemy){
  const route=enemy.route,prefix=trafficDistances(route),i=Math.min(enemy.index,route.length-2);
  const progress=prefix[i]+(prefix[i+1]-prefix[i])*enemy.t;
  return enemies.some(other=>{
    if(other===enemy||Math.abs(other.mesh.position.y-enemy.mesh.position.y)>.65||other.mesh.position.distanceTo(enemy.mesh.position)>1.3)return false;
    const p=other.mesh.position;let lateral=Infinity,along=0;
    for(let k=Math.max(0,i-2);k<Math.min(route.length-1,i+12);k++){
      const a=route[k],b=route[k+1],dx=b.x-a.x,dz=b.z-a.z,len=dx*dx+dz*dz;
      const t=THREE.MathUtils.clamp(((p.x-a.x)*dx+(p.z-a.z)*dz)/Math.max(.00001,len),0,1);
      const dist=Math.hypot(p.x-a.x-t*dx,p.z-a.z-t*dz);
      if(dist<lateral){lateral=dist;along=prefix[k]+t*(prefix[k+1]-prefix[k]);}
    }
    // Reserve turning room only near a sharp corner/fork; regular columns
    // remain close enough for the existing fire-area damage to work.
    function nearTurn(unit){
      const r=unit.route;let previous=null;
      for(let k=Math.max(0,unit.index-3);k<Math.min(r.length-1,unit.index+9);k++){
        const dx=r[k+1].x-r[k].x,dz=r[k+1].z-r[k].z,length=Math.hypot(dx,dz);if(length<.001)continue;
        const direction={x:dx/length,z:dz/length};if(previous&&previous.x*direction.x+previous.z*direction.z<.5)return true;previous=direction;
      }
      return false;
    }
    // Reserve enough arc length for a leading fighter to turn across a fork.
    // A mere body-distance check lets its follower occupy the turning space.
    const gap=(nearTurn(enemy)||nearTurn(other)) ? .92 : (other.kind==='chief' ? .65 : .48);
    return lateral<.28&&along-progress>.012&&along-progress<gap;
  });
}
function approachingTraffic(t){
  const p=t.mesh.position;
  return enemies.some(e=>{
    if(e.siege||Math.abs(e.mesh.position.y-p.y)>.65||e.mesh.position.distanceTo(p)>1.65)return false;
    let a=e.mesh.position;
    for(let i=e.index+1;i<Math.min(e.route.length,e.index+9);i++){
      const b=e.route[i],dx=b.x-a.x,dz=b.z-a.z,len=dx*dx+dz*dz;
      const k=THREE.MathUtils.clamp(((p.x-a.x)*dx+(p.z-a.z)*dz)/Math.max(.00001,len),0,1);
      if(Math.hypot(p.x-a.x-k*dx,p.z-a.z-k*dz)<.58)return true;
      a=b;
    }
    return false;
  });
}
function findRoadShoulder(t){
  const origin=t.mesh.position,cell=.20,queue=[{x:0,z:0,cost:0}],visited=new Set(),best=new Map([['0,0',0]]),parent=new Map(),points=new Map([['0,0',origin.clone()]]);
  const allies=towers.filter(o=>o!==t),foes=enemies.filter(e=>Math.abs(e.mesh.position.y-origin.y)<.65);
  const directions=[[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]];
  while(queue.length&&visited.size<420){
    queue.sort((a,b)=>a.cost-b.cost);const cur=queue.shift(),key=cur.x+','+cur.z;
    if(visited.has(key))continue;visited.add(key);const from=points.get(key);
    if(key!=='0,0'&&pathDistance(from.x,from.z)>=ROAD_SHOULDER&&from.distanceTo(origin)>.30){
      const path=[];let k=key;while(k!=='0,0'){path.push(points.get(k).clone());k=parent.get(k);}return path.reverse();
    }
    for(const [dx,dz] of directions){
      const x=cur.x+dx,z=cur.z+dz,k=x+','+z;if(visited.has(k)||Math.hypot(x*cell,z*cell)>3.2)continue;
      const cost=cur.cost+Math.hypot(dx,dz)*cell;if(cost>=(best.get(k)??Infinity))continue;
      const p=new THREE.Vector3(origin.x+x*cell,0,origin.z+z*cell);p.y=groundY(p.x,p.z);
      if(Math.abs(p.y-from.y)>.22||!isLandPoint(p.x,p.z)||obstacleAt(p.x,p.z,p.y,.13)||!segmentClear(from,p,.13))continue;
      if(allies.some(o=>Math.abs(o.mesh.position.y-p.y)<.65&&Math.hypot(o.mesh.position.x-p.x,o.mesh.position.z-p.z)<.51))continue;
      if(allies.some(o=>o.yieldTarget&&Math.abs(o.yieldTarget.y-p.y)<.65&&Math.hypot(o.yieldTarget.x-p.x,o.yieldTarget.z-p.z)<.53))continue;
      // A defender already close to a foe may take a separating step away.
      if(foes.some(e=>{
        const q=e.mesh.position,after=Math.hypot(p.x-q.x,p.z-q.z),before=Math.hypot(from.x-q.x,from.z-q.z);
        return after<.46&&after<=before+.004;
      }))continue;
      best.set(k,cost);parent.set(k,key);points.set(k,p);queue.push({x,z,cost});
    }
  }
  return null;
}
function clearRoadPriority(){
  if(!gameStarted||runEnded)return;
  for(const t of towers){
    if(t.yielding||simTime<(t.trafficCheckAt||0))continue;
    t.trafficCheckAt=simTime+.18;
    const onLane=pathDistance(t.mesh.position.x,t.mesh.position.z)<ROAD_SHOULDER-.01;
    const threat=onLane&&approachingTraffic(t);
    const stranded=onLane&&!t.moveRoute?.length;
    if((threat||stranded)&&simTime>=(t.yieldRetry||0)){
      const path=findRoadShoulder(t);
      if(path?.length){
        if(!t.resumeDestination&&t.moveRoute?.length)t.resumeDestination=t.moveRoute[t.moveRoute.length-1].clone();
        t.moveRoute=path;t.detouring=null;t.yielding=true;t.yieldStuck=0;t.yieldTarget=path[path.length-1].clone();
        trafficLog(t,'yield');
        if(selectedTower===t)notify(towerNames[t.type]+' macht die Straße frei.');
      }else t.yieldRetry=simTime+.45;
      continue;
    }
    if(t.resumeDestination&&!t.moveRoute?.length&&!threat&&simTime>=(t.resumeNotBefore||0)){
      // Let the approaching column pass before re-entering its lane.
      if(enemies.some(e=>!e.siege&&Math.abs(e.mesh.position.y-t.mesh.position.y)<.65&&e.mesh.position.distanceTo(t.mesh.position)<1.6))continue;
      const destination=t.resumeDestination;
      if(t.mesh.position.distanceTo(destination)<.12){t.resumeDestination=null;continue;}
      const route=routeForMoving(t.mesh.position,destination);
      if(route?.length){t.moveRoute=route;t.resumeDestination=null;t.detouring=null;trafficLog(t,'resume');}
      else {trafficLog(t,'no-resume-path');t.resumeDestination=null;if(selectedTower===t)notify('Die Straße ist frei. Wähle ein neues Laufziel.');}
    }
  }
}
