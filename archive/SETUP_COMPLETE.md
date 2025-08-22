# VMG Presentation System - Setup Complete ✅

## What Has Been Created

Your modular presentation system is now set up at:
`/Users/darrensilver/python_projects/Booth_app/Assignments/Business_Casev2/Final_Presentation/`

### Files Created:

1. **Structure**
   - `slides/` - Directory for individual slide files
   - `templates/` - Reusable slide templates
   - `styles/` - CSS stylesheets
   - `scripts/` - JavaScript files

2. **Core Files**
   - `slides_manifest.json` - Controls which slides appear and their order
   - `build_presentation.py` - Assembles slides into complete presentation
   - `extract_slides.py` - Extracts slides from your original HTML
   - `README.md` - Complete documentation

3. **Templates**
   - `header.html` - Presentation header with CSS/JS includes
   - `footer.html` - Navigation controls and scripts
   - `standard_template.html` - Basic slide template
   - `grid_template.html` - Grid layout template

4. **Example Slide**
   - `slide_01_vmg_overview.html` - First slide extracted as example

## Next Steps to Complete Migration

### Option 1: Quick Start (Recommended)
1. Copy your original `Submitted_Assignment_4.html` to the Final_Presentation folder
2. Run: `python extract_slides.py`
   - This will automatically extract all 13 slides
3. Run: `python build_presentation.py`
   - This creates your new modular presentation

### Option 2: Manual Migration
1. Open your original HTML file
2. Copy each slide's content (between `<div class="slide">` tags)
3. Save as individual files in `slides/` folder
4. Update `slides_manifest.json` with correct filenames
5. Run `python build_presentation.py`

## How to Use Going Forward

### Edit a slide:
```bash
# 1. Edit the individual slide file
nano slides/slide_02_smb_dilemma.html

# 2. Rebuild presentation
python build_presentation.py
```

### Add a new slide:
```bash
# 1. Copy a template
cp templates/grid_template.html slides/slide_14_new_content.html

# 2. Edit the content
nano slides/slide_14_new_content.html

# 3. Add to manifest
# Edit slides_manifest.json and add your slide entry

# 4. Rebuild
python build_presentation.py
```

### Remove a slide:
```bash
# 1. Edit manifest - set "active": false
nano slides_manifest.json

# 2. Rebuild
python build_presentation.py
```

## Benefits of This System

✅ **Edit individual slides** without touching others
✅ **Add/remove slides** without regenerating everything  
✅ **Version control friendly** - see exactly what changed
✅ **Reusable templates** for consistent new slides
✅ **Single source of truth** - manifest controls everything
✅ **No manual HTML assembly** - Python script handles it

## Important Notes

⚠️ Your original HTML file is 100,000+ characters with complex styling and scripts
⚠️ The full CSS and JavaScript need to be extracted for complete functionality
⚠️ Some slides have interactive elements (charts) that need special handling

## To Complete the System

Run these commands:
```bash
cd /Users/darrensilver/python_projects/Booth_app/Assignments/Business_Casev2/Final_Presentation

# Extract slides from your original file
python extract_slides.py

# Build the new modular presentation
python build_presentation.py

# Open the result
open presentation.html
```

The system is ready for you to start using!
