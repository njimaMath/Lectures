const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {spawn}=require('node:child_process');
const keepAlive=setInterval(()=>{},1000);
(async()=>{
 const output=path.resolve('.review_education_ai');
 const profile=fs.mkdtempSync(path.join(os.tmpdir(),'education-ai-browser-'));
 const child=spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',['--headless','--disable-gpu','--no-sandbox','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--user-data-dir='+profile,'about:blank'],{windowsHide:true,stdio:['ignore','ignore','pipe']});
 let socket;
 try{
  const browserUrl=await new Promise((resolve,reject)=>{let buffer='';const timer=setTimeout(()=>reject(new Error('Chrome startup timeout')),10000);child.stderr.on('data',d=>{buffer+=d;const m=buffer.match(/DevTools listening on (ws:\/\/[^\s]+)/);if(m){clearTimeout(timer);resolve(m[1]);}});child.on('error',reject);});
  const address=new URL(browserUrl),targets=await(await fetch('http://'+address.host+'/json/list')).json();
  socket=new WebSocket(targets.find(t=>t.type==='page').webSocketDebuggerUrl);
  await new Promise((resolve,reject)=>{socket.addEventListener('open',resolve,{once:true});socket.addEventListener('error',reject,{once:true});});
  let serial=0;const pending=new Map();
  socket.addEventListener('message',event=>{const m=JSON.parse(event.data);if(pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);clearTimeout(p.timer);m.error?p.reject(new Error(m.error.message)):p.resolve(m.result);}});
  const cdp=(method,params={})=>new Promise((resolve,reject)=>{const id=++serial,timer=setTimeout(()=>{pending.delete(id);reject(new Error(method+' timeout'));},15000);pending.set(id,{resolve,reject,timer});socket.send(JSON.stringify({id,method,params}));});
  const evaluate=async expression=>{const r=await cdp('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw new Error(r.exceptionDetails.text);return r.result.value;};
  await cdp('Page.enable');
  await cdp('Emulation.setDeviceMetricsOverride',{width:1280,height:800,deviceScaleFactor:1,mobile:false});
  await cdp('Page.navigate',{url:'file:///C:/Users/Public/Github/Lectures/An26w/class7/education_ai.html'});
  let ready=false;for(let i=0;i<50;i++){await new Promise(r=>setTimeout(r,250));if(await evaluate('Boolean(window.MathJax?.startup?.promise)')){ready=true;break;}}
  if(!ready)throw new Error('MathJax failed to load');
  await evaluate('MathJax.startup.promise.then(()=>true)');
  const reports=[];
  for(const page of [2,4,9,10,11,18,19]){
   await evaluate('location.hash='+JSON.stringify(String(page)));
   await new Promise(r=>setTimeout(r,100));
   const report=await evaluate(`(()=>{const s=document.querySelector('.slide.active'),f=s.querySelector('.footer').getBoundingClientRect();return{label:s.getAttribute('aria-label'),page:location.hash,mathErrors:s.querySelectorAll('mjx-merror,[data-mjx-error]').length,mathOverflow:[...s.querySelectorAll('mjx-container')].filter(e=>{const r=e.getBoundingClientRect();return r.right>1218||r.left<62;}).length,contentBottom:Math.max(...[...s.children].filter(e=>!e.classList.contains('footer')).map(e=>e.getBoundingClientRect().bottom)),footerTop:f.top,scrollHeight:s.scrollHeight,clientHeight:s.clientHeight};})()`);
   const shot=await cdp('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(path.join(output,'slide-'+page+'.png'),Buffer.from(shot.data,'base64'));reports.push(report);console.log(JSON.stringify(report));
  }
  fs.writeFileSync(path.join(output,'report.json'),JSON.stringify(reports,null,2));
  await cdp('Browser.close').catch(()=>{});
 }finally{if(socket)socket.close();child.kill();}
})().catch(e=>{console.error(e.message);process.exitCode=1;}).finally(()=>clearInterval(keepAlive));
