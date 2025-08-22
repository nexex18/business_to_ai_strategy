#!/usr/bin/env python3
"""
Setup SQLite database for presentation slides with agenda sections
Files keep their original names - no renaming
"""

import sqlite3
from pathlib import Path

# Define slides with agenda sections and actual file names
SLIDES = [
    # Title & Agenda
    {"num": "01", "name": "title", "title": "VMG AI-Enabled Consulting Platform", 
     "source": "slide_01_title.html", "agenda_section": "Title"},
    
    {"num": "02", "name": "agenda", "title": "Agenda", 
     "source": "slide_02_agenda.html", "agenda_section": "Agenda"},
    
    # VMG Background
    {"num": "03", "name": "executive_summary", "title": "Executive Summary", 
     "source": "slide_16_executive_summary.html", "agenda_section": "VMG background"},
    
    {"num": "04", "name": "evolution_combined", "title": "Evolution of Consulting & VMG's Transformation", 
     "source": "slide_18_evolution_combined.html", "agenda_section": "VMG background"},
    
    # Competitive Landscape
    {"num": "05", "name": "competitive_landscape", "title": "Competitive Landscape", 
     "source": "slide_14_competitive_landscape.html", "agenda_section": "Competitive landscape"},
    
    # Internal Assessment
    {"num": "06", "name": "vmg_built_for_ai", "title": "VMG Built for AI", 
     "source": "slide_20_vmg_built_for_ai.html", "agenda_section": "Internal assessment"},
    
    {"num": "07", "name": "porters_five_forces", "title": "Porter's Five Forces Analysis", 
     "source": "slide_19_porters_five_forces.html", "agenda_section": "Internal assessment"},
    
    # Opportunities
    {"num": "08", "name": "smb_ai_dilemma", "title": "The SMB AI Dilemma", 
     "source": "slide_21_smb_ai_dilemma.html", "agenda_section": "Opportunities"},
    
    {"num": "09", "name": "market_opportunity", "title": "Market Opportunity", 
     "source": "slide_17_market_opportunity.html", "agenda_section": "Opportunities"},
    
    # Business and AI Strategies
    {"num": "10", "name": "core_strategies", "title": "Core Business Strategies", 
     "source": "slide_01_core_strategies.html", 
     "agenda_section": "Business and AI strategies"},
    
    {"num": "11", "name": "extended_positioning", "title": "Extended Positioning", 
     "source": "slide_02_extended_positioning.html", 
     "agenda_section": "Business and AI strategies"},
    
    {"num": "12", "name": "three_moats", "title": "Three Strategic Moats", 
     "source": "slide_05_three_moats.html", 
     "agenda_section": "Business and AI strategies"},
    
    # AI Maturity
    {"num": "13", "name": "ai_maturity_framework", "title": "AI Maturity Framework", 
     "source": "slide_13_ai_maturity_framework.html", "agenda_section": "AI maturity"},
    
    {"num": "14", "name": "maturity_assessment_graph", "title": "VMG AI Maturity Assessment", 
     "source": "slide_12b_assessment_graph.html", 
     "agenda_section": "AI maturity"},
    
    # AI Initiatives
    {"num": "15", "name": "initiatives_with_pillars", "title": "Five Integrated AI Initiatives", 
     "source": "slide_02_initiatives_with_pillars_message.html", 
     "agenda_section": "AI initiatives"},
    
    {"num": "16", "name": "strategic_prioritization", "title": "Strategic Initiative Prioritization", 
     "source": "slide_05_strategic_initiative_prioritization.html", 
     "agenda_section": "AI initiatives"},
    
    {"num": "17", "name": "intelligent_content_generation", "title": "Intelligent Content Generation Platform", 
     "source": "slide_06_initiative_intelligent_content_generatio.html", 
     "agenda_section": "AI initiatives"},
    
    # Financial Analysis
    {"num": "18", "name": "financial_overview", "title": "Financial Overview", 
     "source": "slide_18_financial_overview.html", "agenda_section": "Financial analysis"},
    
    {"num": "19", "name": "cost_benefit_analysis", "title": "Cost-Benefit Analysis", 
     "source": "slide_08_costbenefit_analysis.html", 
     "agenda_section": "Financial analysis"},
    
    {"num": "20", "name": "roi_analysis", "title": "Return on Investment Analysis", 
     "source": "slide_10_return_on_investment_analysis.html", 
     "agenda_section": "Financial analysis"},
    
    {"num": "21", "name": "key_investment_metrics", "title": "Key Investment Metrics", 
     "source": "slide_12_key_investment_metrics.html", 
     "agenda_section": "Financial analysis"},
    
    # Timeline
    {"num": "22", "name": "development_timeline", "title": "Development Timeline", 
     "source": "slide_11_development_timeline.html", 
     "agenda_section": "Timeline"},
    
    # Risks and Mitigation
    {"num": "23", "name": "risk_assessment", "title": "Risk Assessment & Mitigation Strategy", 
     "source": "slide_13_risk_assessment_mitigation_strategy.html", 
     "agenda_section": "Risks and mitigation strategies"},
]

def create_database():
    """Create a new SQLite database with slides table including agenda section"""
    
    # Remove existing database if it exists
    db_path = Path('slides.db')
    if db_path.exists():
        print("🗑️  Removing existing database...")
        db_path.unlink()
    
    # Create new database
    conn = sqlite3.connect('slides.db')
    cursor = conn.cursor()
    
    # Create table with agenda_section column
    cursor.execute('''
        CREATE TABLE slides (
            num TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            title TEXT NOT NULL,
            source TEXT NOT NULL,
            agenda_section TEXT NOT NULL
        )
    ''')
    
    # Insert all slides
    for slide in SLIDES:
        cursor.execute('''
            INSERT INTO slides (num, name, title, source, agenda_section)
            VALUES (?, ?, ?, ?, ?)
        ''', (slide['num'], slide['name'], slide['title'], slide['source'], slide['agenda_section']))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database created with {len(SLIDES)} slides")

def verify_files():
    """Verify that all source files exist in slides_complete/"""
    print("\n📁 Verifying source files in slides_complete/...")
    
    missing_files = []
    found_files = []
    
    for slide in SLIDES:
        source_path = Path('slides_complete') / slide['source']
        if source_path.exists():
            found_files.append(f"  ✅ Slide {slide['num']}: {slide['source']}")
        else:
            missing_files.append(f"  ❌ Slide {slide['num']}: {slide['source']}")
    
    print(f"\n✅ Found {len(found_files)} files")
    
    if missing_files:
        print(f"\n❌ Missing {len(missing_files)} files:")
        for item in missing_files:
            print(item)
        return False
    else:
        print("\n✅ All HTML files found!")
        return True

def display_agenda_sections():
    """Display slides organized by agenda section"""
    print("\n📋 Slides by Agenda Section:")
    print("="*50)
    
    current_section = None
    for slide in SLIDES:
        if slide['agenda_section'] != current_section:
            current_section = slide['agenda_section']
            print(f"\n{current_section}:")
        print(f"  {slide['num']}. {slide['title']} ({slide['source']})")

def main():
    print("🚀 Setting up VMG Presentation Database v2")
    print("="*50)
    
    # Create database
    create_database()
    
    # Verify files exist
    all_files_exist = verify_files()
    
    # Display agenda sections
    display_agenda_sections()
    
    print("\n" + "="*50)
    
    if all_files_exist:
        print("\n✅ Database setup complete!")
        print("   All files verified in slides_complete/")
        print("\n   Next step: Run python build_linked_presentation.py")
    else:
        print("\n⚠️  Warning: Some files are missing from slides_complete/")
        print("   Check the file names and run organize_slides.sh if needed")
    
    print("\n📝 Notes:")
    print("   - Slides 13 & 18 are placeholders for Google Slides content")
    print("   - All files keep their original names (no renumbering)")
    print("   - The presentation order is defined in the database")

if __name__ == "__main__":
    main()