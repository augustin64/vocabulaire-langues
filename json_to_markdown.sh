#!/bin/bash

OUT="md"

json_to_md () 
{
	filename=$(echo "$1" | awk -F/ '{print $NF}')
	if [[ $(which jq) != *"not found" ]]; then
		jq '.' "$1" --unbuffered > "/tmp/$filename"
	else
		cp "$1" "/tmp/$filename"
	fi;
	f="/tmp/$filename"
	echo "Converting $1"
	o="${2}/$(echo "/tmp/$1" | sed -e 's/.json/.md/g' | awk -F/ '{print $NF}')"
	echo "$f" | awk -F/ '{print "# " $NF}' | sed -e 's/.json//g' -e 's/_/ /g' > "$o"
	while read line
	do
		if [[ "$line" != *"}"* && "$line" != *"{"* ]]; then
			echo "$line" | sed -e 's/"//g' -e 's/,//g' | awk -F: '{print "| "$1 " |" $2 " |"}' >> "$o"
		elif [[ "$line" == *":"*"{"* ]]; then
			title=$(echo "$line" | sed -e 's/"//g' -e 's/{//g' -e 's/: //g')
			echo -e "## $title\n|||\n|:---|:---|" >> "$o"
		fi;
	done < "$f"
	rm "$f"
}




if [[ "$1" == "" ]]; then
	files=$(ls listes/*)
else
	files="$1"
fi;

for file in $files; do
	json_to_md "$file" "$OUT"
done;
