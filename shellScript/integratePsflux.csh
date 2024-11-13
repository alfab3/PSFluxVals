#!/bin/csh

set directory_path_1 = "/volatile/halld/home/alfab/CPP_REACTIONFILTER/fulltarget/pippim/tree_gpb208_pippimmisspb208__B4/101582/" 
set directory_path_2 = "/cache/halld/RunPeriod-2022-05/recon/ver01/tree_PSFlux/101582/"  
set output_numbers_file = "output_numbers.txt"      
set output_integral_file = "integral_results.txt"   


echo "" > $output_numbers_file
echo "" > $output_integral_file


foreach file ($directory_path_1/tree_gpb208_pippimmisspb208__B4_*.root)
  set number = `basename $file | sed -E 's/.*_([0-9]+)\.root/\1/'`
  echo $number >> $output_numbers_file
end


sort -n $output_numbers_file | uniq > temp_file && mv temp_file $output_numbers_file
set counter = 0

foreach number (`cat $output_numbers_file`)

  @ counter++
  set flux_file = "$directory_path_2/tree_PSFlux_101582_${number}.root"
  

  if (-e $flux_file) then

    
    root -b -l -q 'my_integral_script.C("'$flux_file'")' >> $output_integral_file

  else
    echo "$number: File not found" >> $output_integral_file
  endif
end

echo "Process complete. Integral results saved to $output_integral_file."
