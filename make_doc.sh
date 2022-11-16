#!/bin/bash
roles=(redelk_client redelk_server)

for role in ${roles[@]}; do
  echo -e "Processing role $role\n\n"
  SAVEIFS=$IFS
  IFS=$'\n'
  variables=$(cat roles/$role/defaults/main.yml | grep -v -E '(^#|---|^\s*-)' --color=never)

  echo "| Variable | Description | Default value |"
  echo "|----------|-------------|---------------|"
  for var in $variables; do
    key=$(echo $var | cut -d ':' -f 1)
    val=$(echo $var | cut -d ':' -f 2- | sed -E -e 's/(^\s*)"*//g' | sed -E -e 's/"$//g')
    descr=$(cat roles/$role/defaults/main.yml | grep -E "(^#\s*${key}\s*\|)" | cut -d '|' -f 2- | sed -E -e 's/^\s*//g')
    echo "| \`$key\` | $descr | \`$val\` |"
  done
  echo -e "\n\n"
  IFS=$SAVEIFS

done
