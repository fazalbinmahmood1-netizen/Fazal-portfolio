'use strict';
const menu=document.querySelector('.menu-toggle'),nav=document.querySelector('#navigation');
function closeMenu(){nav.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Open menu');}
menu.addEventListener('click',()=>{const open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'Close menu':'Open menu');});
matchMedia('(min-width:768px)').addEventListener('change',closeMenu);
document.addEventListener('click',e=>{if(!e.target.closest('.header'))closeMenu();});
nav.addEventListener('click',e=>{if(e.target.closest('a'))closeMenu();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeMenu();document.querySelectorAll('details[open]').forEach(el=>el.removeAttribute('open'));}});
document.addEventListener('click',e=>{document.querySelectorAll('details[open]').forEach(el=>{if(!el.contains(e.target))el.removeAttribute('open');});});
const motion=matchMedia('(prefers-reduced-motion: reduce)');
if(!motion.matches&&'IntersectionObserver'in window){document.documentElement.classList.add('js-motion');const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('visible');observer.unobserve(entry.target);}}),{threshold:.08});document.querySelectorAll('.reveal').forEach(el=>observer.observe(el));}
document.querySelectorAll('.quote-slider').forEach(slider=>{
 const viewport=slider.querySelector('.quote-panels'),panels=[...viewport.querySelectorAll('[data-slide]')],dots=[...slider.querySelectorAll('[data-to]')],hint=slider.querySelector('.swipe-hint');
 if(panels.length<2)return;
 const track=document.createElement('div');track.className='quote-track';
 panels.forEach(p=>{p.hidden=false;track.append(p);});
 const before=panels.at(-1).cloneNode(true),after=panels[0].cloneNode(true);
 [before,after].forEach(p=>{p.removeAttribute('data-slide');p.setAttribute('aria-hidden','true');p.inert=true;p.querySelectorAll('[id]').forEach(e=>e.removeAttribute('id'));});
 track.prepend(before);track.append(after);viewport.append(track);slider.classList.add('sliding');
 let index=0,position=1,timer=null,inView=false,hover=false,interacted=false,drag=null,animating=false,settleTimer=null;
 const step=()=>viewport.getBoundingClientRect().width+10;
 function stop(){clearTimeout(timer);}
 function schedule(){stop();if(inView&&!hover&&!interacted&&!motion.matches&&!document.hidden)timer=setTimeout(()=>go(index+1),5000);}
 function paint(animate=true,offset=0){track.style.transitionDuration=animate&&!motion.matches?'500ms':'0ms';track.style.transform=`translate3d(${-position*step()+offset}px,0,0)`;}
 function mark(){panels.forEach((p,i)=>{p.setAttribute('aria-hidden',String(i!==index));p.inert=i!==index;});dots.forEach((d,i)=>{d.classList.toggle('active',i===index);d.setAttribute('aria-pressed',String(i===index));});}
 function settle(){clearTimeout(settleTimer);if(position===0)position=panels.length;if(position===panels.length+1)position=1;paint(false);animating=false;schedule();}
 function go(n){if(animating)return;index=(n+panels.length)%panels.length;position=n<0?0:n>=panels.length?panels.length+1:index+1;animating=true;mark();paint();clearTimeout(settleTimer);settleTimer=setTimeout(settle,motion.matches?0:550);}
 function manual(n){interacted=true;stop();hint?.classList.add('dismissed');go(n);}
 track.addEventListener('transitionend',e=>{if(e.target===track&&e.propertyName==='transform')settle();});
 dots.forEach((d,i)=>d.addEventListener('click',()=>manual(i)));
 slider.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();manual(index+(e.key==='ArrowRight'?1:-1));dots[index].focus();}});
 viewport.addEventListener('pointerdown',e=>{if(!e.isPrimary||e.button!==0||animating||e.target.closest('a,button,input'))return;stop();drag={id:e.pointerId,x:e.clientX,y:e.clientY,dx:0,axis:null};});
 viewport.addEventListener('pointermove',e=>{if(!drag||drag.id!==e.pointerId)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(!drag.axis&&Math.max(Math.abs(dx),Math.abs(dy))>6){drag.axis=Math.abs(dx)>Math.abs(dy)?'x':'y';if(drag.axis==='x'){viewport.setPointerCapture(e.pointerId);viewport.classList.add('dragging');}}if(drag.axis==='x'){e.preventDefault();drag.dx=dx;paint(false,dx);}});
 function end(e){if(!drag||drag.id!==e.pointerId)return;const d=drag;drag=null;viewport.classList.remove('dragging');if(viewport.hasPointerCapture(e.pointerId))viewport.releasePointerCapture(e.pointerId);if(d.axis==='x'){if(Math.abs(d.dx)>Math.min(50,viewport.clientWidth*.15)&&e.type!=='pointercancel')manual(index+(d.dx<0?1:-1));else{animating=true;paint();settleTimer=setTimeout(settle,550);}}else schedule();}
 viewport.addEventListener('pointerup',end);viewport.addEventListener('pointercancel',end);viewport.addEventListener('pointerleave',e=>{if(drag&&!viewport.hasPointerCapture(e.pointerId))end(e);});viewport.addEventListener('dragstart',e=>e.preventDefault());
 slider.addEventListener('mouseenter',()=>{hover=true;stop();});slider.addEventListener('mouseleave',()=>{hover=false;schedule();});slider.addEventListener('focusin',stop);slider.addEventListener('focusout',schedule);
 document.addEventListener('visibilitychange',schedule);motion.addEventListener('change',()=>{settle();schedule();});
 new ResizeObserver(()=>{drag=null;settle();}).observe(viewport);
 if('IntersectionObserver'in window)new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;schedule();},{threshold:.25}).observe(slider);
 mark();paint(false);
});
// The reference uses scroll-linked horizontal logo movement on desktop only.
const logoViewport=document.querySelector('.logo-viewport'),logoTrack=document.querySelector('.client-logos');
if(logoViewport&&logoTrack){
 const desktop=matchMedia('(min-width:1025px)');let queued=false,visible=true;
 function paint(){queued=false;document.documentElement.style.setProperty('--viewport-width',document.documentElement.clientWidth+'px');if(!desktop.matches||motion.matches){logoTrack.style.transform='';return;}const r=logoViewport.getBoundingClientRect(),travel=Math.max(0,logoTrack.scrollWidth-logoViewport.clientWidth),progress=Math.max(0,Math.min(1,(innerHeight-r.top)/(innerHeight+r.height)));logoTrack.style.transform=`translate3d(${-travel*progress}px,0,0)`;}
 function requestPaint(){if(!queued&&visible){queued=true;requestAnimationFrame(paint);}}
 addEventListener('scroll',requestPaint,{passive:true});addEventListener('resize',requestPaint,{passive:true});desktop.addEventListener('change',paint);motion.addEventListener('change',paint);
 if('IntersectionObserver'in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible)requestPaint();},{rootMargin:'100px'}).observe(logoViewport);
 paint();
}
// Load the lightweight SVG player near the gesture; play once on entry.
const gesture=document.querySelector('.swipe-hint');
if(gesture&&!motion.matches&&'IntersectionObserver'in window){
 let animation=null,ready=false,entered=false,played=false;
 function play(){if(ready&&entered&&!played&&!gesture.classList.contains('dismissed')&&!motion.matches){played=true;gesture.classList.add('playing');animation.play();}}
 const arrival=new IntersectionObserver(entries=>{if(entries[0].isIntersecting){entered=true;play();}else{entered=false;}},{threshold:.6});arrival.observe(gesture);
 const loader=new IntersectionObserver(entries=>{if(!entries[0].isIntersecting)return;loader.disconnect();
 const script=document.createElement('script');script.src='/assets/lottie-light.min.js';script.async=true;
 script.onload=()=>{if(!window.lottie)return;animation=window.lottie.loadAnimation({container:gesture,renderer:'svg',loop:false,autoplay:false,path:'/assets/swipe-hint.json',rendererSettings:{progressiveLoad:true}});animation.addEventListener('DOMLoaded',()=>{ready=true;play();});animation.addEventListener('complete',()=>{gesture.classList.add('finished');arrival.disconnect();animation.destroy();});};
 document.head.append(script);
 },{rootMargin:'500px'});loader.observe(gesture);
 motion.addEventListener('change',()=>{if(motion.matches){animation?.destroy();gesture.classList.add('finished');arrival.disconnect();loader.disconnect();}});
}
const dialog=document.querySelector('#search-dialog'),input=document.querySelector('#search-input'),results=document.querySelector('#search-results');let searchData=null,searchPromise=null;
async function loadSearch(){if(searchData)return searchData;if(!searchPromise)searchPromise=fetch('/assets/search.json').then(r=>{if(!r.ok)throw Error('Search unavailable');return r.json();}).then(data=>searchData=data).catch(err=>{searchPromise=null;throw err;});return searchPromise;}
function displayResults(){results.replaceChildren();const term=input.value.trim().toLowerCase();if(!searchData)return;const matches=searchData.filter(x=>(x.title+' '+x.description).toLowerCase().includes(term)).slice(0,8);if(!matches.length){const p=document.createElement('p');p.textContent='No matches found. Try Shopify, mobile or Nishani.';results.append(p);}matches.forEach(item=>{const a=document.createElement('a'),title=document.createElement('strong'),desc=document.createElement('span');a.className='search-result';a.href=item.url;title.textContent=item.title;desc.textContent=item.description;a.append(title,desc);results.append(a);});}
document.querySelector('.search-toggle').addEventListener('click',async()=>{closeMenu();dialog.showModal();input.focus();results.textContent='Loading search…';try{await loadSearch();displayResults();}catch{results.textContent='Search could not load. Please use the navigation links or try again.';}});
document.querySelector('.close-search').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});input.addEventListener('input',displayResults);
document.querySelectorAll('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());
