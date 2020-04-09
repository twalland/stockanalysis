#!/bin/sh

# Bail out if there are any errors.
set -e

# The name of the database we're going to backup.
dbname="finance"

# The Google Drive folder ID where database exports will be uploaded to
gdrivefolderid="1i5gSz6u-F13NN_rL49WdsKYvq6Bh_Co6"

# Number of days we want to retain local backups for
retentiondays=14

# Date format for dates appended to database export files 
dateformat="%Y-%m-%d_%H:%M:%S"

# The local directory where we'll be storing database exports
dumpdir="/home/thomas/finance/db-backup"

# Options to pass to the mysqldump command
mysqlopts=""

# Make sure the directory exists
mkdir -p "$dumpdir"

# Delete local export files older than our retentiondays value
find "$dumpdir" -type f -name "*.sql.gz" -mtime +"$retentiondays" -print -exec rm "{}" \;

# Zip up any existing export files
find "$dumpdir" -type f -name "*.sql" -print -exec gzip "{}" \;

# Perform a backup of the live database
file="$dbname-$(date +$dateformat).sql"
path="$dumpdir/$file"

mysqlopts=--user=db-backup
mysqldump $mysqlopts "$dbname" > "$path"

# Upload the newly created file to Google Drive
gdrive upload --parent "$gdrivefolderid" "$path"
