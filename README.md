# VMG AI-Enabled Consulting Platform - Presentation System

A comprehensive presentation building system that creates linked HTML presentations with navigation, agenda tracking, and PDF export capabilities.

## Overview

This system manages a professional presentation for VMG (Velocity MG) consulting, featuring:
- 24 slides covering business strategy and AI transformation
- Color-coded agenda sections for easy navigation
- Automated PDF generation with fullscreen captures
- SQLite database for slide management

## Directory Structure

```
Final_Presentation/
├── slides_complete/          # Source HTML files for all slides
├── slides_dev/              # Development versions of slides
├── vmg_presentation_latest/  # Latest built presentation (symlink)
├── slide_captures/          # Screenshot storage for PDF generation
├── slides.db               # SQLite database with slide metadata
└── *.py                    # Build and utility scripts
```

## Prerequisites

### Required Software
- Python 3.7+
- Google Chrome browser
- ChromeDriver (`brew install chromedriver` on macOS)

### Python Packages
```bash
pip install selenium pillow reportlab beautifulsoup4
```

## Setup Instructions

### 1. Initialize the Slide Database

The SQLite database stores slide metadata including order, titles, and agenda sections.

```bash
# Create and populate the database
python setup_slides_db_v2.py
```

This creates `slides.db` with the following schema:
- `num`: Slide number (01-24)
- `name`: URL-friendly slide name
- `title`: Display title
- `source`: Source HTML filename
- `agenda_section`: Category for color-coding

### 2. Prepare Slides in slides_complete Directory

All source slides must be in the `slides_complete/` directory. Use the organization script to copy files:

```bash
# Copy slides from development to complete directory
./organize_slides.sh
```

Alternatively, manually ensure all HTML files are present:
- slide_01_title.html
- slide_02_agenda.html
- ... (through slide_24_conclusion.html)

#### Creating/Editing Slides

Each slide should follow this template structure:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Slide Title</title>
    <style>
        /* Standard presentation styles */
        .presentation-container { ... }
        .slide { ... }
        /* Custom slide styles */
    </style>
</head>
<body>
    <div class="presentation-container">
        <div class="slide active">
            <!-- Slide content -->
        </div>
    </div>
</body>
</html>
```

### 3. Build the Linked Presentation

Generate the complete presentation with navigation:

```bash
python build_linked_presentation_v2.py
```

This script:
- Reads slide configuration from `slides.db`
- Processes each slide from `slides_complete/`
- Adds navigation bars with color-coded agenda sections
- Creates an index page with table of contents
- Outputs to timestamped directory (e.g., `vmg_presentation_20250822_041326/`)
- Updates `vmg_presentation_latest` symlink

#### Agenda Section Colors

The build script applies a gradient color scheme from red to green:
- VMG background: `#d73502` (Dark red-orange)
- Competitive landscape: `#cb5a00` (Orange)
- Internal assessment: `#bf7800` (Dark orange)
- Opportunities: `#b39000` (Yellow-orange)
- Business and AI strategies: `#97a000` (Yellow-green)
- AI maturity: `#7aad00` (Light green)
- AI initiatives: `#5cb600` (Green)
- Financial analysis: `#3dbd00` (Bright green)
- Timeline: `#1dc200` (Bright green)
- Risks and mitigation: `#00c624` (Final green)

### 4. View the Presentation

Open the presentation in your browser:

```bash
# Open the index page
open vmg_presentation_latest/index.html

# Or open a specific slide
open vmg_presentation_latest/slides/01_title.html
```

#### Navigation Controls
- **Arrow Keys**: Navigate between slides
- **Space**: Next slide
- **Home**: Return to index
- **F**: Toggle fullscreen

## Generating PDF Output

### Automated PDF Generation

The system includes an automated script that captures each slide and creates a PDF:

```bash
python capture_slides_to_pdf.py
```

This script:
1. Opens Chrome browser automatically
2. Navigates to each slide sequentially
3. Enters fullscreen mode (F key)
4. Waits 5 seconds for animations to complete
5. Takes a screenshot
6. Compiles all screenshots into `VMG_Presentation.pdf`

#### Timing Configuration

If slides need more time to load, edit `capture_slides_to_pdf.py`:
```python
time.sleep(2)  # Initial load time (increase if needed)
time.sleep(5)  # After fullscreen (increase for complex slides)
```

### Manual PDF Generation

If automated capture fails, use the simple capture script:

```bash
python capture_slides_simple.py
```

Choose option 1 to take screenshots, then:
1. Open Preview.app
2. Select all screenshots in `slide_captures/`
3. File → Print → Save as PDF

## Database Management

### View Current Slides
```bash
sqlite3 slides.db "SELECT * FROM slides ORDER BY num;"
```

### Add a New Slide
```bash
sqlite3 slides.db "INSERT INTO slides (num, name, title, source, agenda_section) 
VALUES ('25', 'new_slide', 'New Slide Title', 'slide_25_new.html', 'Conclusion');"
```

### Update Slide Information
```bash
sqlite3 slides.db "UPDATE slides SET title = 'Updated Title' WHERE num = '24';"
```

## Troubleshooting

### ChromeDriver Issues
If you get ChromeDriver errors:
```bash
# macOS
brew install chromedriver
brew upgrade chromedriver

# Allow ChromeDriver in Security settings
xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver
```

### PDF Generation Fails
1. Ensure Chrome is installed and up-to-date
2. Check ChromeDriver matches Chrome version
3. Verify all Python packages are installed
4. Try increasing wait times in the script

### Slides Not Loading Properly
1. Check all files exist in `slides_complete/`
2. Verify database entries match filenames
3. Ensure no JavaScript errors in console
4. Check network requests aren't blocked

## Project Workflow

### Complete Workflow Example

```bash
# 1. Setup database
python setup_slides_db_v2.py

# 2. Organize slides
./organize_slides.sh

# 3. Build presentation
python build_linked_presentation_v2.py

# 4. View presentation
open vmg_presentation_latest/index.html

# 5. Generate PDF
python capture_slides_to_pdf.py

# 6. Open PDF
open VMG_Presentation.pdf
```

### Making Changes

1. Edit slide HTML in `slides_complete/`
2. Update database if titles/order changed
3. Rebuild presentation: `python build_linked_presentation_v2.py`
4. Regenerate PDF if needed

## File Descriptions

- `setup_slides_db_v2.py`: Creates and populates the slides database
- `build_linked_presentation_v2.py`: Main presentation builder
- `organize_slides.sh`: Copies slides to slides_complete directory
- `capture_slides_to_pdf.py`: Automated PDF generation using Selenium
- `capture_slides_simple.py`: Alternative screenshot tool
- `slides.db`: SQLite database with slide configuration

## Notes

- Always rebuild the presentation after making changes to slides
- The `vmg_presentation_latest` symlink always points to the most recent build
- Screenshots are saved in `slide_captures/` during PDF generation
- Each build creates a timestamped directory for version control

## Support

For issues or questions about the presentation system, check:
1. Browser console for JavaScript errors
2. Python error messages for script issues
3. ChromeDriver logs for automation problems
4. SQLite database integrity

---

*Built for VMG - Velocity Made Good: Ensuring Your AI Journey Reaches Its True Destination*