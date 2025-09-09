---
layout: default
title: Jasper Taal | Visualizations & Projects
---
<style>
  .hero-section {
    background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url("{{ '/assets/images/background.png' | relative_url }}");
    background-size: cover;
    background-position: center;
  }
  .card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
  }
  .card h3 {
    font-size: 1.3rem;
  }
  .card small {
    font-size: 0.85rem;
    color: #ddd;
  }
</style>

<div class="hero-section text-white">
  <div class="px-4 py-5 my-5 text-center">
    <h1 class="display-4 fw-bold">Visualizations & Projects</h1>
    <div class="col-lg-6 mx-auto">
      <p class="lead mb-4">A collection of interactive experiments and creative coding projects. Explore the intersection of data, art, and technology.</p>
    </div>
  </div>
</div>

<div class="container px-4 py-5" id="custom-cards">
  <h2 class="pb-2 border-bottom">Projects</h2>

  <div class="row row-cols-1 row-cols-lg-2 align-items-stretch g-4 py-5">
    {% for post in site.data.posts %}
      <div class="col">
        {% if post.post_url %}
          <a href="{{ post.post_url | relative_url }}" class="text-decoration-none">
            <div class="card card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg" style="background-image: url('{{ post.thumbnail | relative_url }}'); background-size: cover; background-position: center;">
              <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1" style="background-color: rgba(0, 0, 0, 0.5);">
                <h3 class="pt-5 mt-5 mb-4 display-6 lh-1 fw-bold">{{ post.title }}</h3>
                <ul class="d-flex list-unstyled mt-auto"><li class="me-auto"><small>{{ post.description }}</small></li></ul>
              </div>
            </div>
          </a>
        {% elsif post.visualization_url %}
          <a href="{{ post.visualization_url | relative_url }}" class="text-decoration-none">
            <div class="card card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg" style="background-image: url('{{ post.thumbnail | relative_url }}'); background-size: cover; background-position: center;">
              <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1" style="background-color: rgba(0, 0, 0, 0.5);">
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
            <div class="card card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg" style="background-image: url('{{ project.thumbnail | relative_url }}'); background-size: cover; background-position: center;">
              <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1" style="background-color: rgba(0, 0, 0, 0.5);">
                <h3 class="pt-5 mt-5 mb-4 display-6 lh-1 fw-bold">{{ project.title }}</h3>
                <ul class="d-flex list-unstyled mt-auto"><li class="me-auto"><small>{{ project.description }}</small></li></ul>
              </div>
            </div>
          </a>
        {% elsif project.visualization_url %}
          <a href="{{ project.visualization_url | relative_url }}" class="text-decoration-none">
            <div class="card card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg" style="background-image: url('{{ project.thumbnail | relative_url }}'); background-size: cover; background-position: center;">
              <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1" style="background-color: rgba(0, 0, 0, 0.5);">
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