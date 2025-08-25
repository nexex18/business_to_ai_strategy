#!/usr/bin/env python3
"""
Build a clean linked presentation from standalone slides
Each slide is a separate HTML page with navigation
Includes color-coded agenda sections in navigation
"""

import os
import shutil
import sqlite3
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

# Define agenda section colors (from orange/red to green gradient)
AGENDA_COLORS = {
    "Title": "#666",  # Neutral gray for title
    "Agenda": "#666",  # Neutral gray for agenda
    "VMG background": "#d73502",  # Dark red-orange
    "Competitive landscape": "#cb5a00",  # Orange
    "Internal assessment": "#bf7800",  # Dark orange
    "Opportunities": "#b39000",  # Yellow-orange
    "Business and AI strategies": "#97a000",  # Yellow-green
    "AI maturity": "#7aad00",  # Light green
    "AI initiatives": "#5cb600",  # Green
    "Financial analysis": "#3dbd00",  # Bright green
    "Timeline": "#1dc200",  # Bright green
    "Risks and mitigation strategies": "#00c624",  # Final green
    "Conclusion": "#00a31f"  # Darker green for conclusion
}

def load_slides_from_db():
    """Load slides configuration from SQLite database with agenda sections"""
    conn = sqlite3.connect('slides.db')
    cursor = conn.cursor()
    
    # Try to get agenda_section, fall back if it doesn't exist
    try:
        cursor.execute('SELECT num, name, title, source, agenda_section FROM slides ORDER BY num')
        has_agenda = True
    except:
        cursor.execute('SELECT num, name, title, source FROM slides ORDER BY num')
        has_agenda = False
    
    slides = []
    for row in cursor.fetchall():
        slide_dict = {
            'num': row[0],
            'name': row[1],
            'title': row[2],
            'source': row[3]
        }
        if has_agenda and len(row) > 4:
            slide_dict['agenda_section'] = row[4]
        else:
            slide_dict['agenda_section'] = 'General'
        slides.append(slide_dict)
    
    conn.close()
    return slides

# Load slides from database
SLIDES = load_slides_from_db()

def create_navigation(slide_index, total_slides):
    """Create navigation HTML for a slide with breadcrumb agenda sections"""
    current = SLIDES[slide_index]
    current_section = current.get('agenda_section', 'General')
    
    # Abbreviations for long section names
    section_abbreviations = {
        'Competitive landscape': 'Competition',
        'Business and AI strategies': 'Strategies',
        'Risks and mitigation strategies': 'Risks & Mitigation'
    }
    
    # Get unique agenda sections in order
    seen_sections = []
    agenda_sections = []
    for slide in SLIDES:
        section = slide.get('agenda_section', 'General')
        # Include all sections
        if section not in seen_sections:
            seen_sections.append(section)
            # Find first slide in this section for linking
            first_slide = next((s for s in SLIDES if s.get('agenda_section') == section), None)
            if first_slide:
                # Use abbreviated name if available
                display_name = section_abbreviations.get(section, section)
                agenda_sections.append({
                    'name': display_name,
                    'color': AGENDA_COLORS.get(section, '#666'),
                    'link': f'{first_slide["num"]}_{first_slide["name"]}.html',
                    'is_current': section == current_section
                })
    
    # Create breadcrumbs HTML
    breadcrumbs = []
    for i, section in enumerate(agenda_sections):
        if section['is_current']:
            breadcrumbs.append(f'<span class="breadcrumb-item active" style="background: {section["color"]};">{section["name"]}</span>')
        else:
            breadcrumbs.append(f'<a href="{section["link"]}" class="breadcrumb-item inactive">{section["name"]}</a>')
        
        # Add separator except for last item
        if i < len(agenda_sections) - 1:
            breadcrumbs.append('<span class="breadcrumb-separator">›</span>')
    
    breadcrumbs_html = ''.join(breadcrumbs)
    
    # Previous link
    if slide_index > 0:
        prev_slide = SLIDES[slide_index - 1]
        prev_link = f'<a href="{prev_slide["num"]}_{prev_slide["name"]}.html" class="nav-prev">← Previous</a>'
    else:
        prev_link = '<span class="nav-prev nav-disabled">← Previous</span>'
    
    # Next link
    if slide_index < total_slides - 1:
        next_slide = SLIDES[slide_index + 1]
        next_link = f'<a href="{next_slide["num"]}_{next_slide["name"]}.html" class="nav-next">Next →</a>'
    else:
        next_link = '<span class="nav-next nav-disabled">Next →</span>'
    
    # Find the agenda slide for linking
    agenda_slide = next((s for s in SLIDES if s.get('name') == 'agenda'), None)
    agenda_link = f'{agenda_slide["num"]}_{agenda_slide["name"]}.html' if agenda_slide else '02_agenda.html'
    
    # Navigation HTML with breadcrumbs
    nav_html = f'''
    <nav class="slide-navigation">
        <div class="nav-left">
            {prev_link}
        </div>
        <div class="nav-center">
            <span class="nav-counter">Slide {int(current["num"])} of {total_slides}</span>
            <div class="nav-breadcrumbs">
                <a href="../index.html" class="breadcrumb-item toc-item">TOC</a>
                <span class="breadcrumb-separator">›</span>
                {breadcrumbs_html}
            </div>
        </div>
        <div class="nav-right">
            {next_link}
        </div>
    </nav>
    '''
    
    return nav_html

def add_navigation_css():
    """CSS for the navigation bar with breadcrumb styling"""
    return '''
    <style>
        .slide-navigation {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 60px;
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            z-index: 1000;
            box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
        }
        
        .nav-left {
            display: flex;
            align-items: center;
            min-width: 120px;
        }
        
        .nav-center {
            display: flex;
            align-items: center;
            gap: 20px;
            flex: 1;
            justify-content: center;
        }
        
        .nav-right {
            display: flex;
            align-items: center;
            min-width: 120px;
            justify-content: flex-end;
        }
        
        .nav-prev, .nav-next {
            color: white;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 5px;
            transition: background 0.3s;
            font-weight: 600;
            font-size: 14px;
            white-space: nowrap;
        }
        
        .nav-prev:hover, .nav-next:hover {
            background: rgba(255, 255, 255, 0.1);
        }
        
        .nav-disabled {
            opacity: 0.3;
            cursor: not-allowed;
        }
        
        .nav-counter {
            color: rgba(255, 255, 255, 0.8);
            font-size: 13px;
            white-space: nowrap;
            margin-right: 15px;
        }
        
        .nav-breadcrumbs {
            display: flex;
            align-items: center;
            gap: 6px;
            flex-wrap: nowrap;
        }
        
        .breadcrumb-item {
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 10px;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s;
            white-space: nowrap;
        }
        
        .breadcrumb-item.active {
            color: white;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
        }
        
        .breadcrumb-item.inactive {
            background: rgba(128, 128, 128, 0.3);
            color: rgba(255, 255, 255, 0.6);
        }
        
        .breadcrumb-item.inactive:hover {
            background: rgba(128, 128, 128, 0.5);
            color: rgba(255, 255, 255, 0.9);
        }
        
        .breadcrumb-item.toc-item {
            background: rgba(102, 126, 234, 0.3);
            color: rgba(255, 255, 255, 0.9);
            font-weight: 700;
        }
        
        .breadcrumb-item.toc-item:hover {
            background: rgba(102, 126, 234, 0.5);
            color: white;
        }
        
        .breadcrumb-item.agenda-item {
            background: rgba(118, 75, 162, 0.3);
            color: rgba(255, 255, 255, 0.9);
            font-weight: 700;
        }
        
        .breadcrumb-item.agenda-item:hover {
            background: rgba(118, 75, 162, 0.5);
            color: white;
        }
        
        .breadcrumb-separator {
            color: rgba(255, 255, 255, 0.4);
            font-size: 12px;
            margin: 0 -3px;
        }
        
        /* Adjust slide container to account for navigation without affecting content */
        .presentation-container {
            height: 100vh;
            overflow: hidden;
        }
        
        .slide {
            height: calc(100vh - 60px);
            overflow-y: auto;
            padding-bottom: 20px;
        }
        
        /* Ensure header elements stay visible */
        .slide > h1:first-of-type,
        .slide > .subtitle,
        .slide > div[style*="height: 2px"] {
            position: relative;
            z-index: 1;
        }
        
        /* Responsive adjustments for smaller screens */
        @media (max-width: 1400px) {
            .nav-breadcrumbs {
                font-size: 10px;
            }
            .breadcrumb-item {
                padding: 3px 8px;
                font-size: 10px;
            }
        }
    </style>
    '''

def add_keyboard_navigation():
    """JavaScript for keyboard navigation"""
    return '''
    <script>
        document.addEventListener('keydown', function(e) {
            switch(e.key) {
                case 'ArrowLeft':
                    const prevLink = document.querySelector('.nav-prev:not(.nav-disabled)');
                    if (prevLink) prevLink.click();
                    break;
                case 'ArrowRight':
                case ' ':
                    e.preventDefault();
                    const nextLink = document.querySelector('.nav-next:not(.nav-disabled)');
                    if (nextLink) nextLink.click();
                    break;
                case 'Home':
                    e.preventDefault();
                    document.querySelector('.nav-home').click();
                    break;
                case 'f':
                case 'F':
                    if (document.fullscreenElement) {
                        document.exitFullscreen();
                    } else {
                        document.documentElement.requestFullscreen();
                    }
                    break;
            }
        });
    </script>
    '''

def process_slide(slide_info, slide_index, total_slides, output_dir):
    """Process a single slide file"""
    source_path = Path("slides_complete") / slide_info["source"]
    
    # Read the source file
    with open(source_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Add navigation CSS to head
    head = soup.find('head')
    if head:
        head.append(BeautifulSoup(add_navigation_css(), 'html.parser'))
    
    # Add navigation bar before closing body
    body = soup.find('body')
    if body:
        nav_html = create_navigation(slide_index, total_slides)
        body.append(BeautifulSoup(nav_html, 'html.parser'))
        
        # Add keyboard navigation script
        body.append(BeautifulSoup(add_keyboard_navigation(), 'html.parser'))
    
    # Write to new location
    output_filename = f"{slide_info['num']}_{slide_info['name']}.html"
    output_path = output_dir / "slides" / output_filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"  ✅ Created: {output_filename} ({slide_info.get('agenda_section', 'General')})")
    
    return output_filename

def create_index_page(output_dir):
    """Create the index/contents page matching slide styling"""
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VMG Strategic Initiative - Presentation</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: #f5f5f5;
            overflow: hidden;
            margin: 0;
            padding: 0;
        }

        .presentation-container {
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            position: relative;
        }

        .slide {
            display: flex;
            flex-direction: column;
            width: 100vw;
            height: 100vh;
            padding: 3vh 4vw;
            background: white;
            position: relative;
            overflow-y: auto;
            overflow-x: hidden;
        }
        
        h1 {
            font-size: 2.8vw;
            margin-bottom: 1vh;
            color: #1a1a1a;
            text-align: center;
            font-weight: 300;
            letter-spacing: -0.5px;
        }
        
        .subtitle {
            font-size: 1.3vw;
            color: #666;
            margin-bottom: 3vh;
            padding-bottom: 2vh;
            border-bottom: 2px solid #e9ecef;
            text-align: center;
        }
        
        .toc-title {
            font-size: 1.8vw;
            color: #495057;
            margin-bottom: 2vh;
            font-weight: 600;
            text-align: center;
        }
        
        .toc-container {
            max-width: 70vw;
            margin: 0 auto;
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        
        .toc-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.5vw;
            margin-bottom: 3vh;
        }
        
        .toc-column {
            display: flex;
            flex-direction: column;
            gap: 0.5vh;
        }
        
        .toc-item {
            list-style: none;
            margin-bottom: 0.5vh;
        }
        
        .toc-link {
            color: #495057;
            text-decoration: none;
            display: flex;
            padding: 0.8vh 1.2vw;
            border-radius: 8px;
            transition: all 0.3s;
            align-items: baseline;
            background: #f8f9fa;
            border: 1px solid transparent;
        }
        
        .toc-link:hover {
            background: white;
            border-color: #0076a8;
            color: #0076a8;
            transform: translateX(5px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .toc-number {
            font-weight: 600;
            min-width: 2.5vw;
            color: #0076a8;
            font-size: 1.1vw;
        }
        
        .toc-text {
            flex: 1;
            font-size: 1vw;
            line-height: 1.4;
        }
        
        .start-button {
            display: inline-block;
            background: linear-gradient(135deg, #0076a8 0%, #00a74f 100%);
            color: white;
            text-decoration: none;
            padding: 1.2vh 3vw;
            border-radius: 50px;
            font-size: 1.2vw;
            font-weight: 600;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .start-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
        }
        
        .button-container {
            text-align: center;
            margin-top: 2vh;
            padding-top: 2vh;
            border-top: 2px solid #e9ecef;
        }
        
        .keyboard-hint {
            margin-top: 2vh;
            padding: 1vh 2vw;
            background: #f8f9fa;
            border-radius: 8px;
            font-size: 0.9vw;
            color: #6c757d;
            text-align: center;
        }
        
        .keyboard-hint strong {
            color: #495057;
        }
    </style>
</head>
<body>
    <div class="presentation-container">
        <div class="slide">
            <h1>VMG Strategic Initiative</h1>
            <div class="subtitle">AI-Enabled Consulting Platform</div>
            
            <div class="toc-container">
                <div class="toc-title">Table of Contents</div>
                <div class="toc-grid">
                    <div class="toc-column">
'''
    
    # Add table of contents entries - split into two columns
    half_point = len(SLIDES) // 2 + (len(SLIDES) % 2)  # Round up for odd numbers
    
    for i, slide in enumerate(SLIDES):
        if i == half_point:
            # Start second column
            index_html += '''
                    </div>
                    <div class="toc-column">
'''
        
        index_html += f'''
                        <div class="toc-item">
                            <a href="slides/{slide["num"]}_{slide["name"]}.html" class="toc-link">
                                <span class="toc-number">{int(slide["num"])}.</span>
                                <span class="toc-text">{slide["title"]}</span>
                            </a>
                        </div>
'''
    
    # Add start button pointing to first slide
    first_slide = SLIDES[0] if SLIDES else None
    start_link = f'slides/{first_slide["num"]}_{first_slide["name"]}.html' if first_slide else '#'
    
    index_html += f'''
                    </div>
                </div>
                
                <div class="button-container">
                    <a href="{start_link}" class="start-button">Start Presentation →</a>
                    <a href="presenter.html" class="start-button" style="background: linear-gradient(135deg, #00a74f 0%, #0076a8 100%); margin-left: 20px;">
                        🔳 Fullscreen Mode
                    </a>
                </div>
                
                <div class="keyboard-hint">
                    <strong>Keyboard Shortcuts:</strong> Use arrow keys to navigate between slides, 
                    Home key to return here, F for fullscreen, and Space for next slide.<br>
                    <strong>Tip:</strong> Use "Fullscreen Mode" button for seamless presentation without losing fullscreen between slides.
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''
    
    # Write index file
    index_path = output_dir / "index.html"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print("  ✅ Created: index.html (with color-coded sections)")

def main():
    """Build the complete linked presentation"""
    print("\n🚀 Building VMG Linked Presentation v2 (with color-coded sections)")
    print("="*50)
    
    # Check if database exists
    if not Path('slides.db').exists():
        print("❌ Error: slides.db not found!")
        print("   Run setup_slides_db_v2.py first to create the database")
        return
    
    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"vmg_presentation_{timestamp}")
    slides_dir = output_dir / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)
    
    # Also create/update a symlink to the latest version
    latest_link = Path("vmg_presentation_latest")
    if latest_link.exists() or latest_link.is_symlink():
        latest_link.unlink()
    latest_link.symlink_to(output_dir)
    
    # Process each slide
    print("\n📄 Processing slides:")
    total_slides = len(SLIDES)
    
    for i, slide in enumerate(SLIDES):
        process_slide(slide, i, total_slides, output_dir)
    
    # Create index page
    print("\n📋 Creating index page:")
    create_index_page(output_dir)
    
    # Copy image.png if it exists
    image_path = Path("slides_complete/image.png")
    if image_path.exists():
        shutil.copy(image_path, slides_dir / "image.png")
        print("  ✅ Copied: image.png")
    
    # Copy presenter.html if it exists
    presenter_path = Path("presenter.html")
    if presenter_path.exists():
        shutil.copy(presenter_path, output_dir / "presenter.html")
        print("  ✅ Copied: presenter.html (fullscreen mode)")
    
    print("\n✨ Presentation built successfully!")
    print(f"   Version: {timestamp}")
    print(f"   Location: {output_dir}/")
    print(f"   Latest link: vmg_presentation_latest/")
    print(f"   To view: open {output_dir}/index.html")
    print(f"   Total slides: {total_slides}")
    print("\n📝 Features:")
    print("   - Color-coded agenda sections in navigation")
    print("   - Grouped table of contents by agenda section")
    print("   - Keyboard navigation support")
    print("\n" + "="*50)

if __name__ == "__main__":
    main()