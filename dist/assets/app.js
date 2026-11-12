'use strict';
const menu=document.querySelector('.menu-toggle'),nav=document.querySelector('#navigation');
function closeMenu(){nav.classList.remove('open');menu.setAttribute('aria-expanded','false');}
menu.addEventListener('click',()=>{const open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});
nav.addEventListener('click',e=>{if(e.target.closest('a'))closeMenu();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeMenu();document.querySelectorAll('details[open]').forEach(el=>el.removeAttribute('open'));}});
document.addEventListener('click',e=>{document.querySelectorAll('details[open]').forEach(el=>{if(!el.contains(e.target))el.removeAttribute('open');});});
const motion=matchMedia('(prefers-reduced-motion: reduce)');
if(!motion.matches&&'IntersectionObserver'in window){document.documentElement.classList.add('js-motion');const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('visible');observer.unobserve(entry.target);}}),{threshold:.08});document.querySelectorAll('.reveal').forEach(el=>observer.observe(el));}
document.querySelectorAll('.quote-slider').forEach(slider=>{
 const panels=[...slider.querySelectorAll('[data-slide]')],dots=[...slider.querySelectorAll('[data-to]')];
 let index=0,timer=null,inView=false,hover=false,interacted=false,start=null;
 const hint=slider.querySelector('.swipe-hint');
 function stop(){clearTimeout(timer);timer=null;}
 function schedule(){stop();if(inView&&!hover&&!interacted&&!motion.matches&&!document.hidden)timer=setTimeout(()=>{showSlide((index+1)%panels.length);schedule();},5000);}
 function showSlide(n){index=(n+panels.length)%panels.length;panels.forEach((p,i)=>{p.hidden=i!==index;p.setAttribute('aria-hidden',String(i!==index));});dots.forEach((d,i)=>{d.classList.toggle('active',i===index);d.setAttribute('aria-pressed',String(i===index));});}
 function manual(n){interacted=true;stop();if(hint)hint.classList.add('dismissed');showSlide(n);}
 dots.forEach((dot,i)=>dot.addEventListener('click',()=>manual(i)));
 slider.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();manual(index+(e.key==='ArrowRight'?1:-1));dots[index].focus();}});
 slider.addEventListener('pointerdown',e=>{if(e.isPrimary)start={x:e.clientX,y:e.clientY};});
 slider.addEventListener('pointerup',e=>{if(!start)return;const dx=e.clientX-start.x,dy=e.clientY-start.y;start=null;if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)*1.5)manual(index+(dx<0?1:-1));});
 slider.addEventListener('pointercancel',()=>start=null);
 slider.addEventListener('mouseenter',()=>{hover=true;stop();});slider.addEventListener('mouseleave',()=>{hover=false;schedule();});
 slider.addEventListener('focusin',stop);slider.addEventListener('focusout',()=>{if(!slider.contains(document.activeElement))schedule();});
 document.addEventListener('visibilitychange',schedule);motion.addEventListener('change',schedule);
 if('IntersectionObserver'in window)new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;schedule();},{threshold:.25}).observe(slider);
 showSlide(0);
});
// The reference uses scroll-linked horizontal logo movement on desktop only.
const logoViewport=document.querySelector('.logo-viewport'),logoTrack=document.querySelector('.client-logos');
if(logoViewport&&logoTrack){
 const desktop=matchMedia('(min-width:1025px)');let queued=false,visible=true;
 function paint(){queued=false;if(!desktop.matches||motion.matches){logoTrack.style.transform='';return;}const r=logoViewport.getBoundingClientRect(),travel=Math.max(0,logoTrack.scrollWidth-logoViewport.clientWidth),progress=Math.max(0,Math.min(1,(innerHeight-r.top)/(innerHeight+r.height)));logoTrack.style.transform=`translate3d(${-travel*progress}px,0,0)`;}
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
