#!/bin/bash

OUT="md"

json_to_md () 
{
	echo "Converting $1"
	outfile="${2}/$(echo "$1" | sed -e 's/.json/.md/g' | awk -F/ '{print $2}')"
	echo "$1" | awk -F/ '{print "# " $2}' | sed -e 's/.json//g' -e 's/_/ /g' > "$outfile"
	while read line
	do
		if [[ "$line" != *"}"* && "$line" != *"{"* ]]; then
			echo "$line" | sed -e 's/"//g' -e 's/,//g' | awk -F: '{print "| "$1 " |" $2 " |"}' >> "$outfile"
		elif [[ "$line" == *":{"* ]]; then
			title=$(echo "$line" | sed -e 's/"//g' -e 's/{//g')
			echo -e "## $title\n|||\n|:---|:---|" >> "$outfile"
		fi;
	done < "$1"
}




if [[ "$1" == "" ]]; then
	files=$(ls listes/*)
else
	files="$1"
fi;

for file in $files; do
	json_to_md "$file" "$OUT"
done;
