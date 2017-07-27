-- Removes all duplicate records from a tbl, leaving one record. 
-- Duplicates are identified by having the same values in a column, usually PKs or similar identifiers. The biggest Row #/ID is kept (iirc).
-- Useful for when you're adding uniqueness constraints to a tbl (the reason why this was developed with godspeed).
-- Requires 1 temp tbl and 2 full-tbl copies (the second being much smaller, usually).

SET @row = 0;
DROP TABLE IF EXISTS temp_tbl;
CREATE TABLE temp_tbl LIKE tbl;
INSERT INTO temp_tbl 
    SELECT * 
    FROM tbl 
    ORDER BY pk_1, pk_2;  -- (!) Group records without collapse/aggregation
DELETE tt.* 
FROM temp_tbl AS tt
JOIN (
    SELECT 
        pk_1,
        pk_2,
        COUNT(*) AS cnt  -- Number of duplicates in group
    FROM temp_tbl
    GROUP BY pk_1, pk_2
    HAVING COUNT(*) > 1  -- Find groups that have duplicates
) AS dupes ON dupes.pk_2 = t.pk_2 AND dupes.pk_1 = tt.pk_1
WHERE 
    (@row:=MOD(@row+1, dupes.cnt)) > 0  -- (!) Count up the duplicate records in each group, when MOD hits Zero then keep that, which resets the counter
;
DELETE FROM tbl;
INSERT INTO tbl SELECT * FROM temp_tbl;
DROP TABLE IF EXISTS temp_tbl;