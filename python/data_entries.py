from pathlib import Path
import yaml

visualizations_dir = Path("_visualizations")
output_file = Path("_data/projects.yml")

projects = []

for f in visualizations_dir.glob("*.html"):
    # Generate a title from the filename
    title = f.stem.replace('-', ' ').title()
    
    # Create the half-baked entry
    project = {
        "title": title,
        "author": "Jasper Taal",
        "thumbnail": f"/assets/images/{f.stem}.png",
        "post_url": None,
        "visualization_url": f"/visualizations/{f.name}",
        "description": "A short description goes here."
    }
    
    projects.append(project)

# Write each entry with a blank line after it
with open(output_file, "w") as f:
    for project in projects:
        yaml.dump([project], f, sort_keys=False)
        f.write("\n")  # blank line between entries

print(f"Generated {len(projects)} project entries in {output_file}")
