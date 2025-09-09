---
layout: default
title: Jasper Taal | Visualizations & Projects
---

<!-- DNA Banner -->
<div id="dna-strip-container">
  <canvas id="bg-canvas"></canvas>
</div>
<div id="gene-info">Fetching gene data...</div>

<style>
  body {
    background-color: #111827;
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
</style>

<!-- Hero section (unchanged) -->
<div class="hero-section text-white">
  <div class="px-4 py-5 my-5 text-center">
    <h1 class="display-4 fw-bold">Our sky tells the story of infinite possibility, constrained to reality</h1>
    <div class="col-lg-6 mx-auto">
      <p class="lead mb-4">A collection of interactive experiments and creative coding projects. Explore the intersection of data, art, and technology.</p>
    </div>
  </div>
</div>

<div class="container px-4 py-5" id="custom-cards">
  <!-- Search -->
  <h2 class="pb-2 border-bottom">Projects</h2>
  <input id="search" class="form-control my-4" placeholder="Search projects or visualisations...">

  <script>
    document.addEventListener("DOMContentLoaded", function () {
      const search = document.getElementById("search");
      const cards = document.querySelectorAll("#custom-cards .card");
      search.addEventListener("input", function () {
        const q = this.value.toLowerCase();
        cards.forEach(card => {
          const text = card.innerText.toLowerCase();
          card.parentElement.style.display = text.includes(q) ? "" : "none";
        });
      });
    });
  </script>

  <!-- Existing Projects loop -->
  <div class="row row-cols-1 row-cols-lg-2 align-items-stretch g-4 py-5">
    {% for post in site.data.posts %}
      <div class="col">
        {% if post.post_url %}
          <a href="{{ post.post_url | relative_url }}" class="text-decoration-none">
            <div class="card card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg"
                 style="background-image: url('{{ post.thumbnail | relative_url }}'); background-size: cover; background-position: center;">
              <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1"
                   style="background-color: rgba(0, 0, 0, 0.5);">
                <h3 class="pt-5 mt-5 mb-4 display-6 lh-1 fw-bold">{{ post.title }}</h3>
                <ul class="d-flex list-unstyled mt-auto">
                  <li class="me-auto"><small>{{ post.description }}</small></li>
                </ul>
              </div>
            </div>
          </a>
        {% elsif post.visualization_url %}
          <a href="{{ post.visualization_url | relative_url }}" class="text-decoration-none">
            <div class="card card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg"
                 style="background-image: url('{{ post.thumbnail | relative_url }}'); background-size: cover; background-position: center;">
              <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1"
                   style="background-color: rgba(0, 0, 0, 0.5);">
                <h3 class="pt-5 mt-5 mb-4 display-6 lh-1 fw-bold">{{ post.title }}</h3>
              </div>
            </div>
          </a>
        {% else %}
          <div class="card card-cover h-100 overflow-hidden text-bg-secondary rounded-4 shadow-lg" style="opacity: 0.7;"></div>
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
                   style="background-color: rgba(0, 0, 0, 0.5);">
                <h3 class="pt-5 mt-5 mb-4 display-6 lh-1 fw-bold">{{ project.title }}</h3>
                <ul class="d-flex list-unstyled mt-auto">
                  <li class="me-auto"><small>{{ project.description }}</small></li>
                </ul>
              </div>
            </div>
          </a>
        {% elsif project.visualization_url %}
          <a href="{{ project.visualization_url | relative_url }}" class="text-decoration-none">
            <div class="card card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg"
                 style="background-image: url('{{ project.thumbnail | relative_url }}'); background-size: cover; background-position: center;">
              <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1"
                   style="background-color: rgba(0, 0, 0, 0.5);">
                <h3 class="pt-5 mt-5 mb-4 display-6 lh-1 fw-bold">{{ project.title }}</h3>
              </div>
            </div>
          </a>
        {% else %}
          <div class="card card-cover h-100 overflow-hidden text-bg-secondary rounded-4 shadow-lg" style="opacity: 0.7;"></div>
        {% endif %}
      </div>
    {% endfor %}
  </div>

  {% include how-to-cite.html %}
</div>

<!-- Scripts for DNA banner -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
  document.addEventListener("DOMContentLoaded", function () {
    // simplified init: scrolling A/T/C/G background
    let scene, camera, renderer, letters = [];
    const container = document.getElementById('dna-strip-container');
    const geneInfoDiv = document.getElementById('gene-info');
    const bases = ['A','T','C','G'];
    const colors = { A:'red',T:'blue',C:'yellow',G:'purple' };

    function createTexture(text, color) {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = 64; canvas.height = 64;
      ctx.fillStyle = color;
      ctx.font = "bold 48px Courier";
      ctx.textAlign = "center"; ctx.textBaseline = "middle";
      ctx.fillText(text, 32, 32);
      return new THREE.CanvasTexture(canvas);
    }

    function createSprite(base) {
      const tex = createTexture(base, colors[base]);
      const mat = new THREE.SpriteMaterial({ map: tex, transparent: true });
      const s = new THREE.Sprite(mat);
      s.scale.set(20,20,1);
      return s;
    }

    function init() {
      scene = new THREE.Scene();
      const w = container.clientWidth, h = container.clientHeight;
      camera = new THREE.OrthographicCamera(-w/2,w/2,h/2,-h/2,1,1000);
      camera.position.z = 10;
      renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('bg-canvas'), alpha:true });
      renderer.setSize(w,h);
      for(let i=0;i<50;i++){
        const base = bases[Math.floor(Math.random()*4)];
        const sprite = createSprite(base);
        sprite.position.set(i*30 - w/2,0,0);
        letters.push(sprite);
        scene.add(sprite);
      }
      animate();
      geneInfoDiv.textContent = "DNA visual banner running...";
    }

    function animate() {
      requestAnimationFrame(animate);
      letters.forEach(l => {
        l.position.x -= 1;
        if(l.position.x < -container.clientWidth/2-30){
          l.position.x += container.clientWidth+30;
        }
      });
      renderer.render(scene,camera);
    }

    init();
    window.addEventListener("resize", () => location.reload());
  });
</script>
