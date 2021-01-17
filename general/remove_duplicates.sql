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
    ORDER BY pk_1, pk_2;  -- (!) Group records without collapse/aggregation [1]
DELETE tt.* 
FROM temp_tbl AS tt
JOIN (
    SELECT 
        pk_1,
        pk_2,
        COUNT(*) AS cnt  -- Number of duplicates in group [2]
    FROM temp_tbl
    GROUP BY pk_1, pk_2
    HAVING COUNT(*) > 1  -- Find groups that have duplicates [3]
) AS dupes ON dupes.pk_2 = tt.pk_2 AND dupes.pk_1 = tt.pk_1
WHERE 
    (@row:=MOD(@row+1, dupes.cnt)) > 0  -- (!) [4] Count up the duplicate records in each group, when MOD hits Zero then keep that, which resets the counter
;
DELETE FROM tbl;
INSERT INTO tbl SELECT * FROM temp_tbl;
DROP TABLE IF EXISTS temp_tbl;
               
/*
               Imagine you have are tasked with distributing an entire regular playing card deck to 52 people.
               You see that a blackjack shoe works well at distributing cards and decide to use that.
               However, after distributing, you start to hear "cool I have the Ace of Spaces" multiple times from the group, 
               and you realize there's a problem: you learn that blackjack shoes have between 6 and 8 decks of cards, and you distributed duplicate cards to people.
               
               There's an unknown number of possible duplicates. 
               There's no point in telling everyone to turn in their card, so you only need to keep one person around.
               There aren't any other features to identify possible duplicates (e.g. all 6-8 decks have the same back).
               How do you fix this?
               
               First, have the people group up together by their card in a line [1]. Have them note how many people are in their group [2], and ignore groups of 1 [3].
               Then, go down the line and have each group tell you their group size [2]. Count off that many people, and tell the last one to stay [4].
               
               [4]
               You: "how many king of clubs?"
               Group: "5"
               You, counting off: 
                    1, go turn your card in...  
                    2, go...  
                    3, go...  
                    4, go....  
                    and 5, stay"
               
               1 MOD 5 = 1, which is greater than 0, so delete. @row is 0, then is set to 1 (the result of 1 MOD 5).
               2 MOD 5 = 2, which is greater than 0, so delete. @row is 1, then is set to 2.
               3 MOD 5 = 3, *
               4 MOD 5 = 4, *
               5 MOD 5 = 0, so keep. @row is 4, then is set to 0.
*/
