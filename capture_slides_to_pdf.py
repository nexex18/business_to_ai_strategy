#!/usr/bin/env python3
"""
Capture all presentation slides to PDF using Selenium
Navigates through each slide and takes screenshots
"""

import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.utils import ImageReader
import sqlite3

def get_slides_from_db():
    """Get all slides from the database"""
    conn = sqlite3.connect('slides.db')
    cursor = conn.cursor()
    cursor.execute('SELECT num, name, title FROM slides ORDER BY CAST(num AS INTEGER)')
    slides = cursor.fetchall()
    conn.close()
    return slides

def capture_slides():
    """Capture all slides using Selenium"""
    print("🚀 Starting slide capture process...")
    
    # Create output directory
    output_dir = Path("slide_captures")
    output_dir.mkdir(exist_ok=True)
    
    # Get slides from database
    slides = get_slides_from_db()
    print(f"Found {len(slides)} slides to capture")
    
    # Setup Chrome options for better screenshots
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Set window size to standard presentation size (16:9 aspect ratio)
    options.add_argument('--window-size=1920,1080')
    
    # Initialize the driver
    print("Starting Chrome browser...")
    driver = webdriver.Chrome(options=options)
    
    try:
        # Navigate to the presentation
        presentation_path = Path.cwd() / "vmg_presentation_latest" / "index.html"
        driver.get(f"file://{presentation_path}")
        time.sleep(2)
        
        captured_files = []
        
        for slide_num, slide_name, slide_title in slides:
            print(f"📸 Capturing slide {slide_num}: {slide_title}")
            
            # Navigate to the slide
            slide_url = f"file://{Path.cwd()}/vmg_presentation_latest/slides/{str(slide_num).zfill(2)}_{slide_name}.html"
            driver.get(slide_url)
            
            # Wait for slide to load
            time.sleep(2)  # Initial load time
            
            # Try to go fullscreen (F key)
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys('f')
            
            # Wait longer for fullscreen and all animations to complete
            time.sleep(5)  # Give plenty of time for everything to render
            
            # Take screenshot
            screenshot_path = output_dir / f"slide_{str(slide_num).zfill(2)}_{slide_name}.png"
            driver.save_screenshot(str(screenshot_path))
            captured_files.append(screenshot_path)
            
            # Exit fullscreen for next slide
            body.send_keys('f')
            time.sleep(0.2)
        
        print(f"✅ Captured {len(captured_files)} slides")
        return captured_files
        
    finally:
        driver.quit()

def create_pdf_from_screenshots(screenshot_files, output_filename="presentation.pdf"):
    """Create a PDF from the screenshot files"""
    print(f"📄 Creating PDF: {output_filename}")
    
    if not screenshot_files:
        print("❌ No screenshots to process")
        return
    
    # Create PDF with landscape orientation
    pdf_path = Path(output_filename)
    c = canvas.Canvas(str(pdf_path), pagesize=landscape(letter))
    
    # Get page dimensions
    page_width, page_height = landscape(letter)
    
    for i, img_path in enumerate(screenshot_files):
        print(f"  Adding slide {i+1}/{len(screenshot_files)}")
        
        # Open image to get dimensions
        img = Image.open(img_path)
        img_width, img_height = img.size
        
        # Calculate scaling to fit page
        scale_w = page_width / img_width
        scale_h = page_height / img_height
        scale = min(scale_w, scale_h) * 0.95  # Leave small margin
        
        # Calculate position to center image
        scaled_width = img_width * scale
        scaled_height = img_height * scale
        x = (page_width - scaled_width) / 2
        y = (page_height - scaled_height) / 2
        
        # Draw image on PDF
        c.drawImage(str(img_path), x, y, width=scaled_width, height=scaled_height)
        
        # Add new page if not last image
        if i < len(screenshot_files) - 1:
            c.showPage()
    
    # Save PDF
    c.save()
    print(f"✅ PDF created: {pdf_path}")
    return pdf_path

def main():
    """Main function to capture slides and create PDF"""
    print("=" * 50)
    print("VMG Presentation PDF Generator")
    print("=" * 50)
    
    try:
        # Capture all slides
        screenshots = capture_slides()
        
        # Create PDF
        if screenshots:
            pdf_file = create_pdf_from_screenshots(screenshots, "VMG_Presentation.pdf")
            print("\n✨ Success! Your presentation has been saved as VMG_Presentation.pdf")
            print(f"   Location: {Path.cwd() / 'VMG_Presentation.pdf'}")
            
            # Optionally clean up screenshot files
            cleanup = input("\n🧹 Delete screenshot files? (y/n): ").lower()
            if cleanup == 'y':
                for f in screenshots:
                    f.unlink()
                print("   Screenshots deleted")
        else:
            print("❌ No screenshots were captured")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Chrome browser installed")
        print("2. ChromeDriver installed (brew install chromedriver)")
        print("3. Required Python packages (selenium, pillow, reportlab)")
        print("\nInstall packages with:")
        print("pip install selenium pillow reportlab")

if __name__ == "__main__":
    main()