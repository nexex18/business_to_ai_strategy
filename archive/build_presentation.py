#!/usr/bin/env python3
"""
Build script for VMG Presentation
This script assembles individual slide files into a complete presentation
"""

import json
import os
from pathlib import Path

def load_manifest(manifest_path):
    """Load the slides manifest JSON file"""
    with open(manifest_path, 'r') as f:
        return json.load(f)

def read_file(filepath):
    """Read content from a file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def build_presentation():
    """Main function to build the presentation"""
    
    # Set up paths
    base_dir = Path(__file__).parent
    manifest_path = base_dir / "slides_manifest.json"
    slides_dir = base_dir / "slides"
    output_path = base_dir / "presentation.html"
    
    # Load manifest
    manifest = load_manifest(manifest_path)
    
    # Read template files
    header_template = read_file(base_dir / "templates" / "header.html")
    footer_template = read_file(base_dir / "templates" / "footer.html")
    
    # Start building the presentation
    presentation_html = header_template
    
    # Add each slide
    active_slides = [s for s in manifest['slides'] if s.get('active', True)]
    
    for i, slide in enumerate(active_slides, 1):
        slide_path = slides_dir / slide['file']
        if slide_path.exists():
            slide_content = read_file(slide_path)
            # Update slide number in the content
            slide_content = slide_content.replace('{{SLIDE_NUMBER}}', str(i))
            presentation_html += f"\n<!-- Slide {i}: {slide['title']} -->\n"
            presentation_html += slide_content + "\n"
        else:
            print(f"Warning: Slide file not found: {slide['file']}")
    
    # Update total slides count in footer
    footer_template = footer_template.replace('{{TOTAL_SLIDES}}', str(len(active_slides)))
    
    # Add footer
    presentation_html += footer_template
    
    # Write the complete presentation
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(presentation_html)
    
    print(f"✅ Presentation built successfully!")
    print(f"   Total slides: {len(active_slides)}")
    print(f"   Output file: {output_path}")
    
    # List any inactive slides
    inactive_slides = [s for s in manifest['slides'] if not s.get('active', True)]
    if inactive_slides:
        print(f"   Inactive slides: {len(inactive_slides)}")
        for slide in inactive_slides:
            print(f"     - {slide['title']}")

if __name__ == "__main__":
    build_presentation()
