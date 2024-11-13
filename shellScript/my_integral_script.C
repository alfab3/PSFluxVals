void my_integral_script(const char* flux_file) {
  TFile *file = TFile::Open(flux_file);
  if (!file || file->IsZombie()) {
    std::cerr << "Error: File could not be opened!" << std::endl;
    return;
  }
  
  TTree *tree = (TTree*)file->Get("PSFlux_Tree");
  if (!tree) {
    std::cerr << "Error: Tree 'tree_PSFlux' not found!" << std::endl;
    file->Close();
    return;
  }
  
  TBranch *branch = tree->GetBranch("PSPairEnergy");
  if (!branch) {
    std::cerr << "Error: Branch 'PSPairEnergy' not found!" << std::endl;
    file->Close();
    return;
  }
  
  TH1F *hist = new TH1F("hist", "Branch Integral", 100, 4, 6);

  tree->Draw(Form("%s >> hist", "PSPairEnergy"), Form("%s >= %f && %s <= %f", "PSPairEnergy", 4.0, "PSPairEnergy", 6.0));
  
  double integral = hist->Integral();

  // Output the result
  std::cout << integral << std::endl;
  delete hist;
  file->Close();
}
