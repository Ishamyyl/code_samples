#!/usr/bin/env bash

un='redacted'
pw='redacted'
db='redacted'
port='redacted'
host='redacted'

#9 -- Adds 
while read table column type
do
	echo "ALTER TABLE $table MODIFY COLUMN $column $type NOT NULL AUTO_INCREMENT;" \
	| mysql -u $un -p$pw -h $host -P $port $db
done < <(echo "SELECT TABLE_NAME, COLUMN_NAME, COLUMN_TYPE FROM COLUMNS WHERE TABLE_SCHEMA = 'redacted' AND EXTRA = 'auto_increment';" | mysql -u $un -p$pw -h $host -P $port --skip-column-names information_schema)


#4 -- Adds data back in to database after making a manual backup
#$ ./test.sh < file.bak.txt
while read id input; do
	echo "UPDATE table SET column = $input WHERE id = $id;" | mysql -u $un -p$pw -h $host -P $port redacted
done
