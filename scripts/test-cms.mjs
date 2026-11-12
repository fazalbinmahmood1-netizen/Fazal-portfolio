import fs from 'node:fs';
import assert from 'node:assert/strict';
const code=fs.readFileSync('dist/server/index.js','utf8');
const {default:worker}=await import('data:text/javascript;base64,'+Buffer.from(code).toString('base64'));
class Bucket{constructor(){this.map=new Map();this.counter=0;}async get(k){const x=this.map.get(k);return x?{etag:x.etag,json:async()=>JSON.parse(x.data),body:x.data,httpMetadata:x.httpMetadata}:null;}async put(k,data,o={}){let old=this.map.get(k);if(o.onlyIf?.etagMatches&&o.onlyIf.etagMatches!==old?.etag)return null;if(o.onlyIf?.etagDoesNotMatch==='*'&&old)return null;const x={data,etag:String(++this.counter),httpMetadata:o.httpMetadata};this.map.set(k,x);return x;}}
const env={BUCKET:new Bucket(),ADMIN_EMAIL:'owner@example.test'};const seed=JSON.parse(fs.readFileSync('content/cms-seed.json'));
async function req(path,body,options={}){const headers={...(options.anonymous?{}:{'oai-authenticated-user-id':options.id||'owner1','oai-authenticated-user-email':options.email||'owner@example.test'}),...(body?{'Origin':options.origin||'https://example.test','Content-Type':'application/json'}:{})};return worker.fetch(new Request('https://example.test'+path,{method:body?'POST':'GET',headers,body:body?JSON.stringify(body):undefined}),env);}
assert.equal((await req('/api/admin/state',null,{anonymous:true})).status,401);
assert.equal((await req('/api/admin/state',null,{email:'intruder@example.test'})).status,403);
assert.equal((await req('/api/admin/save',{revision:0,document:seed},{origin:'https://evil.test'})).status,403);
let r=await req('/api/admin/save',{revision:0,document:seed});assert.equal(r.status,200,await r.text());
assert.equal((await req('/api/admin/save',{revision:0,document:seed})).status,409);
assert.equal((await req('/api/admin/state',null,{id:'other-id'})).status,403);
const evil=structuredClone(seed);evil.theme.accent='red;display:none';assert.equal((await req('/api/admin/save',{revision:1,document:evil})).status,400);
const bad=structuredClone(seed);bad.pages[0].fields.find(x=>x.kind==='link').href='javascript:alert(1)';assert.equal((await req('/api/admin/save',{revision:1,document:bad})).status,400);
const changed=structuredClone(seed);changed.theme.heroSize=60;assert.equal((await req('/api/admin/save',{revision:1,document:changed})).status,200);
assert.equal((await env.BUCKET.get('cms/state.json')).json instanceof Function,true);
assert.equal((await (await env.BUCKET.get('cms/state.json')).json()).published.theme.heroSize,55);
assert.equal((await req('/api/admin/publish',{revision:2})).status,200);
let st=await (await env.BUCKET.get('cms/state.json')).json();assert.equal(st.published.theme.heroSize,60);assert.equal(st.history.length,1);
assert.equal((await req('/api/admin/restore',{revision:3,id:st.history[0].id})).status,200);
st=await (await env.BUCKET.get('cms/state.json')).json();assert.equal(st.draft.theme.heroSize,55);assert.equal(st.published.theme.heroSize,60);
assert.equal((await req('/api/admin/export')).status,200);
assert.equal((await req('/admin/',null,{anonymous:true})).status,200);
assert.equal((await req('/api/admin/upload',{bad:true})).status,400);
console.log('PASS: access controls, owner binding, CSRF, validation, stale-write protection, separate drafts, publishing, restore and export');
