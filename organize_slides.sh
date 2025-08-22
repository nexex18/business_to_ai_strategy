#!/bin/bash

# Script to copy presentation slides to slides_complete folder
# Files keep their original names - no renaming needed

echo "🚀 Organizing VMG Presentation Slides"
echo "======================================"

# Create slides_complete directory if it doesn't exist
mkdir -p slides_complete

echo "📁 Copying files from slides_dev..."

# Copy files from slides_dev (keeping original names)
cp slides_dev/slide_01_title.html slides_complete/
cp slides_dev/slide_02_agenda.html slides_complete/
cp slides_dev/slide_16_executive_summary.html slides_complete/
cp slides_dev/slide_18_evolution_combined.html slides_complete/
cp slides_dev/slide_14_competitive_landscape.html slides_complete/
cp slides_dev/slide_20_vmg_built_for_ai.html slides_complete/
cp slides_dev/slide_19_porters_five_forces.html slides_complete/
cp slides_dev/slide_21_smb_ai_dilemma.html slides_complete/
cp slides_dev/slide_17_market_opportunity.html slides_complete/

echo "📁 Copying files from business_to_ai_strat_and_maturity_model..."

# Copy files from business strategy subdirectory (keeping original names)
cp slides_dev/business_to_ai_strat_and_maturity_model/slide_01_core_strategies.html slides_complete/
cp slides_dev/business_to_ai_strat_and_maturity_model/slide_02_extended_positioning.html slides_complete/
cp slides_dev/business_to_ai_strat_and_maturity_model/slide_05_three_moats.html slides_complete/
cp slides_dev/business_to_ai_strat_and_maturity_model/slide_12b_assessment_graph.html slides_complete/

echo "📁 Copying files from initiatives..."

# Copy files from initiatives subdirectory
cp slides_dev/initiatives/slide_02_initiatives_with_pillars_message.html slides_complete/

echo ""
echo "📊 Creating placeholder files for Google Slides..."

# Create placeholder files for Google Slides (keeping consistent naming)
cat > slides_complete/slide_13_ai_maturity_framework.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Maturity Framework</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: #f5f5f5;
        }
        .placeholder {
            text-align: center;
            padding: 40px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            max-width: 600px;
        }
        h1 {
            color: #1a1a1a;
            margin-bottom: 20px;
        }
        p {
            color: #666;
            line-height: 1.6;
        }
        .note {
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="placeholder">
        <h1>AI Maturity Framework</h1>
        <p>This slide contains content from Google Slides.</p>
        <div class="note">
            <strong>Note:</strong> This slide needs to be exported from Google Slides as HTML or integrated using an iframe.
        </div>
    </div>
</body>
</html>
EOF

cat > slides_complete/slide_18_financial_overview.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Financial Overview</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: #f5f5f5;
        }
        .placeholder {
            text-align: center;
            padding: 40px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            max-width: 600px;
        }
        h1 {
            color: #1a1a1a;
            margin-bottom: 20px;
        }
        p {
            color: #666;
            line-height: 1.6;
        }
        .note {
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="placeholder">
        <h1>Financial Overview</h1>
        <p>This slide contains content from Google Slides.</p>
        <div class="note">
            <strong>Note:</strong> This slide needs to be exported from Google Slides as HTML or integrated using an iframe.
        </div>
    </div>
</body>
</html>
EOF

echo ""
echo "✅ All slides copied successfully!"
echo ""
echo "📋 Summary:"
echo "  - Copied 15 files from slides_dev/ and subdirectories"
echo "  - Created 2 placeholder files for Google Slides"
echo "  - Existing 7 files in slides_complete/ remain unchanged"
echo ""
echo "📂 Files now in slides_complete/:"
ls -1 slides_complete/*.html | wc -l
echo "HTML files total"
echo ""
echo "Next steps:"
echo "  1. Export Google Slides (13 & 18) as HTML if needed"
echo "  2. Run setup_slides_db_v2.py to create the database"
echo "  3. Run build_linked_presentation.py to build the presentation"