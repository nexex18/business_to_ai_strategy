#!/usr/bin/env python3
"""
Create and populate SQLite database for presentation slides
"""

import sqlite3
import os

def create_database():
    """Create the slides database and populate it with data"""
    
    # Remove old database if it exists
    db_path = 'slides.db'
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Create new database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create slides table
    cursor.execute('''
        CREATE TABLE slides (
            num TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            title TEXT NOT NULL,
            source TEXT NOT NULL
        )
    ''')
    
    # Data to insert - matching current filenames in slides_complete/
    slides_data = [
        ("01", "vmg_overview", "Velocity MG: Making Good on AI's Promise", 
         "slide_01_velocity_mg_making_good_on_ais_promise.html"),
        
        ("02", "smb_dilemma", "The SMB AI Dilemma", 
         "slide_02_the_smb_ai_dilemma.html"),
        
        ("03", "framework", "The VMG Framework", 
         "slide_03_the_vmg_framework.html"),
        
        ("04", "ai_approach", "Our AI-Powered Approach", 
         "slide_04_our_aipowered_approach.html"),
        
        ("05", "prioritization", "Strategic Initiative Prioritization", 
         "slide_05_strategic_initiative_prioritization.html"),
        
        ("06", "content_platform", "Initiative: Intelligent Content Generation Platform", 
         "slide_06_initiative_intelligent_content_generatio.html"),
        
        ("07", "revenue_model", "Transforming the Consulting Revenue Model", 
         "slide_07_transforming_the_consulting_revenue_mode.html"),
        
        ("08", "cost_benefit", "Cost-Benefit Analysis", 
         "slide_08_costbenefit_analysis.html"),
        
        ("09", "customer_growth", "Customer Growth Assumptions", 
         "slide_09_customer_growth_assumptions.html"),
        
        ("10", "roi_analysis", "Return on Investment Analysis", 
         "slide_10_return_on_investment_analysis.html"),
        
        ("11", "timeline", "Development Timeline", 
         "slide_11_development_timeline.html"),
        
        ("12", "key_metrics", "Key Investment Metrics", 
         "slide_12_key_investment_metrics.html"),
        
        ("13", "risk_assessment", "Risk Assessment & Mitigation Strategy", 
         "slide_13_risk_assessment_mitigation_strategy.html")
    ]
    
    # Insert data
    cursor.executemany('INSERT INTO slides VALUES (?, ?, ?, ?)', slides_data)
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print(f"✅ Created {db_path} with {len(slides_data)} slides")
    print("\nDatabase contents:")
    
    # Display the data
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM slides ORDER BY num')
    
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]:20} - {row[2][:40]}...")
    
    conn.close()
    print("\n📝 You can edit this database using any SQLite browser")
    print("   or by modifying this script and re-running it")

if __name__ == "__main__":
    create_database()