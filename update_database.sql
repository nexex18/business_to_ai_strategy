-- Clear existing data
DELETE FROM slides;

-- Insert slides with correct filenames
INSERT INTO slides (num, name, title, source, agenda_section) VALUES
('01', 'slide_01_title', 'Title', 'slide_01_title.html', 'Introduction'),
('02', 'slide_02_agenda', 'Agenda', 'slide_02_agenda.html', 'Introduction'),
('03', 'slide_03_executive_summary', 'Executive Summary', 'slide_03_executive_summary.html', 'Background'),
('04', 'slide_04_evolution_combined', 'Evolution of Consulting', 'slide_04_evolution_combined.html', 'Background'),
('05', 'slide_05_competitive_landscape', 'Competitive Landscape', 'slide_05_competitive_landscape.html', 'Competitive Landscape'),
('06', 'slide_07_porters_five_forces', 'Porter''s Five Forces', 'slide_07_porters_five_forces.html', 'Internal Assessment'),
('07', 'slide_08_smb_ai_dilemma', 'SMB AI Dilemma', 'slide_08_smb_ai_dilemma.html', 'Opportunity'),
('08', 'slide_09_market_opportunity', 'Market Opportunity', 'slide_09_market_opportunity.html', 'Opportunity'),
('09', 'slide_06_vmg_built_for_ai', 'VMG Built for AI', 'slide_06_vmg_built_for_ai.html', 'Business & AI Strategies'),
('10', 'slide_12_three_moats', 'Three Moats', 'slide_12_three_moats.html', 'Business & AI Strategies'),
('11', 'slide_14_assessment_graph', 'AI Maturity Assessment', 'slide_14_assessment_graph.html', 'AI Maturity'),
('12', 'slide_15_initiatives_with_pillars', 'Strategic Initiatives', 'slide_15_initiatives_with_pillars.html', 'AI Initiatives'),
('13', 'slide_16_strategic_prioritization', 'Strategic Prioritization', 'slide_16_strategic_prioritization.html', 'AI Initiatives'),
('14', 'slide_18_financial_overview', 'Financial Overview', 'slide_18_financial_overview.html', 'AI Initiatives'),
('15', 'slide_09_customer_growth_assumptions', 'Customer Growth Assumptions', 'slide_09_customer_growth_assumptions.html', 'Financial Analysis'),
('16', 'slide_19_cost_benefit_analysis', 'Cost-Benefit Analysis', 'slide_19_cost_benefit_analysis.html', 'Financial Analysis'),
('17', 'slide_20_roi_analysis', 'ROI Analysis', 'slide_20_roi_analysis.html', 'Financial Analysis'),
('18', 'slide_22_development_timeline', 'Development Timeline', 'slide_22_development_timeline.html', 'Timeline'),
('19', 'slide_23_risk_assessment', 'Risk Assessment', 'slide_23_risk_assessment.html', 'Risks & Mitigations'),
('20', 'slide_24_conclusion', 'Conclusion', 'slide_24_conclusion.html', 'Conclusion');
