#!/usr/bin/env python3
"""
Simple slide capture using macOS screenshot utility
Works without additional dependencies
"""

import os
import subprocess
import time
from pathlib import Path
import sqlite3

def get_slides_from_db():
    """Get all slides from the database"""
    conn = sqlite3.connect('slides.db')
    cursor = conn.cursor()
    cursor.execute('SELECT num, name, title FROM slides ORDER BY num')
    slides = cursor.fetchall()
    conn.close()
    return slides

def capture_with_screenshot():
    """Use macOS screenshot tool to capture slides"""
    print("🚀 Starting slide capture process...")
    print("This will open each slide in your browser and take screenshots")
    print("=" * 50)
    
    # Create output directory
    output_dir = Path("slide_captures")
    output_dir.mkdir(exist_ok=True)
    
    # Get slides from database
    slides = get_slides_from_db()
    print(f"Found {len(slides)} slides to capture\n")
    
    input("Press Enter when ready to start (this will open your browser)...")
    
    captured_files = []
    
    for slide_num, slide_name, slide_title in slides:
        print(f"\n📸 Slide {slide_num}: {slide_title}")
        
        # Build the file URL
        slide_path = Path.cwd() / "vmg_presentation_latest" / "slides" / f"{slide_num}_{slide_name}.html"
        slide_url = f"file://{slide_path}"
        
        # Open in browser
        subprocess.run(["open", slide_url])
        
        print("   Waiting for page to load...")
        time.sleep(2)
        
        # Take screenshot using macOS screencapture
        # -x: no sound
        # -T 0: no delay
        # -t png: PNG format
        screenshot_path = output_dir / f"slide_{slide_num:02d}_{slide_name}.png"
        
        print("   Taking screenshot (capturing entire screen)...")
        subprocess.run([
            "screencapture", 
            "-x",  # No sound
            "-T", "0",  # No delay
            str(screenshot_path)
        ])
        
        captured_files.append(screenshot_path)
        print(f"   ✓ Saved: {screenshot_path.name}")
        
        # Brief pause between slides
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print(f"✅ Captured {len(captured_files)} slides")
    print(f"📁 Screenshots saved in: {output_dir.absolute()}")
    print("\n💡 Next steps:")
    print("1. Review the screenshots in the 'slide_captures' folder")
    print("2. Open Preview.app and select all screenshots")
    print("3. Use File > Print > Save as PDF to create a single PDF")
    print("   OR")
    print("   Use File > Export as PDF for each image and combine")
    
    return captured_files

def create_combined_html():
    """Create a single HTML file with all slides for easy printing"""
    print("\n📄 Creating combined HTML for printing...")
    
    slides = get_slides_from_db()
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VMG Presentation - Print Version</title>
    <style>
        @media print {
            .slide-container {
                page-break-after: always;
                width: 100%;
                height: 100vh;
                position: relative;
            }
            .slide-container:last-child {
                page-break-after: avoid;
            }
        }
        
        body {
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        .slide-container {
            width: 100%;
            height: 100vh;
            border: 1px solid #ddd;
            margin-bottom: 20px;
            position: relative;
            overflow: hidden;
        }
        
        iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
        
        .slide-number {
            position: absolute;
            bottom: 10px;
            right: 10px;
            background: rgba(0,0,0,0.1);
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
            z-index: 1000;
        }
        
        @media screen {
            .instructions {
                background: #f0f0f0;
                padding: 20px;
                margin: 20px;
                border-radius: 10px;
            }
        }
        
        @media print {
            .instructions {
                display: none;
            }
        }
    </style>
</head>
<body>
    <div class="instructions">
        <h2>Print Instructions</h2>
        <ol>
            <li>Press Cmd+P (or File > Print)</li>
            <li>Select "Save as PDF" from the PDF dropdown</li>
            <li>Make sure orientation is set to Landscape</li>
            <li>Set margins to "None" or "Minimum"</li>
            <li>Click "Save" and choose location</li>
        </ol>
    </div>
"""
    
    for slide_num, slide_name, slide_title in slides:
        slide_path = f"vmg_presentation_latest/slides/{slide_num}_{slide_name}.html"
        html_content += f"""
    <div class="slide-container">
        <iframe src="{slide_path}" title="Slide {slide_num}: {slide_title}"></iframe>
        <div class="slide-number">Slide {slide_num}</div>
    </div>
"""
    
    html_content += """
</body>
</html>"""
    
    # Save the combined HTML
    output_path = Path("presentation_print.html")
    output_path.write_text(html_content)
    
    print(f"✅ Created: {output_path}")
    print("\n📖 To create PDF:")
    print("1. Open presentation_print.html in your browser")
    print("2. Press Cmd+P to print")
    print("3. Choose 'Save as PDF'")
    print("4. Set orientation to Landscape")
    print("5. Save the PDF")
    
    # Open in browser
    subprocess.run(["open", str(output_path)])

def main():
    """Main function"""
    print("=" * 50)
    print("VMG Presentation Capture Tool")
    print("=" * 50)
    print("\nChoose an option:")
    print("1. Take screenshots of each slide")
    print("2. Create combined HTML for printing")
    print("3. Both")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice in ["1", "3"]:
        capture_with_screenshot()
    
    if choice in ["2", "3"]:
        create_combined_html()
    
    if choice not in ["1", "2", "3"]:
        print("Invalid choice")

if __name__ == "__main__":
    main()