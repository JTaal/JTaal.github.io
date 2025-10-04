from pathlib import Path
import yaml
import re

# --- Paths ---
posts_dir = Path("_posts")
visualizations_dir = Path("_visualizations")
posts_file = Path("_data/posts.yml")
projects_file = Path("_data/projects.yml")

# --- Template for the Jekyll include block ---
# This will be inserted into each HTML file.
# Note: The double curly braces {{ and }} are used to escape the Liquid syntax
# for Python's .format() method.
JEKYLL_INCLUDE_TEMPLATE = """
    {{% comment %}} --- Jekyll Social Meta Include --- {{% endcomment %}}
    {{%- assign page_title = "{title}" -%}}
    {{%- assign viz_data = site.data.projects | where: "title", page_title | first -%}}
    {{%- if viz_data -%}}
      {{% include social-meta.html
          title=viz_data.title
          description=viz_data.description
          thumbnail=viz_data.thumbnail
          full_url=viz_data.full_url
      %}}
    {{%- endif -%}}
    {{% comment %}} --- End Include --- {{% endcomment %}}
</head>
"""


# --- Step 1: Process posts ---
posts = []

for md_file in posts_dir.glob("*.md"):
    with open(md_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if lines and lines[0].strip() == "---":
        fm_lines = []
        for line in lines[1:]:
            if line.strip() == "---":
                break
            fm_lines.append(line)

        front_matter = yaml.safe_load("".join(fm_lines)) or {}

        title = front_matter.get("title", md_file.stem.replace("-", " ").title())
        visualization_url = front_matter.get("visualization_url")
        description = front_matter.get("description", "")
        date = str(front_matter.get("date", ""))

        # Build post_url from date + slug
        slug = md_file.stem.split("-", 3)[-1]
        post_url = None
        if date and len(date.split("-")) >= 3:
            y, m, d = date.split("-")[:3]
            post_url = f"/{y}/{m}/{d}/{slug}.html"

        # Thumbnail from visualization filename if available
        if visualization_url:
            vis_name = Path(visualization_url).stem
            thumbnail = f"/assets/images/{vis_name}.png"
        else:
            thumbnail = f"/assets/images/{slug}.png"

        post_entry = {
            "title": title,
            "author": "Jasper Taal",  # default
            "thumbnail": thumbnail,
            "post_url": post_url,
            "visualization_url": visualization_url,
            "description": description,
        }
        posts.append(post_entry)

# Sort posts alphabetically
posts.sort(key=lambda p: p["title"])

# Step 2: Write posts.yml (one entry per block, blank line between)
with open(posts_file, "w", encoding="utf-8") as f:
    for post in posts:
        yaml.dump([post], f, sort_keys=False, allow_unicode=True)
        f.write("\n")

print(f"✅ Generated {len(posts)} post entries in {posts_file}")

# --- Step 3: Process projects AND MODIFY HTML FILES ---
projects = []

for f in visualizations_dir.glob("*.html"):
    title = f.stem.replace('-', ' ').title()
    project = {
        "title": title,
        "author": "Jasper Taal",
        "thumbnail": f"/assets/images/{f.stem}.png",
        "visualization_url": f"/visualizations/{f.name}",
        "full_url": f"https://jtaal.github.io/visualizations/{f.name}",
        # Adding a default description for the meta tags
        "description": f"An interactive visualization of {title}.",
    }
    projects.append(project)

    # --- NEW: Modify the HTML file to include the Jekyll code ---
    try:
        html_content = f.read_text(encoding="utf-8")

        # Check if our comment block already exists to prevent duplicates
        if "--- Jekyll Social Meta Include ---" not in html_content:
            
            # Prepare the specific include block for this file
            jekyll_block_to_insert = JEKYLL_INCLUDE_TEMPLATE.format(title=title)

            # Use regex to replace the </head> tag safely
            # This is more robust than a simple string replace
            new_html_content, num_replacements = re.subn(
                r"</head>",
                jekyll_block_to_insert,
                html_content,
                flags=re.IGNORECASE
            )

            if num_replacements > 0:
                f.write_text(new_html_content, encoding="utf-8")
                print(f"  -> Injected meta tags into {f.name}")
            else:
                 print(f"  -> WARNING: Could not find </head> tag in {f.name}")

    except Exception as e:
        print(f"  -> ERROR processing {f.name}: {e}")


# Sort projects alphabetically
projects.sort(key=lambda p: p["title"])

# Step 4: Write projects.yml (one entry per block, blank line between)
with open(projects_file, "w", encoding="utf-8") as f:
    for project in projects:
        yaml.dump([project], f, sort_keys=False, allow_unicode=True)
        f.write("\n") # blank line between entries

print(f"✅ Generated {len(projects)} project entries in {projects_file}")

