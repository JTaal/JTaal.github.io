---
layout: default
title: Home
---

# Visualizations & Projects

A collection of interactive experiments and creative coding projects.

<div class="project-grid">

  <a href="{{ '/assets/visualizations/complex-chirp.html' | relative_url }}" class="project-card">
    <div class="card-image-placeholder" style="background-color: #1a2333;"></div>
    <h3>4D Complex Chirp</h3>
    <p>An interactive 3D visualization of a complex signal with linearly increasing frequency.</p>
    <span class="card-link">View Visualization &rarr;</span>
  </a>

  <div class="project-card-disabled">
    <div class="card-image-placeholder"></div>
    <h3>Another Cool Project</h3>
    <p>A brief description of what this project will be about. Coming soon!</p>
    <span class="card-link">Coming Soon</span>
  </div>

</div>

## Blog Posts

Here you can list your recent blog posts.
<ul class="post-list">
  {% for post in site.posts limit:5 %}
    <li>
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      <span class="post-date">{{ post.date | date: "%B %d, %Y" }}</span>
    </li>
  {% endfor %}
</ul>