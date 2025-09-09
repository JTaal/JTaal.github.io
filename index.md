---
layout: default
title: Jasper Taal | Visualizations & Projects
---
<style>
  body {
    background-color: #111827;
    font-family: 'Inter', sans-serif;
  }
  .hero-section {
    background-image: linear-gradient(rgba(0,0,0,0.6),rgba(0,0,0,0.6)), 
      url("{{ '/assets/images/background.png' | relative_url }}");
    background-size: cover;
    background-position: center;
  }
  #dna-strip-container {
    width: 100%;
    height: 80px;
    background-color: #000;
    overflow: hidden;
    position: relative;
  }
  #bg-canvas {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
  }
  #gene-info {
    width: 100%;
    text-align: center;
    padding: 8px 0;
    background-color: #1f2937;
    color: #d1d5db;
    font-family: "Courier New", monospace;
    font-size: 0.9rem;
    border-bottom: 1px solid #374151;
    z-index: 10;
  }
  .card {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
  }
  .card h3 { font-size: 1.3rem; }
  .card small { font-size: 0.85rem; color: #ddd; }
</style>

<!-- DNA strip -->
<div id="dna-strip-container"><canvas id="bg-canvas"></canvas></div>
<div id="gene-info">Fetching gene data...</div>

<!-- Hero -->
<div class="hero-section text-white">
  <div class="px-4 py-5 my-5 text-center">
    <h1 class="display-4 fw-bold">Visualizations & Projects</h1>
    <div class="col-lg-6 mx-auto">
      <p class="lead mb-4">A collection of interactive experiments and creative coding projects. Explore the intersection of data, art, and technology.</p>
    </div>
  </div>
</div>

<!-- Projects + Visualisations -->
<div class="container px-4 py-5" id="custom-cards">
  <h2 class="pb-2 border-bottom">Projects</h2>
  <input id="search" class="form-control my-4" placeholder="Search projects or visualisations...">

  <div class="row row-cols-1 row-cols-lg-2 align-items-stretch g-4 py-5">
    {% for post in site.data.posts %}
      <div class="col">
        {% if post.post_url %}
          <a href="{{ post.post_url | relative_url }}" class="text-decoration-none">
            <div class="card card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg" 
              style="background-image: url('{{ post.thumbnail | relative_url }}'); background-size: cover; background-position: center;">
              <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1" 
                style="background-color: rgba(0,0,0,0.5);">
                <h3 class="pt-5 mt-5 mb-4 display-6 lh-1 fw-bold">{{ post.title }}</h3>
                <ul class="d-flex list-unstyled mt-auto"><li class="me-auto"><small>{{ post.description }}</small></li></ul>
              </div>
            </div>
          </a>
        {% elsif post.visualization_url %}
          <a href="{{ post.visualization_url | relative_url }}" class="text-decoration-none">
            <div class="card card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg" 
              style="background-image: url('{{ post.thumbnail | relative_url }}'); background-size: cover; background-position: center;">
              <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1" 
                style="background-color: rgba(0,0,0,0.5);">
                <h3 class="pt-5 mt-5 mb-4 display-6 lh-1 fw-bold">{{ post.title }}</h3>
              </div>
            </div>
          </a>
        {% endif %}
      </div>
    {% endfor %}
  </div>

  <h2 class="pb-2 border-bottom">Visualisations</h2>
  <div class="row row-cols-1 row-cols-lg-2 align-items-stretch g-4 py-5">
    {% for project in site.data.projects %}
      <div class="col">
        {% if project.post_url %}
          <a href="{{ project.post_url | relative_url }}" class="text-decoration-none">
            <div class="card card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg" 
              style="background-image: url('{{ project.thumbnail | relative_url }}'); background-size: cover; background-position: center;">
              <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1" 
                style="background-color: rgba(0,0,0,0.5);">
                <h3 class="pt-5 mt-5 mb-4 display-6 lh-1 fw-bold">{{ project.title }}</h3>
                <ul class="d-flex list-unstyled mt-auto"><li class="me-auto"><small>{{ project.description }}</small></li></ul>
              </div>
            </div>
          </a>
        {% elsif project.visualization_url %}
          <a href="{{ project.visualization_url | relative_url }}" class="text-decoration-none">
            <div class="card card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg" 
              style="background-image: url('{{ project.thumbnail | relative_url }}'); background-size: cover; background-position: center;">
              <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1" 
                style="background-color: rgba(0,0,0,0.5);">
                <h3 class="pt-5 mt-5 mb-4 display-6 lh-1 fw-bold">{{ project.title }}</h3>
              </div>
            </div>
          </a>
        {% endif %}
      </div>
    {% endfor %}
  </div>

  {% include how-to-cite.html %}
</div>

<!-- Scripts -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
  const container = document.getElementById('dna-strip-container');
  const geneInfoDiv = document.getElementById('gene-info');
  let scene, camera, renderer, letters=[], dnaSeq="", dnaIndex=0;
  const bases = ['A','T','C','G'];
  const colors = {A:"red",T:"blue",C:"gold",G:"violet"};

  async function fetchGene() {
    const genes=[{id:"NM_007294.4",sym:"BRCA1"},{id:"NM_000546.6",sym:"TP53"}];
    try {
      const g=genes[Math.floor(Math.random()*genes.length)];
      geneInfoDiv.textContent=`Fetching: ${g.sym}...`;
      const url=`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=${g.id}&rettype=fasta&retmode=text`;
      const r=await fetch(url);
      if(!r.ok) throw new Error();
      const fasta=await r.text();
      dnaSeq=fasta.split("\n").slice(1).join("").replace(/[^ATCG]/g,"");
      geneInfoDiv.textContent=`Visualizing ${g.sym}`;
    } catch {
      dnaSeq=Array.from({length:5000},()=>bases[Math.floor(Math.random()*4)]).join("");
      geneInfoDiv.textContent="Fallback: Random DNA";
    }
  }
  function sprite(base){
    const c=document.createElement("canvas"),ctx=c.getContext("2d");
    c.width=c.height=64; ctx.fillStyle=colors[base]; ctx.font="bold 48px monospace"; 
    ctx.textAlign="center"; ctx.textBaseline="middle"; ctx.fillText(base,32,32);
    return new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(c)}));
  }
  function initScene(){
    scene=new THREE.Scene();
    const w=container.clientWidth,h=container.clientHeight;
    camera=new THREE.OrthographicCamera(-w/2,w/2,h/2,-h/2,1,1000); camera.position.z=10;
    renderer=new THREE.WebGLRenderer({canvas:document.getElementById("bg-canvas"),alpha:true});
    renderer.setSize(w,h);
    const spacing=35, count=Math.ceil(w/spacing)+10;
    for(let i=0;i<count;i++){
      const top=sprite("A"), bottom=sprite("T");
      const x=i*spacing-(count*spacing/2);
      top.position.set(x,15,0); bottom.position.set(x,-15,0);
      top.userData.pair=bottom; bottom.userData.pair=top;
      setBase(top); scene.add(top,bottom); letters.push(top,bottom);
    }
    animate();
  }
  function setBase(top){
    if(!dnaSeq) return;
    const b=dnaSeq[dnaIndex++%dnaSeq.length], pair={A:"T",T:"A",C:"G",G:"C"}[b];
    update(top,b); update(top.userData.pair,pair);
  }
  function update(s,b){
    const tex=s.material.map.image.getContext?null:null;
    const c=document.createElement("canvas"),ctx=c.getContext("2d");
    c.width=c.height=64; ctx.fillStyle=colors[b]; ctx.font="bold 48px monospace";
    ctx.textAlign="center"; ctx.textBaseline="middle"; ctx.fillText(b,32,32);
    s.material.map=new THREE.CanvasTexture(c);
  }
  function animate(){
    requestAnimationFrame(animate);
    const w=container.clientWidth, spacing=35,total=(letters.length/2)*spacing;
    letters.forEach((l,i)=>{
      l.position.x-=0.4;
      if(l.position.x<-w/2-spacing){
        l.position.x+=total;
        if(l.position.y>0) setBase(l);
      }
    });
    renderer.render(scene,camera);
  }
  fetchGene().then(initScene);
</script>

<script>
  document.addEventListener("DOMContentLoaded", function () {
    const search=document.getElementById("search");
    const cards=document.querySelectorAll("#custom-cards .card");
    search.addEventListener("input",function(){
      const q=this.value.toLowerCase();
      cards.forEach(card=>{
        const text=card.innerText.toLowerCase();
        card.parentElement.style.display=text.includes(q)?"":"none";
      });
    });
  });
</script>
