import pandas as pd

infile_path="/app/IDRC/XTR/CMS/data/DashboardVolRptData_2024_CY_20250108.144617.txt"
outfile_path="/app/IDRC/XTR/CMS/data/DashboardVolRptData_2024_CY_20250108.144617.csv"

df = pd.read_csv(infile_path,sep='|') 

df.to_csv(outfile_path)
   