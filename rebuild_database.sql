-- Clear and rebuild the slides table with the correct order

BEGIN TRANSACTION;

-- Clear the existing data
DELETE FROM slides;

-- Insert all slides in the new order
INSERT INTO slides (num, name, source, title, agenda_section) VALUES
(1, 'slide_01_title', 'slide_01_title.html', 'Title', 'Title'),
(2, 'slide_02_agenda', 'slide_02_agenda.html', 'Agenda', 'Agenda'),
(3, 'slide_03_executive_summary', 'slide_03_executive_summary.html', 'Executive Summary', 'Background'),
(4, 'slide_04_evolution_combined', 'slide_04_evolution_combined.html', 'Evolution of Consulting', 'Background'),
(5, 'slide_05_competitive_landscape', 'slide_05_competitive_landscape.html', 'Competitive Landscape', 'Competitive Landscape'),
(6, 'slide_07_smb_ai_dilemma', 'slide_07_smb_ai_dilemma.html', 'SMB AI Dilemma', 'Internal Assessment'),
(7, 'slide_09_vmg_built_for_ai', 'slide_09_vmg_built_for_ai.html', 'VMG Built for AI', 'Business & AI Strategies'),
(8, 'slide_12_assessment_graph', 'slide_12_assessment_graph.html', 'AI Maturity Assessment', 'AI Maturity'),
(9, 'slide_13_initiatives_with_pillars', 'slide_13_initiatives_with_pillars.html', 'Strategic Initiatives', 'AI Initiatives'),
(10, 'slide_14_strategic_prioritization', 'slide_14_strategic_prioritization.html', 'Strategic Prioritization', 'AI Initiatives'),
(11, 'slide_15_financial_overview', 'slide_15_financial_overview.html', 'Financial Overview', 'AI Initiatives'),
(12, 'slide_16_customer_growth_assumptions', 'slide_16_customer_growth_assumptions.html', 'Customer Growth Assumptions', 'Financial Analysis'),
(13, 'slide_17_cost_benefit_analysis', 'slide_17_cost_benefit_analysis.html', 'Cost-Benefit Analysis', 'Financial Analysis'),
(14, 'slide_19_development_timeline', 'slide_19_development_timeline.html', 'Development Timeline', 'Timeline'),
(15, 'slide_20_risk_assessment', 'slide_20_risk_assessment.html', 'Risk Assessment', 'Risks & Mitigations'),
(16, 'slide_21_conclusion', 'slide_21_conclusion.html', 'Conclusion', 'Conclusion'),
(17, 'slide_06_porters_five_forces', 'slide_06_porters_five_forces.html', 'Porter''s Five Forces', 'Appendix'),
(18, 'slide_08_market_opportunity', 'slide_08_market_opportunity.html', 'Market Opportunity', 'Appendix'),
(19, 'slide_10_core_strategies', 'slide_10_core_strategies.html', 'Core Strategies', 'Appendix'),
(20, 'slide_11_three_moats', 'slide_11_three_moats.html', 'Three Moats', 'Appendix'),
(21, 'slide_18_roi_analysis', 'slide_18_roi_analysis.html', 'ROI Analysis', 'Appendix'),
(22, 'slide_23_content_generation', 'slide_23_content_generation.html', 'Content Generation', 'Appendix'),
(23, 'slide_24_content_scores', 'slide_24_content_scores.html', 'Content Scores', 'Appendix'),
(24, 'slide_25_discovery_suite', 'slide_25_discovery_suite.html', 'Discovery Suite', 'Appendix'),
(25, 'slide_26_discovery_scores', 'slide_26_discovery_scores.html', 'Discovery Scores', 'Appendix'),
(26, 'slide_27_command_center', 'slide_27_command_center.html', 'Command Center', 'Appendix'),
(27, 'slide_28_command_scores', 'slide_28_command_scores.html', 'Command Scores', 'Appendix'),
(28, 'slide_29_continuous_monitor', 'slide_29_continuous_monitor.html', 'Continuous Monitor', 'Appendix'),
(29, 'slide_30_monitor_scores', 'slide_30_monitor_scores.html', 'Monitor Scores', 'Appendix'),
(30, 'slide_31_knowledge_system', 'slide_31_knowledge_system.html', 'Knowledge System', 'Appendix'),
(31, 'slide_32_knowledge_scores', 'slide_32_knowledge_scores.html', 'Knowledge Scores', 'Appendix');

COMMIT;

-- Verify the result
SELECT num, name, agenda_section FROM slides ORDER BY num;