import configparser
import argparse
import os
import re
import ROOT

#input_topdir = '/volatile/halld/home/alfab/CPP_REACTIONFILTER/fulltarget/pippim/tree_gpb208_pippimmisspb208__B4/'
#flux_dir = '/cache/halld/RunPeriod-2022-05/recon/ver01/tree_PSFlux/'

def get_file_numbers(directory):
    files = os.listdir(directory)
    
    pattern = re.compile(r'.*_(\d{3})\.root$')
    numbers = set()
    for filename in files:
        match = pattern.match(filename)
        if match:
            numbers.add(match.group(1))
    return sorted(numbers)

def find_matching_files(flux_dir,run_number,numbers):
    matching_files = []
    for number in numbers:
        filename = f"{run_number}/tree_PSFlux_{run_number}_{number}.root"
        file_path = os.path.join(flux_dir, filename)
        if os.path.exists(file_path):
            matching_files.append(file_path)
    return matching_files

def integrate_over_branch(files, branch_name, lower_bound, upper_bound):
    total_integral = 0
    for file_path in files:

        root_file = ROOT.TFile(file_path)
        tree = root_file.Get('PSFlux_Tree')

        print("Integrating File: ")
        print(file_path)

        if tree:

            hist = ROOT.TH1F("hist", "Histogram", 100, lower_bound, upper_bound)


            tree.Project("hist", branch_name)


            integral = hist.Integral()
            total_integral += integral
            print("total_integral")
            print(total_integral)
        else:
            print(f"Tree not found in {file_path}")

        root_file.Close()
        

    return total_integral

def process_files(input_dir, flux_dir, branch_name, lower_bound, upper_bound,start_run,end_run):

    i = start_run
    total_integral_over_runs = 0
    while i <= end_run:
        source_dir = input_dir + str(i) + '/'
        numbers = get_file_numbers(source_dir)
        matching_files = find_matching_files(flux_dir, i ,numbers)
        if not matching_files:
            print("No matching files found.")
            return
        total_integral = integrate_over_branch(matching_files, branch_name, lower_bound, upper_bound)
        print(f"Total integral over PSFluxEnergy for run: '{i}': {total_integral}")
        total_integral_over_runs += total_integral
        i += 1
    print(f"Total integral over PSFluxEnergy for all selected runs: {total_integral_over_runs}")
if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('settings.config')

    input_topdir = config['Directories']['INPUT_TOPDIR']
    flux_topdir = config['Directories']['FLUX_DIR']
    
    start_run = config['OtherSettings'].getint('START_RUN')
    end_run = config['OtherSettings'].getint('END_RUN')


    
    process_files(
        input_dir = input_topdir,
        flux_dir = flux_topdir,
        branch_name='PSPairEnergy', 
        lower_bound=0.0,
        upper_bound=12.0,
        start_run = start_run,
        end_run = end_run
    )
