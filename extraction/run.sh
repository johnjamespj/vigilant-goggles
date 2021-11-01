UNIT_COUNT=100
DUMP=~/data/human_entities_backup.csv.bz2
BUCKET=vg-embedding

UNIT_COUNT=${UNIT_COUNT} DUMP=${DUMP} BUCKET=${BUCKET} python3 main.py
