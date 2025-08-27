import os
import shutil
import sqlite3

# Define the new order with proper agenda sections
new_order = [
    ("slide_01_title.html", "slide_01_title.html", "Title", "Introduction"),
    ("slide_02_agenda.html", "slide_02_agenda.html", "Agenda", "Introduction"),
    ("slide_03_executive_summary.html", "slide_03_background_executive_summary.html", "Executive Summary", "Background"),
    ("slide_04_evolution_combined.html", "slide_04_background_evolution.html", "Evolution of Consulting", "Background"),
    ("slide_05_competitive_landscape.html", "slide_05_competitive_landscape.html", "Competitive Landscape", "Competitive Landscape"),
    ("slide_07_porters_five_forces.html", "slide_06_internal_assessment.html", "Porter's Five Forces", "Internal Assessment"),
    ("slide_08_smb_ai_dilemma.html", "slide_07_opportunity_smb_dilemma.html", "SMB AI Dilemma", "Opportunity"),
    ("slide_09_market_opportunity.html", "slide_08_opportunity_market.html", "Market Opportunity", "Opportunity"),
    ("slide_06_vmg_built_for_ai.html", "slide_09_business_ai_strategies.html", "VMG Built for AI", "Business & AI Strategies"),
    ("slide_12_three_moats.html", "slide_10_business_ai_moats.html", "Three Moats", "Business & AI Strategies"),
    ("slide_14_assessment_graph.html", "slide_11_ai_maturity.html", "AI Maturity Assessment", "AI Maturity"),
    ("slide_15_initiatives_with_pillars.html", "slide_12_ai_initiatives_pillars.html", "Strategic Initiatives", "AI Initiatives"),
    ("slide_16_strategic_prioritization.html", "slide_13_ai_initiatives_prioritization.html", "Strategic Prioritization", "AI Initiatives"),
    ("slide_18_financial_overview.html", "slide_14_ai_initiatives_financial.html", "Financial Overview", "AI Initiatives"),
    ("slide_09_customer_growth_assumptions.html", "slide_15_financial_analysis_growth.html", "Customer Growth Assumptions", "Financial Analysis"),
    ("slide_19_cost_benefit_analysis.html", "slide_16_financial_analysis_cost_benefit.html", "Cost-Benefit Analysis", "Financial Analysis"),
    ("slide_20_roi_analysis.html", "slide_17_financial_analysis_roi.html", "ROI Analysis", "Financial Analysis"),
    ("slide_22_development_timeline.html", "slide_18_timeline.html", "Development Timeline", "Timeline"),
    ("slide_23_risk_assessment.html", "slide_19_risks_mitigations.html", "Risk Assessment", "Risks & Mitigations"),
    ("slide_24_conclusion.html", "slide_20_conclusion.html", "Conclusion", "Conclusion")
]

# Slides to move to appendix
appendix_slides = [
    ("slide_10_core_strategies.html", "Core Strategies"),
    ("slide_11_extended_positioning.html", "Extended Positioning"),
    ("slide_13_detailed_assessment.html", "Detailed Assessment"),
    ("slide_17_intelligent_content_generation.html", "Intelligent Content Generation"),
    ("slide_21_key_investment_metrics.html", "Key Investment Metrics"),
    ("slide_25_strategy_assessment.html", "Strategy Assessment")
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
for old_name, new_name, _, _ in new_order:
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
appendix_list = []
for slide, title in appendix_slides:
    old_path = os.path.join(slides_dir, slide)
    if os.path.exists(old_path):
        new_name = f"slide_A{appendix_counter:02d}_{slide[8:]}"  # Remove "slide_XX_" and add "slide_AXX_"
        new_path = os.path.join(temp_dir, new_name)
        shutil.copy2(old_path, new_path)
        print(f"   {slide} -> {new_name}")
        appendix_list.append((new_name, title))
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
# Update database with correct schema
conn = sqlite3.connect('slides.db')
cursor = conn.cursor()

# Clear existing slides
cursor.execute("DELETE FROM slides")

# Insert main presentation slides
for i, (_, new_name, title, section) in enumerate(new_order, 1):
    num = f"{i:02d}"
    name = new_name.replace('.html', '')
    
    cursor.execute("""
        INSERT INTO slides (num, name, title, source, agenda_section)
        VALUES (?, ?, ?, ?, ?)
    """, (num, name, title, f'slides_complete/{new_name}', section))
    print(f"   Added to DB: {num}. {title} [{section}]")

# Insert appendix slides
for i, (new_name, title) in enumerate(appendix_list, 1):
    num = f"A{i:02d}"
    name = new_name.replace('.html', '')
    
    cursor.execute("""
        INSERT INTO slides (num, name, title, source, agenda_section)
        VALUES (?, ?, ?, ?, ?)
    """, (num, name, title, f'slides_complete/{new_name}', 'Appendix'))
    print(f"   Added to DB: {num}. {title} [Appendix]")

conn.commit()

# Verify the changes
print("\n5. Verification:")
print("-" * 50)
cursor.execute("SELECT num, title, agenda_section FROM slides ORDER BY num")
results = cursor.fetchall()
for num, title, section in results:
    print(f"   {num:3s}. {title:40s} [{section}]")

conn.close()

print("\n✅ Reorganization complete!")
print(f"   - {len(new_order)} slides in main presentation")
print(f"   - {len(appendix_list)} slides in appendix")
print("\nRun 'python build_linked_presentation_v2.py' to generate the new presentation.")