---
layout: default
title: Home
---

<div class="px-4 py-5 my-5 text-center">
  <h1 class="display-4 fw-bold">Visualizations & Projects</h1>
  <div class="col-lg-6 mx-auto">
    <p class="lead mb-4">A collection of interactive experiments and creative coding projects. Explore the intersection of data, art, and technology.</p>
  </div>
</div>

<div class="container px-4 py-5" id="custom-cards">
  <h2 class="pb-2 border-bottom">Projects</h2>

  <div class="row row-cols-1 row-cols-lg-2 align-items-stretch g-4 py-5">
    
    <div class="col">
      <a href="{{ '/assets/visualizations/complex-chirp.html' | relative_url }}" class="text-decoration-none">
        <div class="card card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg" style="background-color: #1a2333 !important;">
          <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1">
            <h3 class="pt-5 mt-5 mb-4 display-6 lh-1 fw-bold">4D Complex Chirp</h3>
            <ul class="d-flex list-unstyled mt-auto">
              <li class="me-auto">
                <small>An interactive 3D visualization of a complex signal with linearly increasing frequency.</small>
              </li>
              <li class="d-flex align-items-center">
                <svg class="bi me-2" width="1em" height="1em"><use xlink:href="#arrow-right-circle"></use></svg>
                <small>View Visualization</small>
              </li>
            </ul>
          </div>
        </div>
      </a>
    </div>

    <div class="col">
       <div class="card card-cover h-100 overflow-hidden text-bg-secondary rounded-4 shadow-lg" style="opacity: 0.7;">
        <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1">
          <h3 class="pt-5 mt-5 mb-4 display-6 lh-1 fw-bold">Another Cool Project</h3>
          <ul class="d-flex list-unstyled mt-auto">
            <li class="me-auto">
               <small>A brief description of what this project will be about. Coming soon!</small>
            </li>
            <li class="d-flex align-items-center">
              <svg class="bi me-2" width="1em" height="1em"><use xlink:href="#clock"></use></svg>
              <small>Coming Soon</small>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <h2 class="pt-5 mt-5 pb-2 border-bottom">Recent Blog Posts</h2>

  <div class="list-group list-group-flush py-5">
    {% for post in site.posts limit:5 %}
      <a href="{{ post.url | relative_url }}" class="list-group-item list-group-item-action d-flex gap-3 py-3" aria-current="true">
        <div class="d-flex gap-2 w-100 justify-content-between">
          <div>
            <h6 class="mb-0">{{ post.title }}</h6>
          </div>
          <small class="opacity-50 text-nowrap">{{ post.date | date: "%B %d, %Y" }}</small>
        </div>
      </a>
    {% endfor %}
  </div>

</div>


<svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
  <symbol id="arrow-right-circle" viewBox="0 0 16 16">
    <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0zM4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5H4.5z"/>
  </symbol>
  <symbol id="clock" viewBox="0 0 16 16">
    <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/>
    <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"/>
  </symbol>
</svg>