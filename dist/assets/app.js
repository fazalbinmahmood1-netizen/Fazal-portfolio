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
 function showSlide(n){panels.forEach((p,i)=>p.hidden=i!==n);dots.forEach((d,i)=>{d.classList.toggle('active',i===n);d.setAttribute('aria-pressed',String(i===n));});}
 dots.forEach(dot=>dot.addEventListener('click',()=>showSlide(Number(dot.dataset.to))));
});
const dialog=document.querySelector('#search-dialog'),input=document.querySelector('#search-input'),results=document.querySelector('#search-results');let searchData=null,searchPromise=null;
async function loadSearch(){if(searchData)return searchData;if(!searchPromise)searchPromise=fetch('/assets/search.json').then(r=>{if(!r.ok)throw Error('Search unavailable');return r.json();}).then(data=>searchData=data).catch(err=>{searchPromise=null;throw err;});return searchPromise;}
function displayResults(){results.replaceChildren();const term=input.value.trim().toLowerCase();if(!searchData)return;const matches=searchData.filter(x=>(x.title+' '+x.description).toLowerCase().includes(term)).slice(0,8);if(!matches.length){const p=document.createElement('p');p.textContent='No matches found. Try Shopify, mobile or Nishani.';results.append(p);}matches.forEach(item=>{const a=document.createElement('a'),title=document.createElement('strong'),desc=document.createElement('span');a.className='search-result';a.href=item.url;title.textContent=item.title;desc.textContent=item.description;a.append(title,desc);results.append(a);});}
document.querySelector('.search-toggle').addEventListener('click',async()=>{closeMenu();dialog.showModal();input.focus();results.textContent='Loading search…';try{await loadSearch();displayResults();}catch{results.textContent='Search could not load. Please use the navigation links or try again.';}});
document.querySelector('.close-search').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});input.addEventListener('input',displayResults);
document.querySelectorAll('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());
