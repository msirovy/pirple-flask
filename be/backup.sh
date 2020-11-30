#!/bin/bash

logger "$(whoami) - Starting backup"

# Do mysqldump
mysqldump --add-drop-table flask | gzip > ~/backups/dump-$(date +%F).sql.gz

# Remove old backups
find ~/backups/*gz -mtime +15 -exec rm {} \;

logger "$(whoami) - Backup finished"
