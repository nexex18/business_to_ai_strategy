-- Insert appendix title slide and shift other appendix slides

BEGIN TRANSACTION;

-- First, shift all appendix slides (17-31) up by 1 to make room
UPDATE slides SET num = CAST(num AS INTEGER) + 100 WHERE CAST(num AS INTEGER) >= 17;

-- Now renumber them back down by 1 position higher than before
UPDATE slides SET num = CAST(num AS INTEGER) - 100 + 1 WHERE CAST(num AS INTEGER) >= 117;

-- Insert the appendix title slide at position 17
INSERT INTO slides (num, name, source, title, agenda_section) 
VALUES (17, 'slide_22_appendix_title', 'slide_22_appendix_title.html', 'Appendix', 'Appendix');

COMMIT;

-- Verify the result
SELECT num, name, title, agenda_section FROM slides WHERE CAST(num AS INTEGER) >= 15 ORDER BY CAST(num AS INTEGER);