SELECT * FROM users WHERE bitwise_field & (1 << $flagBitNumber);  -- left-shift BIN(1) n times === 2^n

SELECT table_name FROM information_schema.columns WHERE column_name = 'pk_field' AND table_schema = 'clientA';  -- Does this database have this column?