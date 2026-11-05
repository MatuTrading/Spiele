// Dependency-free isometric office renderer. Visual 2.5D projection, not a WebGL engine.
export function mountOffice(canvas,getState){
 let running=true,ctx=canvas.getContext('2d',{alpha:false});
 if(!ctx)return ()=>{};
 function frame(t){if(!running||!canvas.isConnected)return;const rect=canvas.getBoundingClientRect(),w=Math.max(300,rect.width),h=Math.max(230,rect.height),dpr=Math.min(devicePixelRatio||1,2);if(canvas.width!==Math.round(w*dpr)||canvas.height!==Math.round(h*dpr)){canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);}ctx.setTransform(dpr,0,0,dpr,0,0);draw(ctx,w,h,t*.001,getState());requestAnimationFrame(frame);}requestAnimationFrame(frame);return ()=>running=false;
}
function draw(c,w,h,t,s){
 const tier=s.office;const scale=Math.min(w/820,h/405),ox=w*.5,oy=h*.49;const X=53*scale,Y=27*scale,Z=45*scale;
 const p=(x,y,z=0)=>[ox+(x-y)*X,oy+(x+y)*Y-z*Z];
 const path=(pts,fill,stroke='#0000',lw=1)=>{c.beginPath();pts.forEach((a,i)=>{let b=Array.isArray(a)&&a.length===2?a:p(...a);i?c.lineTo(...b):c.moveTo(...b)});c.closePath();c.fillStyle=fill;c.fill();if(stroke!=='#0000'){c.strokeStyle=stroke;c.lineWidth=lw*scale;c.stroke();}};
 const line=(a,b,color='#fff',lw=1)=>{c.beginPath();c.moveTo(...p(...a));c.lineTo(...p(...b));c.strokeStyle=color;c.lineWidth=lw*scale;c.stroke();};
 const box=(x,y,dx,dy,z,height,top,front,right)=>{let a=[x,y,z],b=[x+dx,y,z],d=[x,y+dy,z],e=[x+dx,y+dy,z];let A=[x,y,z+height],B=[x+dx,y,z+height],D=[x,y+dy,z+height],E=[x+dx,y+dy,z+height];path([d,e,E,D],front);path([b,e,E,B],right);path([A,B,E,D],top);};
 const circle=(x,y,z,r,color)=>{const [px,py]=p(x,y,z);c.beginPath();c.ellipse(px,py,r*scale,r*.8*scale,0,0,Math.PI*2);c.fillStyle=color;c.fill();};
 const glow=c.createLinearGradient(0,0,w,h);glow.addColorStop(0,'#112d42');glow.addColorStop(.52,'#173345');glow.addColorStop(1,'#071521');c.fillStyle=glow;c.fillRect(0,0,w,h);
 for(let i=0;i<28;i++){let lx=(i*71)%w,ly=(i*39)%h;c.fillStyle=`rgba(147,208,207,${.025+.015*Math.sin(t+i)})`;c.fillRect(lx,ly,1.2,1.2);}
 // Big room on a raised architectural plinth.
 box(-3.8,-2.6,7.6,5.2,-.25,.25,'#a88e6a','#775e45','#5c4a39');
 // Back and left walls behind furniture: paneled architecture, glass and city silhouettes.
 path([[-3.8,-2.6,0],[3.8,-2.6,0],[3.8,-2.6,3.1],[-3.8,-2.6,3.1]],'#c7c5ad');
 path([[-3.8,-2.6,0],[-3.8,2.6,0],[-3.8,2.6,3.1],[-3.8,-2.6,3.1]],'#9eab9c');
 // Sky windows in back wall.
 for(let j=0;j<3;j++){let a=-3.35+j*2.22,b=a+1.85;
 path([[a,-2.59,.72],[b,-2.59,.72],[b,-2.59,2.82],[a,-2.59,2.82]],'#518ca2');
 path([[a,-2.58,1.15],[b,-2.58,1.15],[b,-2.58,2.82],[a,-2.58,2.82]],'#2a617b');
 for(let k=0;k<5;k++){let bx=a+.05+k*.37,ht=.5+(k%3)*.18;path([[bx,-2.57,1.15],[bx+.3,-2.57,1.15],[bx+.3,-2.57,1.15+ht],[bx,-2.57,1.15+ht]],'#29475c');}
 line([a,-2.56,1.75],[b,-2.56,1.75],'#b9dfda',1.7);line([(a+b)/2,-2.56,.72],[(a+b)/2,-2.56,2.82],'#abc9c4',1.7);
 }
 // Left wall wooden panels and framed art.
 for(let j=0;j<4;j++){let yy=-2.25+j*1.12;path([[-3.79,yy,.45],[-3.79,yy+.92,.45],[-3.79,yy+.92,2.85],[-3.79,yy,2.85]],j%2?'#9bad9f':'#a4b6a5');}
 path([[-3.78,-1.3,1.1],[-3.78,.4,1.1],[-3.78,.4,2.35],[-3.78,-1.3,2.35]],'#223f54','#e6c88b',2);
 path([[-3.76,-1.08,1.35],[-3.76,.17,1.35],[-3.76,.17,2.15],[-3.76,-1.08,2.15]],'#2c6a7a');
 // Checkerboard floor tiles.
 path([[-3.8,-2.6,0],[3.8,-2.6,0],[3.8,2.6,0],[-3.8,2.6,0]],tier>1?'#e8dcc4':'#e5d9c6');
 for(let x=-3.8;x<3.8;x+=.8)line([x,-2.6,.005],[x,2.6,.005],'rgba(92,74,52,.12)',.7);
 for(let y=-2.6;y<2.6;y+=.8)line([-3.8,y,.005],[3.8,y,.005],'rgba(92,74,52,.12)',.7);
 // Gold border inlay.
 path([[-3.45,-2.27,.01],[3.45,-2.27,.01],[3.45,2.27,.01],[-3.45,2.27,.01]],'rgba(0,0,0,0)','#bf995d',1.7);
 // Rugs: recessed top polygons.
 path([[-1.5,-.6,.012],[1,-.6,.012],[1,1.1,.012],[-1.5,1.1,.012]],'#345766');
 path([[-1.4,-.52,.02],[.9,-.52,.02],[.9,1.02,.02],[-1.4,1.02,.02]],'#507b7f');
 // Furniture sorted from back to front.
 // Bookshelf.
 box(1.9,-2.34,1.25,.39,0,2.15,'#bd9566','#8b6146','#634533');
 for(let j=0;j<3;j++){box(1.96,-2.3,1.08,.34,.5+j*.58,.075,'#c9a577','#8a6244','#654433');for(let k=0;k<6;k++)box(2.02+k*.15,-2.28,.1,.17,.63+j*.58,.37,['#315d65','#e4be79','#617f68'][k%3],'#294955','#23444a');}
 // Board / monitor wall.
 box(-2.8,-2.43,1.78,.15,1.1,1.14,'#35546b','#102c40','#0a2332');
 // Uptrend inside framed glass monitor.
 for(let k=0;k<6;k++)line([-2.62+k*.27,-2.27,1.4+k*.12],[-2.34+k*.27,-2.27,1.55+k*.12],'#8ce5b1',2);
 // Meeting table and chairs when upgraded.
 if(tier>=1){box(1,-.35,1.5,1.05,.4,.14,'#ba8e66','#785a40','#674b35');for(let i=0;i<3;i++){box(.9+i*.55,-.57,.28,.28,0,.38,'#233b4a','#294657','#1a2c39');box(.9+i*.55,-.57,.29,.13,.38,.44,'#314e61','#213b50','#172b3d');}}
 // Desk: legs and large wooden surface.
 box(-1.7,.05,2.35,1.05,.03,.72,'#c6a179','#876245','#714c37');
 box(-1.8,-.05,2.55,1.24,.72,.13,'#e6c29a','#b48d62','#8e6b51');
 // Desk drawers.
 box(-1.62,.74,.48,.36,.12,.57,'#9c714d','#77583e','#5b4333');
 circle(-1.38,1.02,.44,4,'#dabf83');
 // Monitors and monitor stands on desk.
 box(-1.24,.10,.07,.12,.83,.27,'#303d4a','#2c3f4a','#202f3d');
 box(-1.64,-.02,.92,.12,1.08,.7,'#29475b','#182e40','#152637');
 path([[-1.55,.11,1.18],[-.87,.11,1.18],[-.87,.11,1.62],[-1.55,.11,1.62]],'#143650');
 for(let i=0;i<4;i++)line([-1.44+i*.16,.115,1.22],[-1.3+i*.16,.115,1.43+i*.035],'#6de1bd',1.5);
 // Gold desk lamp.
 line([.30,.2,.84],[.24,.12,1.47],'#c8a561',3);circle(.24,.12,1.55,11,'#f5d68a');
 // Plants and pots.
 const plant=(x,y)=>{box(x-.15,y-.15,.3,.3,0,.32,'#b87954','#9d5d43','#774834');for(let j=0;j<7;j++){let ax=Math.sin(j*2.4)*.2,ay=Math.cos(j*2.4)*.22;line([x,y,.31],[x+ax,y+ay,.85+j*.045],'#397962',3);circle(x+ax,y+ay,.85+j*.045,5.5,'#5fa789');}};
 plant(3,1.9);plant(-3,1.9);
 if(tier>=2){plant(2.8,-1.5);box(.7,1.9,1.15,.35,0,.64,'#466e74','#355b61','#274b54');}
 // Team members behind desk / around meeting table.
 if(tier>=1){for(let i=0;i<Math.min(s.staff.length,5);i++){let x=i<2?1.25+i*.72:2.15-(i-2)*.5,y=i<2?-.97:.8;drawPerson(x,y,Math.sin(t*2+i)*.08,'#536f77',.83,false);}}
 // Player: walks periodically from work desk to meeting zone; animated stride.
 let cycle=(t*.07)%1;let walk=cycle<.28||cycle>.77;let x=cycle<.28?-.3+cycle/.28*.75:cycle<.77?.45:-.3+(.99-cycle)/.22*.75;let y=cycle<.28?1.15-cycle/.28*.32:cycle<.77?.83:1.15-(.99-cycle)/.22*.32;
 drawPerson(x,y,t,'#192c50',1,true,walk);
 // Foreground trim and area label.
 path([[-3.8,2.6,-.25],[3.8,2.6,-.25],[3.8,2.6,-.13],[-3.8,2.6,-.13]],'#8d6a49');
 c.save();c.font=`700 ${11*scale}px system-ui`;c.fillStyle='#e8d8b1';c.textAlign='left';c.fillText(['GRÜNDERBÜRO','INVESTMENTBOUTIQUE','ASSET MANAGEMENT','FINANZIMPERIUM'][Math.min(3,tier)],18*scale,26*scale);c.restore();
 function drawPerson(x,y,tt,suit,sz,hero,walking=false){
  const [px,py]=p(x,y,0),K=scale*sz; c.save();c.translate(px,py);c.scale(K,K);
  c.fillStyle='rgba(10,22,30,.22)';c.beginPath();c.ellipse(0,3,16,6,0,0,Math.PI*2);c.fill();
  const step=walking?Math.sin(tt*13)*8:Math.sin(tt*1.6)*1.2;
  c.strokeStyle='#182535';c.lineWidth=7;c.lineCap='round';c.beginPath();c.moveTo(-5,-21);c.lineTo(-7+step*.8,-2);c.moveTo(5,-21);c.lineTo(7-step*.8,-2);c.stroke();
  c.strokeStyle='#101a27';c.lineWidth=9;c.beginPath();c.moveTo(-8+step*.8,-1);c.lineTo(-13+step*.8,2);c.moveTo(7-step*.8,-1);c.lineTo(12-step*.8,2);c.stroke();
  c.fillStyle=suit;c.beginPath();c.moveTo(-13,-53);c.lineTo(12,-53);c.lineTo(10,-21);c.lineTo(-11,-21);c.closePath();c.fill();
  c.strokeStyle=hero?'#667997':'#80969b';c.lineWidth=.8;for(let k=-8;k<10;k+=5){c.beginPath();c.moveTo(k,-51);c.lineTo(k,-23);c.stroke();}
  c.fillStyle='#f3e8d8';c.beginPath();c.moveTo(-4,-52);c.lineTo(4,-52);c.lineTo(0,-32);c.closePath();c.fill();
  c.fillStyle=hero?'#aa844b':'#6a8796';c.beginPath();c.moveTo(-2,-50);c.lineTo(2,-50);c.lineTo(3,-38);c.lineTo(0,-34);c.lineTo(-3,-38);c.closePath();c.fill();
  c.strokeStyle=suit;c.lineWidth=8;c.beginPath();c.moveTo(-12,-48);c.lineTo(-20+(walking?step*.4:Math.sin(tt)*2),-30);c.moveTo(12,-48);c.lineTo(18-(walking?step*.4:Math.sin(tt)*2),-31);c.stroke();
  c.fillStyle='#e5b58c';c.beginPath();c.arc(-20+(walking?step*.4:Math.sin(tt)*2),-29,4.1,0,7);c.arc(18-(walking?step*.4:Math.sin(tt)*2),-30,4.1,0,7);c.fill();
  c.fillStyle='#e7bb93';c.beginPath();c.ellipse(0,-63,10.5,12,0,0,Math.PI*2);c.fill();
  c.fillStyle=hero?'#e3bc61':'#6d5646';c.beginPath();c.moveTo(-10,-66);c.quadraticCurveTo(-13,-79,2,-77);c.quadraticCurveTo(11,-76,10,-68);c.lineTo(6,-71);c.quadraticCurveTo(-3,-69,-10,-66);c.fill();
  c.fillStyle='#2c343a';c.fillRect(-4,-63,1.7,1.4);c.fillRect(4,-63,1.7,1.4);
  c.restore();
 }
}