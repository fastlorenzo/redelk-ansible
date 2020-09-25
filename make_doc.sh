#!/bin/bash

SAVEIFS=$IFS
IFS=$'\n'
variables=$(cat roles/redelk-server/defaults/main.yml | grep -v -E '(^#|---)' --color=never)

echo "| Variable | Description | Default value |"
echo "|----------|-------------|---------------|"
for var in $variables; do
  key=$(echo $var | cut -d ':' -f 1)
  val=$(echo $var | cut -d ':' -f 2- | sed -E -e 's/(^\s*)"*//g' | sed -E -e 's/"$//g')
  descr=$(cat roles/redelk-server/defaults/main.yml | grep -E "(^#\s*${key}\s*\|)" | cut -d '|' -f 2- | sed -E -e 's/^\s*//g')
  echo "| \`$key\` | $descr | \`$val\` |"
done

IFS=$SAVEIFS
