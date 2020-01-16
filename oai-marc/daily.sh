#!/bin/bash
#
# Crontab daily runner
#
# 00 5 * * * root daily.sh &
#

DATA_PATH='/var/www/html/daily'
ROOT_PATH='/var/www/html'

HEADER='<html>
<head><meta charset="utf-8"></head>
<body style="background-color:#000;color:#6DAE42;">
<br><b>OAI-PMH 2.0 MARCXML</b>
<br><b>--------------------------------</b><br><br>
<table>'

FOOTER='</table>
</body>
</html>'

TEMPLATE='<tr><td><p><a target="_blank" href="daily/FN" style="color:white;text-decoration:none;">FN</a></p></td></tr>'

#./oai-marc.py \
#	--set UCLA \
#	--from "$(date --date='yesterday' '+%Y-%m-%d 00:00:00')" \
#	--until "$(date --date='today' '+%Y-%m-%d 00:00:00')" \
#	--check \
#	--notify

mkdir $ROOT_PATH 2>/dev/null
mkdir $DATA_PATH 2>/dev/null

mv oai-marc.html "$DATA_PATH/$(date '+%Y-%m-%d').html"

find $DATA_PATH -maxdepth 1 -type f -mtime +14 -delete

echo "$HEADER" > "$ROOT_PATH/daily.html"

for F in $(find $DATA_PATH -type f -exec basename {} \;); do
	echo "$TEMPLATE" | sed "s/FN/$F/g" >> "$ROOT_PATH/daily.html"
done

echo "$FOOTER" >> "$ROOT_PATH/daily.html"

exit 0
