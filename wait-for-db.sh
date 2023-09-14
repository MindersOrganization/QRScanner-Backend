#!/bin/bash
# wait-for-db.sh

set -e

host="qr_db"
cmd="$@"

until mysql -h "$host" -P 3307 -u "minders_qr_admin" --password="Minders@2023" -e 'SELECT 1'; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - executing command"
>&2 echo $cmd
eval $cmd
