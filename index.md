---
layout: default
title: Home
---
<style>
  .hero-section {
    background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url("{{ '/assets/images/background.jpg' | relative_url }}");
    background-size: cover;
    background-position: center;
  }
</style>

<!-- Bootstrap 5 Hero Section with Background Image -->
<div class="hero-section text-white">
  <div class="px-4 py-5 my-5 text-center">
    <h1 class="display-4 fw-bold">Visualizations & Projects</h1>
    <div class="col-lg-6 mx-auto">
      <p class="lead mb-4">A collection of interactive experiments and creative coding projects. Explore the intersection of data, art, and technology.</p>
    </div>
  </div>
</div>

<!-- Main Content Area -->
<div class="container px-4 py-5" id="custom-cards">
  <h2 class="pb-2 border-bottom">Projects</h2>

  <!-- Project Grid (This part stays the same, reading from _data/projects.yml) -->
  <div class="row row-cols-1 row-cols-lg-2 align-items-stretch g-4 py-5">
    {% for project in site.data.projects %}
      <div class="col">
        {% if project.url %}
          <a href="{{ project.url | relative_url }}" class="text-decoration-none">
            <div class="card card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg" style="background-image: url('{{ project.thumbnail | relative_url }}'); background-size: cover; background-position: center;">
              <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1" style="background-color: rgba(0, 0, 0, 0.5);">
                <h3 class="pt-5 mt-5 mb-4 display-6 lh-1 fw-bold">{{ project.title }}</h3>
                <ul class="d-flex list-unstyled mt-auto"><li class="me-auto"><small>{{ project.description }}</small></li></ul>
              </div>
            </div>
          </a>
        {% else %}
          <div class="card card-cover h-100 overflow-hidden text-bg-secondary rounded-4 shadow-lg" style="opacity: 0.7;"><!-- content for disabled card --></div>
        {% endif %}
      </div>
    {% endfor %}
  </div>

  <!-- How to Cite Section -->
  <h2 class="pt-4 mt-4 pb-2 border-bottom">How to Cite</h2>
  <p>If you find the content on this website useful for your research or work, please consider citing it. You can use the following BibTeX entry:</p>
  <pre class="bg-dark text-white p-3 rounded-3"><code>@misc{YourLastNameWebsite{{ "now" | date: "%Y" }},
  author = {Your Name},
  title  = {Visualizations & Projects},
  year   = {2025},
  url    = {https://jtaal.github.io/}
}</code></pre>

</div>