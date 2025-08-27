import os
import shutil
import sqlite3

# Define the new order
new_order = [
    ("slide_01_title.html", "slide_01_title.html"),
    ("slide_02_agenda.html", "slide_02_agenda.html"),
    ("slide_03_executive_summary.html", "slide_03_background_executive_summary.html"),
    ("slide_04_evolution_combined.html", "slide_04_background_evolution.html"),
    ("slide_05_competitive_landscape.html", "slide_05_competitive_landscape.html"),
    ("slide_07_porters_five_forces.html", "slide_06_internal_assessment.html"),
    ("slide_08_smb_ai_dilemma.html", "slide_07_opportunity_smb_dilemma.html"),
    ("slide_09_market_opportunity.html", "slide_08_opportunity_market.html"),
    ("slide_06_vmg_built_for_ai.html", "slide_09_business_ai_strategies.html"),
    ("slide_12_three_moats.html", "slide_10_business_ai_moats.html"),
    ("slide_14_assessment_graph.html", "slide_11_ai_maturity.html"),
    ("slide_15_initiatives_with_pillars.html", "slide_12_ai_initiatives_pillars.html"),
    ("slide_16_strategic_prioritization.html", "slide_13_ai_initiatives_prioritization.html"),
    ("slide_18_financial_overview.html", "slide_14_ai_initiatives_financial.html"),
    ("slide_09_customer_growth_assumptions.html", "slide_15_financial_analysis_growth.html"),
    ("slide_19_cost_benefit_analysis.html", "slide_16_financial_analysis_cost_benefit.html"),
    ("slide_20_roi_analysis.html", "slide_17_financial_analysis_roi.html"),
    ("slide_22_development_timeline.html", "slide_18_timeline.html"),
    ("slide_23_risk_assessment.html", "slide_19_risks_mitigations.html"),
    ("slide_24_conclusion.html", "slide_20_conclusion.html")
]

# Slides to move to appendix
appendix_slides = [
    "slide_10_core_strategies.html",
    "slide_11_extended_positioning.html",
    "slide_13_detailed_assessment.html",
    "slide_17_intelligent_content_generation.html",
    "slide_21_key_investment_metrics.html",
    "slide_25_strategy_assessment.html"
]

slides_dir = "slides_complete"
temp_dir = "slides_temp"

# Create temp directory
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

print("Starting slide reorganization...")
print("=" * 50)

# Step 1: Copy all files to temp directory with new names
print("\n1. Renaming main presentation slides:")
for old_name, new_name in new_order:
    old_path = os.path.join(slides_dir, old_name)
    new_path = os.path.join(temp_dir, new_name)
    if os.path.exists(old_path):
        shutil.copy2(old_path, new_path)
        print(f"   {old_name} -> {new_name}")
    else:
        print(f"   WARNING: {old_name} not found")

# Step 2: Copy appendix slides with new names
print("\n2. Moving slides to appendix:")
appendix_counter = 1
for slide in appendix_slides:
    old_path = os.path.join(slides_dir, slide)
    if os.path.exists(old_path):
        new_name = f"slide_A{appendix_counter:02d}_{slide[8:]}"  # Remove "slide_XX_" and add "slide_AXX_"
        new_path = os.path.join(temp_dir, new_name)
        shutil.copy2(old_path, new_path)
        print(f"   {slide} -> {new_name}")
        appendix_counter += 1
    else:
        print(f"   WARNING: {slide} not found")

# Step 3: Clear slides_complete and move from temp
print("\n3. Finalizing file structure...")
for file in os.listdir(slides_dir):
    if file.endswith('.html'):
        os.remove(os.path.join(slides_dir, file))

for file in os.listdir(temp_dir):
    shutil.move(os.path.join(temp_dir, file), os.path.join(slides_dir, file))

# Clean up temp directory
os.rmdir(temp_dir)

print("\n4. Updating SQL database...")
# Update database
conn = sqlite3.connect('slides.db')
cursor = conn.cursor()

# Clear existing slides
cursor.execute("DELETE FROM slides")

# Insert main presentation slides
for i, (_, new_name) in enumerate(new_order, 1):
    title = new_name.replace('slide_', '').replace('_', ' ').replace('.html', '').title()
    # Customize titles based on the content
    if 'background' in new_name:
        section = 'Background'
    elif 'competitive' in new_name:
        section = 'Competitive Analysis'
    elif 'internal' in new_name:
        section = 'Internal Assessment'
    elif 'opportunity' in new_name:
        section = 'Opportunity'
    elif 'business_ai' in new_name:
        section = 'Business & AI Strategies'
    elif 'ai_maturity' in new_name:
        section = 'AI Maturity'
    elif 'ai_initiatives' in new_name:
        section = 'AI Initiatives'
    elif 'financial_analysis' in new_name:
        section = 'Financial Analysis'
    elif 'timeline' in new_name:
        section = 'Timeline'
    elif 'risks' in new_name:
        section = 'Risks & Mitigations'
    elif 'conclusion' in new_name:
        section = 'Conclusion'
    else:
        section = 'Introduction'
    
    cursor.execute("""
        INSERT INTO slides (id, title, filename, order_index, section, is_active)
        VALUES (?, ?, ?, ?, ?, 1)
    """, (i, title, new_name, i, section))
    print(f"   Added to DB: {new_name} (Order: {i}, Section: {section})")

# Insert appendix slides
appendix_counter = 1
for slide in appendix_slides:
    if os.path.exists(os.path.join(slides_dir, f"slide_A{appendix_counter:02d}_{slide[8:]}")):
        new_name = f"slide_A{appendix_counter:02d}_{slide[8:]}"
        title = slide.replace('slide_', '').replace('_', ' ').replace('.html', '').title()
        cursor.execute("""
            INSERT INTO slides (id, title, filename, order_index, section, is_active)
            VALUES (?, ?, ?, ?, 'Appendix', 1)
        """, (20 + appendix_counter, title, new_name, 20 + appendix_counter))
        print(f"   Added to DB (Appendix): {new_name}")
        appendix_counter += 1

conn.commit()

# Verify the changes
print("\n5. Verification:")
cursor.execute("SELECT order_index, filename, section FROM slides ORDER BY order_index")
results = cursor.fetchall()
for order, filename, section in results:
    print(f"   {order:2d}. {filename:45s} [{section}]")

conn.close()

print("\n✅ Reorganization complete!")
print(f"   - {len(new_order)} slides in main presentation")
print(f"   - {appendix_counter-1} slides in appendix")
