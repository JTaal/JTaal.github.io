---
layout: default
title: Jasper Taal | Visualizations & Projects
---

<style>
@import url('https://www.google.com/search?q=https://fonts.googleapis.com/css2%3Ffamily%3DOrbitron:wght%40700%26display%3Dswap');
body {
background-color: #111827;
font-family: 'Inter', sans-serif;
}
/* 3D Viewer Styles */
#three-container {
position: relative;
width: 100%;
height: 60vh;
background-color: #000;
overflow: hidden;
color: white;
display: flex;
align-items: center;
justify-content: center;
text-align: center;
}
#three-canvas {
position: absolute;
top: 0;
left: 0;
width: 100%;
height: 100%;
z-index: 1;
}
#viewer-overlay {
position: relative;
z-index: 10;
display: flex;
flex-direction: column;
align-items: center;
justify-content: center;
padding: 2rem;
background: rgba(0,0,0,0.2);
backdrop-filter: blur(2px);
border-radius: 1rem;
}
#logo-placeholder {
width: 80px;
height: 80px;
margin-bottom: 20px;
background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' fill='none' stroke='%23ffffff' stroke-width='4'%3E%3Cpath d='M50 10 L61.8 38.2 L90.5 38.2 L69.3 55.9 L78.8 85 L50 66.9 L21.2 85 L30.7 55.9 L9.5 38.2 L38.2 38.2 Z'/%3E%3C/svg%3E");
background-size: 60%;
background-repeat: no-repeat;
background-position: center;
border: 2px solid rgba(255,255,255,0.5);
border-radius: 50%;
}
#skytales-title {
font-size: 4.5rem;
font-family: 'Orbitron', sans-serif;
font-weight: 700;
text-transform: uppercase;
background: linear-gradient(45deg, #ff8a00, #e52e71, #9c27b0);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
text-shadow: 0 0 15px rgba(255, 107, 0, 0.5), 0 0 25px rgba(229, 46, 113, 0.4);
margin: 0;
}
#viewer-overlay .lead {
max-width: 600px;
color: #d1d5db;
}
/* Original Styles */
#dna-strip-container {
width: 100%;
height: 80px;
background: black;
overflow: hidden;
position: relative;
}
#dna-canvas {
width: 100%;
height: 100%;
display: block;
}
#gene-info {
width: 100%;
text-align: center;
padding: 8px 0;
background-color: #1f2937;
color: #d1d5db;
font-family: "Courier New", monospace;
font-size: 0.9rem;
border-top: 1px solid #374151;
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
<!-- 3D Viewer -->
<div id="three-container">
<canvas id="three-canvas"></canvas>
<div id="viewer-overlay">
<div id="logo-placeholder"></div>
<h1 id="skytales-title">SkyTales</h1>
<p class="lead mb-4 mt-3">
Our sky tells the story of infinite possibility constrained to reality.
</p>
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
<!-- DNA strip -->
<div id="dna-strip-container">
<canvas id="dna-canvas"></canvas>
</div>
<div id="gene-info">Fetching gene data...</div>
<!-- Scripts -->
<script src="https://www.google.com/search?q=https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
// Three.js Starfield Animation
const threeContainer = document.getElementById('three-container');
const threeCanvas = document.getElementById('three-canvas');
if (threeContainer && threeCanvas) {
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, threeContainer.offsetWidth / threeContainer.offsetHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas: threeCanvas, antialias: true, alpha: true });
renderer.setSize(threeContainer.offsetWidth, threeContainer.offsetHeight);
renderer.setClearColor(0x000000, 1);

camera.position.z = 5;

const starGeo = new THREE.BufferGeometry();
const starVertices = [];
for (let i = 0; i &lt; 10000; i++) {
    const x = (Math.random() - 0.5) * 2000;
    const y = (Math.random() - 0.5) * 2000;
    const z = (Math.random() - 0.5) * 2000;
    starVertices.push(x, y, z);
}
starGeo.setAttribute(&#39;position&#39;, new THREE.Float32BufferAttribute(starVertices, 3));

const starMaterial = new THREE.PointsMaterial({
    color: 0xffffff,
    size: 0.7,
    transparent: true
});

const stars = new THREE.Points(starGeo, starMaterial);
scene.add(stars);

function onWindowResize() {
    camera.aspect = threeContainer.offsetWidth / threeContainer.offsetHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(threeContainer.offsetWidth, threeContainer.offsetHeight);
}
window.addEventListener(&#39;resize&#39;, onWindowResize, false);

function animateStars() {
    requestAnimationFrame(animateStars);
    stars.rotation.x += 0.0001;
    stars.rotation.y += 0.0002;
    renderer.render(scene, camera);
}

animateStars();

}
</script>
<script>
// DNA Animation Script
const canvas = document.getElementById("dna-canvas");
const ctx = canvas.getContext("2d");
canvas.width = canvas.offsetWidth;
canvas.height = canvas.offsetHeight;
const bases = ["A","T","C","G"];
const colors = { A: "red", T: "blue", C: "gold", G: "violet" };
const NUCLEOTIDE_SPACING = 40;
let dnaSeq = "";
let dnaIndex = 0;
let letters = [];
async function fetchGene() {
try {
const genes=[{id:"NM_007294.4",sym:"BRCA1"},{id:"NM_000546.6",sym:"TP53"}];
const g=genes[Math.floor(Math.random()*genes.length)];
document.getElementById("gene-info").textContent=Fetching ${g.sym}...;
const url=https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&amp;id=${g.id}&amp;rettype=fasta&amp;retmode=text;
const r=await fetch(url);
if(!r.ok) throw new Error();
const fasta=await r.text();
dnaSeq=fasta.split("\n").slice(1).join("").replace(/[^ATCG]/g,"");
document.getElementById("gene-info").textContent=Visualizing ${g.sym};
} catch {
dnaSeq=Array.from({length:1000},()=>bases[Math.floor(Math.random()*4)]).join("");
document.getElementById("gene-info").textContent="Fallback: Random DNA";
}
}
function nextBase() {
return dnaSeq[dnaIndex++ % dnaSeq.length];
}
function spawnLetter() {
const b = nextBase();
const pair = {A:"T",T:"A",C:"G",G:"C"}[b];
const x = canvas.width + 20;
letters.push({base:b, x, y:20, color:colors[b]});
letters.push({base:pair, x, y:60, color:colors[pair]});
}
function draw() {
ctx.clearRect(0,0,canvas.width,canvas.height);
ctx.font="bold 28px monospace";
ctx.textAlign="center";
ctx.textBaseline="middle";
letters.forEach(l=>{
ctx.fillStyle=l.color;
ctx.fillText(l.base,l.x,l.y);
l.x -= 2; // speed
});
letters = letters.filter(l=>l.x > -20);
}
function animateDna() {
const lastLetter = letters[letters.length - 1];
if (!lastLetter || lastLetter.x < canvas.width - NUCLEOTIDE_SPACING) {
spawnLetter();
}
draw();
requestAnimationFrame(animateDna);
}
fetchGene().then(()=> animateDna());
</script>
<script>
// Search Script
document.addEventListener("DOMContentLoaded", function () {
const search=document.getElementById("search");
const cards=document.querySelectorAll("#custom-cards .col"); // Target the column for hiding
search.addEventListener("input",function(){
const q=this.value.toLowerCase();
cards.forEach(cardContainer=>{
const text=cardContainer.innerText.toLowerCase();
cardContainer.style.display=text.includes(q)?"":"none";
});
});
});
</script>
