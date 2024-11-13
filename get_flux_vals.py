import os
import re
import ROOT

#source_dir = '/volatile/halld/home/alfab/CPP_REACTIONFILTER/fulltarget/pippim/tree_gpb208_pippimmisspb208__B4/101582/'
#flux_dir = '/cache/halld/RunPeriod-2022-05/recon/ver01/tree_PSFlux/101582/'

def get_file_numbers(directory):
    files = os.listdir(directory)
    pattern = re.compile(r'.*_(\d{3})\.root$')
    numbers = set()
    for filename in files:
        match = pattern.match(filename)
        if match:
            numbers.add(match.group(1))
    return sorted(numbers)

def find_matching_files(flux_dir, numbers):
    matching_files = []
    for number in numbers:
        filename = f"tree_PSFlux_101604_{number}.root"
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

def process_files(source_dir, flux_dir, branch_name, lower_bound, upper_bound):

    numbers = get_file_numbers(source_dir)
    

    matching_files = find_matching_files(flux_dir, numbers)
    
    if not matching_files:
        print("No matching files found.")
        return
    

    total_integral = integrate_over_branch(matching_files, branch_name, lower_bound, upper_bound)
    print(f"Total integral over branch '{branch_name}': {total_integral}")
if __name__ == "__main__":
    process_files(
        #source_dir = '/volatile/halld/home/alfab/CPP_REACTIONFILTER/fulltarget/pippim/tree_gpb208_pippimmisspb208__B4/101582/',
        source_dir = '/volatile/halld/home/alfab/CPP_REACTIONFILTER/mttarget/pippim/tree_gpb208_pippimmisspb208__B4/101604/',
        #flux_dir = '/cache/halld/RunPeriod-2022-05/recon/ver01/tree_PSFlux/101582/',
        flux_dir = '/cache/halld/RunPeriod-2022-05/recon/ver01/tree_PSFlux/101604/',
        branch_name='PSPairEnergy', 
        lower_bound=4.0,
        upper_bound=6.0 
    )
