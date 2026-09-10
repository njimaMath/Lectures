(() => {
  const svg = (content, height = 230, label = '') => `<svg viewBox="0 0 720 ${height}" role="img" aria-label="${label}" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrow-${height}" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="none" stroke="#087e80"/></marker></defs>${content}</svg>`;
  const text = (x,y,value,size=14,color='#203b3b') => `<text x="${x}" y="${y}" text-anchor="middle" font-size="${size}" fill="${color}">${value}</text>`;
  const box = (x,y,w,h,label,fill='#fffefa') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="4" fill="${fill}" stroke="#a8c4b7"/>${text(x+w/2,y+h/2+5,label)}`;
  const line = (x,y,a,b) => `<path d="M${x} ${y}L${a} ${b}" fill="none" stroke="#087e80" stroke-width="1.5"/>`;
  const figure = (id,n,title,body,caption) => {
    const anchor = document.getElementById(id);
    anchor.insertAdjacentHTML('afterend',`<figure class="visual"><div class="visual-label"><span>FIG. ${n}</span><span>${title}</span></div>${body}<figcaption>${caption}</figcaption></figure>`);
  };
  let hero = text(360,30,'FROM CONTEXT TO POSSIBILITY',12,'#087e80');
  [120,480].forEach((x,i)=>{hero+=box(x,380,120,42,['Alice','likes'][i]);hero+=line(x+60,380,x+60,325)});
  for(let layer=0;layer<2;layer++){
    const y=layer===0?250:140;
    hero+=`<rect x="100" y="${y}" width="520" height="75" rx="5" fill="${layer===0?'#dce9df':'#c4ded1'}" stroke="#9bbfaf"/>`;
    hero+=text(360,y+29,`TRANSFORMER BLOCK ${layer+1}`,12,'#087e80');
    [180,540].forEach((x,i)=>{hero+=`<circle cx="${x}" cy="${y+52}" r="6" fill="#087e80"/>`;if(layer===0){for(let j=0;j<=i;j++)hero+=`<path d="M${180+j*360} ${y} C${180+j*360} 222 ${x} 230 ${x} 215" stroke="#087e80" stroke-opacity=".35" fill="none"/>`}});
  }
  hero+=line(540,140,540,102)+box(466,58,148,44,'tea  ·  80%','#087e80');
  hero=hero.replace('>tea  ·  80%</text>',' fill-opacity="1">tea  ·  80%</text>').replace('fill="#203b3b" fill-opacity="1"','fill="#ffffff"');
  hero+=text(260,85,'次の単語を、文脈から。',19)+text(360,463,'模式図 / 確率は第4節の経験分布を例示',11,'#637571');
  document.getElementById('hero-visual').innerHTML=svg(hero,490,'過去のトークンが2つのTransformerブロックを通り、次単語の分布になる模式図');
  figure('section-1','01','ひとつ先を予測する',svg(text(75,54,'入力',12)+text(75,152,'教師',12)+box(145,25,140,52,'Alice')+box(325,25,140,52,'likes')+box(325,125,140,52,'likes','#d2e6db')+box(505,125,140,52,'tea','#d2e6db')+line(215,80,380,120)+line(395,80,560,120)+text(350,212,'入力と教師を、1トークンずらして対応づける',13),240,'Aliceからlikesを、Alice likesからteaを予測する入力と教師の対応'),'各位置の出力は、その次の単語を予測する。後の位置ほど長い接頭列を利用できる。');
  figure('section-2','02','モデル全体の見取り図','<div class="flow"><div class="flow-node">入力<small>token + position</small></div><span class="flow-arrow">→</span><div class="flow-node">Block 1<small>attention + FFN</small></div><span class="flow-arrow">→</span><div class="flow-node">Block 2<small>attention + FFN</small></div><span class="flow-arrow">→</span><div class="flow-node">次単語の分布<small>LN → linear → softmax</small></div></div>','2つのブロックで文脈を取り込み、各位置の隠れ状態を語彙上の確率分布に変換する。');
  let embedding=box(15,68,100,50,'Alice')+text(152,99,'→',24)+text(265,30,'トークン埋め込み',13)+text(440,30,'位置埋め込み',13)+text(353,99,'+',24)+text(533,99,'=',24)+text(625,30,'初期状態',13);
  [220,395,580].forEach((x,k)=>{[0,1,2,3].forEach(j=>{embedding+=`<rect x="${x+j*22}" y="65" width="19" height="60" fill="#087e80" opacity="${.2+((j*3+k*2)%7)/10}"/>`})});
  figure('section-2-1','03','単語の意味に、位置を加える',svg(embedding,165,'トークン埋め込みと位置埋め込みのベクトル和'),'色の濃淡はベクトル成分の模式表現。2つのベクトルは同じ次元を持ち、成分ごとに加算される。');
  figure('section-2-4','04','参照できるのは、現在と過去だけ','<div class="mask-layout"><div class="mask-grid" id="mask-grid" role="img" aria-label="5位置の下三角因果マスク"></div><div><label class="control-label" for="mask-position">予測を行う入力位置 <output id="position-value">3</output></label><input id="mask-position" type="range" min="1" max="5" value="3"><p class="mask-status" id="mask-status" aria-live="polite"></p><div class="legend"><i></i>選択行の参照可能な位置<br>淡い緑：他の行の参照可能な位置 / ×：未来</div></div></div>','5位置の模式例。行はクエリ位置、列はキー位置。未来のスコアを負の無限大にし、softmax 後の重みを0にする。');
  const mask=document.getElementById('mask-grid'),range=document.getElementById('mask-position');
  function updateMask(){const pos=Number(range.value);let cells='<span class="mask-cell label">i / j</span>';for(let j=1;j<=5;j++)cells+=`<span class="mask-cell label">${j}</span>`;for(let i=1;i<=5;i++){cells+=`<span class="mask-cell label">${i}</span>`;for(let j=1;j<=5;j++)cells+=`<span class="mask-cell ${j<=i?'allowed':''} ${i===pos&&j<=i?'selected':''}">${j<=i?'0':'×'}</span>`;}mask.innerHTML=cells;document.getElementById('position-value').value=pos;document.getElementById('mask-status').textContent=`位置 ${pos} は、位置 1〜${pos} を参照して次の単語を予測します。`;mask.setAttribute('aria-label',`5位置の因果マスク。選択した行${pos}では列1から${pos}まで参照可能。`)}
  range.addEventListener('input',updateMask);updateMask();
  figure('section-2-5','05','Attention の情報の流れ',svg(box(20,30,110,45,'Query')+box(20,100,110,45,'Key')+line(130,52,195,87)+line(130,122,195,87)+box(195,65,150,45,'内積 / スケール')+line(345,87,395,87)+box(395,65,135,45,'mask + softmax')+line(530,87,600,87)+box(20,175,110,45,'Value')+line(130,197,600,197)+line(600,197,600,110)+box(560,65,140,45,'重み付き和'),245,'QueryとKeyから重みを計算し、Valueの重み付き和を作る'),'Query と Key が参照の強さを決め、Value が実際に集約される情報を運ぶ。この計算を複数のヘッドで並列に行う。');
  figure('section-2-6','06','残差接続で、情報を引き継ぐ',svg(text(45,113,'入力',14)+line(75,108,140,108)+box(140,83,100,50,'LN')+line(240,108,285,108)+box(285,83,190,50,'Linear → ReLU → Linear')+line(475,108,562,108)+`<path d="M95 108V35H580V86" stroke="#087e80" fill="none" stroke-width="1.5"/>`+text(350,24,'残差経路',12)+`<circle cx="580" cy="108" r="22" fill="#d2e6db" stroke="#087e80"/>`+text(580,114,'+',22)+line(602,108,660,108)+text(687,113,'出力',14),180,'正規化とFFNを通る経路に入力を直接加算する残差接続'),'Pre-LN のフィードフォワード部分層。入力を直接加える経路と、正規化して変換する経路を合流させる。');
  figure('section-3','07','予測と正解を比較し、更新する','<div class="flow"><div class="flow-node">接頭列<small>真の過去単語</small></div><span class="flow-arrow">→</span><div class="flow-node">モデルの予測<small>次単語の確率</small></div><span class="flow-arrow">→</span><div class="flow-node">損失<small>正解の負の対数確率</small></div></div><div style="text-align:center;color:var(--accent);font-size:13px">← 勾配を計算し、パラメータを更新 ←</div>','学習時は真の接頭列を入力する。すべての文と予測位置について損失を平均し、共有パラメータを更新する。');
  figure('section-4-5','08','文脈が変わると、分布が変わる','<div class="context-controls" aria-label="接頭列を選択"><button type="button" data-context="0" aria-pressed="true">Alice likes</button><button type="button" data-context="1" aria-pressed="false">Bob likes</button><button type="button" data-context="2" aria-pressed="false">Alice / Bob</button></div><div id="distribution"></div><p class="distribution-status" id="distribution-status" aria-live="polite"></p>','表示は10文から数えた経験的な教師分布であり、学習済みモデルの出力ではない。有限のロジットによる softmax は厳密な0をとらない。');
  const distributions=[[0,0,0,.8,.2],[0,0,0,.2,.8],[0,0,1,0,0]],words=['Alice','Bob','likes','tea','coffee'];
  const distribution=document.getElementById('distribution');
  distribution.innerHTML=words.map(w=>`<div class="bar-row"><span>${w}</span><div class="bar-track"><div class="bar-fill"></div></div><span class="bar-value"></span></div>`).join('');
  function updateDistribution(index){document.querySelectorAll('[data-context]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.context)===index)));distributions[index].forEach((p,i)=>{distribution.children[i].querySelector('.bar-fill').style.width=p*100+'%';distribution.children[i].querySelector('.bar-value').textContent=p*100+'%'});document.getElementById('distribution-status').textContent=['Alice likes：5例中、tea が4例、coffee が1例。','Bob likes：5例中、tea が1例、coffee が4例。','Alice と Bob のどちらも、その直後は5例すべて likes。'][index]}
  document.querySelectorAll('[data-context]').forEach(b=>b.addEventListener('click',()=>updateDistribution(Number(b.dataset.context))));updateDistribution(0);
})();
