#!/bin/csh

set directory_path = "/volatile/halld/home/alfab/CPP_REACTIONFILTER/fulltarget/pippim/tree_gpb208_pippimmisspb208__B4/101582/"

set output_file = "output_numbers.txt"

echo "" > $output_file


foreach file ($directory_path/tree_gpb208_pippimmisspb208__B4_101582_*.root)

  set number = `basename $file | sed -E 's/.*_([0-9]+)\.root/\1/'`


  echo $number >> $output_file
end


sort -n $output_file | uniq > temp_file && mv temp_file $output_file

echo "The numbers have been extracted and saved to $output_file."
