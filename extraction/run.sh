UNIT_COUNT=100
DUMP=~/data/human_entities_backup.csv.bz2
BUCKET=vg-embedding
START=5700

UNIT_COUNT=${UNIT_COUNT} DUMP=${DUMP} BUCKET=${BUCKET} START=${START} python3 main.py
