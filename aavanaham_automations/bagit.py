
# coding: utf-8

import pandas as pd
import datetime
import subprocess


reports_folder = "/home/parathan/reportsFolder"
pids_to_create_bags = "8.csv"
bags_creation_report = "finalCSV.csv"


# Load the pid list
df = pd.read_csv(reports_folder + "/" + pids_to_create_bags)

# Loop through the pid list and create bag
creation_results = []
for index, row in df.iterrows():
    pid = row["PID"]

    # execute the command
    cmd = "sudo drush --user=1 create-islandora-bag object " + pid
    cmd_output = subprocess.getoutput(cmd)
    print(cmd_output)

    cmd1 = "sudo rm -r /tmp/islandora_bagit_tmp/"
    cmd1_output = subprocess.getoutput(cmd1)

    # Check status of running the command
    creation_status = "Fail"
    if "Bag created and saved" in str(cmd_output): 
        creation_status = "Success"
        
    # Add to result set
    timestamp = datetime.datetime.utcnow()        
    creation_results.append((pid, creation_status, timestamp))
    print(pid + " " + creation_status)


# In[17]:

df_creation_results = pd.DataFrame(creation_results, columns=('pid', 'creation_status', "created_on"))
df_creation_results.to_csv(reports_folder + "/" + bags_creation_report)
df_creation_results
