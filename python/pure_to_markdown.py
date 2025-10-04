from pathlib import Path

# --- Paths ---
visualisations_dir = Path("_visualizations")        # output folder for .md frontmatter
pure_html_dir = visualisations_dir / "pure"         # raw html input

print("🚀 Starting Markdown generation...")
print(f"📂 Looking for HTML in: {pure_html_dir.resolve()}")

# Track totals
processed = 0
errors = 0

# --- Step: Process HTML files and generate .md frontmatter ---
for html_file in pure_html_dir.glob("*.html"):
    print(f"\n🔍 Processing {html_file.name}...")
    title = html_file.stem.replace('-', ' ').title()

    project = {
        "title": title,
        "author": "Jasper Taal",
        "thumbnail": f"/assets/images/{html_file.stem}.png",
        "visualization_url": f"/visualisations/{html_file.stem}.html",
        "full_url": f"https://jtaal.github.io/visualisations/{html_file.stem}.html",
        "description": f"An interactive visualization of {title}.",
    }

    # --- Always overwrite .md file with frontmatter ---
    try:
        md_file = visualisations_dir / f"{html_file.stem}.md"
        md_frontmatter = f"""---
layout: visualization
title: "{project['title']}"
author: {project['author']}
description: "{project['description']}"
visualization_url: {project['visualization_url']}
---
"""
        md_file.write_text(md_frontmatter, encoding="utf-8")
        print(f"  ✅ Wrote MD frontmatter: {md_file}")
        processed += 1
    except Exception as e:
        print(f"  ❌ ERROR writing MD for {html_file.name}: {e}")
        errors += 1

print("\n🏁 Done!")
print(f"📊 Summary: {processed} Markdown files created, {errors} errors.")
