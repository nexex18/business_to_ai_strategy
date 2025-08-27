-- Reorganize slides to move 5 slides to appendix
-- Moving: 06 (porters), 08 (market), 10 (core strategies), 11 (three moats), 18 (roi)

BEGIN TRANSACTION;

-- First, temporarily move the slides to be moved to high numbers
UPDATE slides SET num = 106 WHERE num = 6;  -- porters_five_forces
UPDATE slides SET num = 108 WHERE num = 8;  -- market_opportunity
UPDATE slides SET num = 110 WHERE num = 10; -- core_strategies
UPDATE slides SET num = 111 WHERE num = 11; -- three_moats
UPDATE slides SET num = 118 WHERE num = 18; -- roi_analysis

-- Now renumber the remaining slides to fill gaps
-- After removing 6, slide 7 becomes 6
UPDATE slides SET num = 6 WHERE num = 7;   -- smb_ai_dilemma

-- After removing 8, slide 9 becomes 7
UPDATE slides SET num = 7 WHERE num = 9;   -- vmg_built_for_ai

-- After removing 10 and 11, slide 12 becomes 8
UPDATE slides SET num = 8 WHERE num = 12;  -- assessment_graph

-- Slides 13-17 move up by 4 positions
UPDATE slides SET num = 9 WHERE num = 13;  -- initiatives_with_pillars
UPDATE slides SET num = 10 WHERE num = 14; -- strategic_prioritization
UPDATE slides SET num = 11 WHERE num = 15; -- financial_overview
UPDATE slides SET num = 12 WHERE num = 16; -- customer_growth_assumptions
UPDATE slides SET num = 13 WHERE num = 17; -- cost_benefit_analysis

-- After removing 18, slides 19-32 move up by 5 positions
UPDATE slides SET num = 14 WHERE num = 19; -- development_timeline
UPDATE slides SET num = 15 WHERE num = 20; -- risk_assessment
UPDATE slides SET num = 16 WHERE num = 21; -- conclusion
UPDATE slides SET num = 17 WHERE num = 22; -- appendix_title
UPDATE slides SET num = 18 WHERE num = 23; -- content_generation
UPDATE slides SET num = 19 WHERE num = 24; -- content_scores
UPDATE slides SET num = 20 WHERE num = 25; -- discovery_suite
UPDATE slides SET num = 21 WHERE num = 26; -- discovery_scores
UPDATE slides SET num = 22 WHERE num = 27; -- command_center
UPDATE slides SET num = 23 WHERE num = 28; -- command_scores
UPDATE slides SET num = 24 WHERE num = 29; -- continuous_monitor
UPDATE slides SET num = 25 WHERE num = 30; -- monitor_scores
UPDATE slides SET num = 26 WHERE num = 31; -- knowledge_system
UPDATE slides SET num = 27 WHERE num = 32; -- knowledge_scores

-- Now add the moved slides to the end as appendix items
UPDATE slides SET num = 28 WHERE num = 106; -- porters_five_forces
UPDATE slides SET num = 29 WHERE num = 108; -- market_opportunity  
UPDATE slides SET num = 30 WHERE num = 110; -- core_strategies
UPDATE slides SET num = 31 WHERE num = 111; -- three_moats
UPDATE slides SET num = 32 WHERE num = 118; -- roi_analysis

-- Update agenda sections for moved slides
UPDATE slides SET agenda_section = 'Appendix' WHERE num IN (28, 29, 30, 31, 32);

COMMIT;

-- Verify the new order
SELECT num, name, agenda_section FROM slides ORDER BY num;