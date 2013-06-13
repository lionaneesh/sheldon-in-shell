DB_PATH="SheldonQuotes"
sqlite3 $DB_PATH "SELECT quote || ' --- ' || source from Quotes ORDER BY RANDOM() LIMIT 1;"
