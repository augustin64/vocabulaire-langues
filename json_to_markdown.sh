#!/bin/bash

OUT="md"

json_to_md () 
{
	filename=$(echo "$1" | awk -F/ '{print $NF}')
	f="/tmp/$filename"
	o="${2}/$(echo "/tmp/$1" | sed -e 's/.json/.md/g' | awk -F/ '{print $NF}')"
	title=$(echo "$f" | awk -F/ '{print $NF}' | sed -e 's/.json//g' -e 's/_/ /g')

	if [[ $(which jq) != *"not found" ]]; then
		jq '.' "$1" --unbuffered > "/tmp/$filename"
	else
		cp "$1" "/tmp/$filename"
	fi;

	echo "Converting $1"
	echo "# $title" > $o
	while read line
	do
		if [[ "$line" != *"}"* && "$line" != *"{"* ]]; then
			echo "$line" | sed -e 's/"//g' -e 's/,//g' | awk -F: '{print "| "$1 " |" $2 " |"}' >> "$o"
		elif [[ "$line" == *":"*"{"* ]]; then
			theme_title=$(echo "$line" | sed -e 's/"//g' -e 's/{//g' -e 's/: //g')
			echo -e "\n## $theme_title\n|||\n|:---|:---|" >> "$o"
		fi;
	done < "$f"
	rm "$f"
	# Ajoute le fichier à la liste des listes si il n'y ait pas déjà
	if [[ -e md/README.md && $(cat md/README.md) != *"$title"* ]]; then
		echo "|[$title]($(echo $o | awk -F/ '{print $NF}'))|" >> "md/README.md"
	fi;
}




if [[ "$1" == "" ]]; then
	files=$(ls listes/*)
else
	files="$1"
fi;

for file in $files; do
	json_to_md "$file" "$OUT"
done;
