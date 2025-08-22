#!/usr/bin/env python3
"""
Build a clean linked presentation from standalone slides
Each slide is a separate HTML page with navigation
"""

import os
import shutil
from pathlib import Path
from bs4 import BeautifulSoup

# Slide configuration
SLIDES = [
    {"num": "01", "name": "vmg_overview", "title": "Velocity MG: Making Good on AI's Promise", "source": "slide_01_velocity_mg_making_good_on_ais_promise_standalone.html"},
    {"num": "02", "name": "smb_dilemma", "title": "The SMB AI Dilemma", "source": "slide_02_the_smb_ai_dilemma_standalone.html"},
    {"num": "03", "name": "framework", "title": "The VMG Framework", "source": "slide_03_the_vmg_framework_standalone.html"},
    {"num": "04", "name": "ai_approach", "title": "Our AI-Powered Approach", "source": "slide_04_our_aipowered_approach_standalone.html"},
    {"num": "05", "name": "prioritization", "title": "Strategic Initiative Prioritization", "source": "slide_05_strategic_initiative_prioritization_standalone.html"},
    {"num": "06", "name": "content_platform", "title": "Initiative: Intelligent Content Generation Platform", "source": "slide_06_initiative_intelligent_content_generatio_standalone.html"},
    {"num": "07", "name": "revenue_model", "title": "Transforming the Consulting Revenue Model", "source": "slide_07_transforming_the_consulting_revenue_mode_standalone.html"},
    {"num": "08", "name": "cost_benefit", "title": "Cost-Benefit Analysis", "source": "slide_08_costbenefit_analysis_standalone.html"},
    {"num": "09", "name": "customer_growth", "title": "Customer Growth Assumptions", "source": "slide_09_fixed.html"},
    {"num": "10", "name": "roi_analysis", "title": "Return on Investment Analysis", "source": "slide_10_fixed.html"},
    {"num": "11", "name": "timeline", "title": "Development Timeline", "source": "slide_11_development_timeline_standalone.html"},
    {"num": "12", "name": "key_metrics", "title": "Key Investment Metrics", "source": "slide_12_fixed.html"},
    {"num": "13", "name": "risk_assessment", "title": "Risk Assessment & Mitigation Strategy", "source": "slide_13_risk_assessment_mitigation_strategy_standalone.html"}
]

def create_navigation(slide_index, total_slides):
    """Create navigation HTML for a slide"""
    current = SLIDES[slide_index]
    
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
    
    # Navigation HTML
    nav_html = f'''
    <nav class="slide-navigation">
        {prev_link}
        <div class="nav-center">
            <a href="../index.html" class="nav-home">☰ Contents</a>
            <span class="nav-counter">Slide {int(current["num"])} of {total_slides}</span>
        </div>
        {next_link}
    </nav>
    '''
    
    return nav_html

def add_navigation_css():
    """CSS for the navigation bar"""
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
            padding: 0 30px;
            z-index: 1000;
            box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
        }
        
        .nav-prev, .nav-next {
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 5px;
            transition: background 0.3s;
            font-weight: 600;
            font-size: 16px;
        }
        
        .nav-prev:hover, .nav-next:hover {
            background: rgba(255, 255, 255, 0.1);
        }
        
        .nav-disabled {
            opacity: 0.3;
            cursor: not-allowed;
        }
        
        .nav-center {
            display: flex;
            align-items: center;
            gap: 30px;
        }
        
        .nav-home {
            color: white;
            text-decoration: none;
            padding: 8px 16px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 5px;
            transition: all 0.3s;
            font-weight: 500;
        }
        
        .nav-home:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.5);
        }
        
        .nav-counter {
            color: rgba(255, 255, 255, 0.8);
            font-size: 14px;
        }
        
        /* Adjust slide container to account for navigation */
        .presentation-container, .slide {
            padding-bottom: 80px !important;
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

def process_slide(slide_info, slide_index, total_slides):
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
    output_path = Path("vmg_presentation/slides") / output_filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"  ✅ Created: {output_filename}")
    
    return output_filename

def create_index_page():
    """Create the index/contents page"""
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 800px;
            width: 100%;
            padding: 60px;
        }
        
        h1 {
            font-size: 36px;
            color: #1a1a1a;
            margin-bottom: 10px;
        }
        
        .subtitle {
            font-size: 20px;
            color: #666;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 2px solid #e9ecef;
        }
        
        .toc-title {
            font-size: 24px;
            color: #495057;
            margin-bottom: 20px;
            font-weight: 600;
        }
        
        .toc-list {
            list-style: none;
            margin-bottom: 40px;
        }
        
        .toc-item {
            margin-bottom: 12px;
        }
        
        .toc-link {
            color: #495057;
            text-decoration: none;
            display: flex;
            padding: 12px 16px;
            border-radius: 8px;
            transition: all 0.3s;
            align-items: baseline;
        }
        
        .toc-link:hover {
            background: #f8f9fa;
            color: #667eea;
            transform: translateX(5px);
        }
        
        .toc-number {
            font-weight: 600;
            min-width: 30px;
            color: #667eea;
        }
        
        .toc-text {
            flex: 1;
        }
        
        .start-button {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            padding: 16px 40px;
            border-radius: 50px;
            font-size: 18px;
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
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px solid #e9ecef;
        }
        
        .keyboard-hint {
            margin-top: 40px;
            padding: 16px;
            background: #f8f9fa;
            border-radius: 8px;
            font-size: 14px;
            color: #6c757d;
        }
        
        .keyboard-hint strong {
            color: #495057;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>VMG Strategic Initiative</h1>
        <div class="subtitle">Intelligent Content Generation Platform</div>
        
        <div class="toc-title">Table of Contents</div>
        <ol class="toc-list">
'''
    
    # Add table of contents entries
    for slide in SLIDES:
        index_html += f'''
            <li class="toc-item">
                <a href="slides/{slide["num"]}_{slide["name"]}.html" class="toc-link">
                    <span class="toc-number">{int(slide["num"])}.</span>
                    <span class="toc-text">{slide["title"]}</span>
                </a>
            </li>
'''
    
    index_html += '''
        </ol>
        
        <div class="button-container">
            <a href="slides/01_vmg_overview.html" class="start-button">Start Presentation →</a>
        </div>
        
        <div class="keyboard-hint">
            <strong>Keyboard Shortcuts:</strong> Use arrow keys to navigate between slides, 
            Home key to return here, F for fullscreen, and Space for next slide.
        </div>
    </div>
</body>
</html>
'''
    
    # Write index file
    index_path = Path("vmg_presentation/index.html")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print("  ✅ Created: index.html")

def main():
    """Build the complete linked presentation"""
    print("\n🚀 Building VMG Linked Presentation")
    print("="*50)
    
    # Process each slide
    print("\n📄 Processing slides:")
    total_slides = len(SLIDES)
    
    for i, slide in enumerate(SLIDES):
        process_slide(slide, i, total_slides)
    
    # Create index page
    print("\n📋 Creating index page:")
    create_index_page()
    
    print("\n✨ Presentation built successfully!")
    print(f"   Location: vmg_presentation/")
    print(f"   To view: open vmg_presentation/index.html")
    print("\n" + "="*50)

if __name__ == "__main__":
    main()