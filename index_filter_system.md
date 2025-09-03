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

  /* --- NEW STYLES for Filter Controls & Cards --- */
  .filter-controls {
    list-style: none;
    padding: 0;
    margin-bottom: 2rem;
  }
  .filter-controls li {
    cursor: pointer;
    padding: 0.5rem 1.25rem;
    margin: 0.25rem;
    border: 1px solid var(--bs-border-color);
    border-radius: 999px; /* Pill shape */
    transition: all 0.2s ease-in-out;
  }
  .filter-controls li:hover {
    background-color: var(--bs-secondary-bg);
  }
  .filter-controls li.active {
    background-color: var(--bs-primary);
    color: var(--bs-light);
    border-color: var(--bs-primary);
  }

  .portfolio-item {
    transition: transform 0.3s ease, opacity 0.3s ease;
  }
  
  .portfolio-item.hide {
    transform: scale(0.9);
    opacity: 0;
    /* We use visibility and height to remove it from the layout flow */
    visibility: hidden;
    height: 0;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    margin-top: 0 !important;
    margin-bottom: 0 !important;
  }
  
  .card-tags {
    position: absolute;
    top: 1rem;
    left: 1rem;
    z-index: 10;
  }
  
  .card-tag {
    backdrop-filter: blur(5px);
    background-color: rgba(255, 255, 255, 0.15);
  }

</style>

<!-- Hero Section (No change) -->
<div class="hero-section text-white">
  <div class="px-4 py-5 my-5 text-center">
    <h1 class="display-4 fw-bold">Creative Portfolio</h1>
    <div class="col-lg-6 mx-auto">
      <p class="lead mb-4">A collection of interactive experiments and creative coding projects. Explore the intersection of data, art, and technology.</p>
    </div>
  </div>
</div>

<div class="container px-4 py-5">

  <!-- NEW: Filter Controls -->
  <div class="d-flex justify-content-center flex-wrap">
    <ul class="filter-controls d-flex flex-wrap justify-content-center">
      <li class="active" data-filter="all">All</li>
      <li data-filter="project">Project</li>
      <li data-filter="visualization">Visualization</li>
      <!-- You can add more filters here based on your tags! -->
    </ul>
  </div>

  <!-- {% comment %}
    1. Merge posts and projects into a single array called `allItems`.
    2. We'll add a 'type' to each so we can filter them.
  {% endcomment %} -->
  {% assign allItems = "" | split: "" %}

  {% for project in site.data.projects %}
    {% assign project_item = project | merge: { "type": "visualization" } %}
    {% assign allItems = allItems | push: project_item %}
  {% endfor %}

  {% for post in site.posts %}
    {% assign post_item = post | merge: { "type": "project" } %}
    {% assign allItems = allItems | push: post_item %}
  {% endfor %}

  <!-- Unified Portfolio Grid -->
  <div id="portfolio-grid" class="row row-cols-1 row-cols-md-2 align-items-stretch g-4 py-5">
    
    {% for item in allItems %}
      <div class="col portfolio-item" data-category="{{ item.type }}">
        <a href="{{ item.post_url | default: item.visualization_url | relative_url }}" class="text-decoration-none">
          <div class="card card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg">
            
            <!-- NEW: Tags for each card -->
            <div class="card-tags">
              <span class="badge rounded-pill card-tag p-2 px-3 text-white text-uppercase">{{ item.type }}</span>
            </div>

            <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1" style="background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.8)), url('{{ item.thumbnail | relative_url }}'); background-size: cover; background-position: center;">
              <h3 class="pt-5 mt-5 mb-4 display-6 lh-1 fw-bold">{{ item.title }}</h3>
              <ul class="d-flex list-unstyled mt-auto">
                <li class="me-auto"><small>{{ item.description }}</small></li>
              </ul>
            </div>
          </div>
        </a>
      </div>
    {% endfor %}
  </div>

  <!-- Citation Section (No change) -->
  {% include how-to-cite.html %}
</div>

<!-- NEW: JavaScript for Filtering -->
<script>
document.addEventListener('DOMContentLoaded', function() {
  const filterControls = document.querySelector('.filter-controls');
  const portfolioItems = document.querySelectorAll('.portfolio-item');

  filterControls.addEventListener('click', function(e) {
    if (e.target.tagName !== 'LI') return;

    // Update active button state
    filterControls.querySelector('.active').classList.remove('active');
    e.target.classList.add('active');

    const filterValue = e.target.getAttribute('data-filter');

    // Show/Hide items based on filter
    portfolioItems.forEach(item => {
      const itemCategory = item.getAttribute('data-category');
      if (filterValue === 'all' || filterValue === itemCategory) {
        item.classList.remove('hide');
      } else {
        item.classList.add('hide');
      }
    });
  });
});
</script>
