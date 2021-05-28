# -*- coding: utf-8 -*-
"""
Created on Fri May 28 12:50:09 2021
@author: kmacdonald
"""
#created & tested on PC using:
# pandas v1.1.3
# python v3.8.5


#import packages I need
import glob
import os
import subprocess
import fnmatch
import pandas as pd
import numpy as np


# Store current date in a variable:
from datetime import datetime
Today = datetime.today().strftime('%Y-%m-%d')   # output is like '2021-01-26'  

#---------------------import and process QC SUMMARY file-----------------------------

# Read in QCsummary excel file (Sheet1):
df_QCsummary0 = pd.read_excel('C:/Path/to/QCsummaryFile/Runs_CombinedQCsummary.xlsx', sheet_name=0)
# print(df_QCsummary0)


# Parse SampleID out of new sampleIDs (if fastqIDs look like: R1234567890-201-D-E03) (or leave out (Comment out) if just have CID or other sampleID you want left as-is):
LibNum_split_QC = df_QCsummary0['sample'].str.split("-")
#print(LibNum_split_QC)
# store the 2nd value between -'s as a variable (this is for samples that start with E or R (named like R1234567890-201-D-E03)):
LibNum0_QC = df_QCsummary0['sample'].str.split("-").str[1]
#print(LibNum0_QC)
# store the 3rd value btwn -'s as a variable (this is for pos/neg cntrls (named like: NEG20210331-nCoVWGS-201-D)):
LibNum1_QC = df_QCsummary0['sample'].str.split("-").str[2]
#print(LibNum1_QC)
# store the 1st value (before 1st -) - the sampleID, as a variable:
SampleID_QC = df_QCsummary0['sample'].str.split("-").str[0]
#print(SampleID_QC)
#store the LibNum0_QC length in a variable:
SampleLength_QC = LibNum0_QC.str.len()
#print(SampleLength_QC)
#print(SampleLength_QC.loc[1]) 


#REPLACE SAMPLE string in sample column with SampleID variable (just the CID part, instead of the fastqID) (leave out if doesn't apply):

conditions = [
    (SampleLength_QC < 5),    
    (SampleLength_QC > 5)
]

choices = [SampleID_QC, df_QCsummary0['sample']]

df_QCsummary0['sample'] = np.select(conditions, choices, default= df_QCsummary0['sample'])
#print(df_QCsummary0['sample'])  #correct

# Replace contents of SampleID_RunID with the concatenated field values
SampleID_RunID_qc = (df_QCsummary0["sample"].astype(str)) + '_' + (df_QCsummary0["run_name"].astype(str))
#print(SampleID_RunID_qc)    #correct

# Create New Column for, and Combine, SampleID_RunID:
df_QCsummary0.insert(35, "SampleID_RunID", SampleID_RunID_qc)
#print(df_QCsummary0)   #36 columns, inc index

# # Check you have the columns you want:
# print(df_QCsummary0.iloc[:, 0:17])   #correct (Useless# - qc_pass_x)
# print(df_QCsummary0.iloc[:, 18:23])  #correct (watch_mutns - propn_watchlist..)
# print(df_QCsummary0.iloc[:, 25:36])  #correct (pct_N_bases - SampleID_RunID)

# Sort & Remove repeats/duplicates (based on new SampleID_RunID column created above): (Now that everything on diff runs should have a unique name)
df_QCsummary0 = df_QCsummary0.sort_values('SampleID_RunID', ascending=False)
df_QCsummary0 = df_QCsummary0.drop_duplicates(subset=['SampleID_RunID'], keep='last') #if a sample is repeated b/c it failed the first time, keep the 2nd/last occurrence.
#print(df_QCsummary0)   #36 columns, inc index




#------------------NEWEST LINEAGES---------------------------

# Read in Updated Pangolin lineages file: (transfer from server to folder below, so you can read it in on your PC)
# File produced on server from pangolin pipeline, that runs newest version on all sequence data in COVID directory on server, will have name: [date]_pangolin_lineages.csv )
path = "S:/Path/To/UpdatedLineage/File/*_pangolin_lineages.csv"

for filename in glob.glob(path):
    with open(filename, 'r') as f:
        print(f)
        df_lineages0a = pd.read_csv(f)

# Set order of columns in lineage file, so are always compatible with lines below:
df_lineages0 = df_lineages0a[['run_id', 'sample_id', 'genome_completeness', 'genome_completness_status', 'lineage', 'conflict', 'pangoLEARN_version', 'pangolin_version', 'pango_version', 'status', 'note']]
 

# Parse SampleID out of new sampleIDs (if fastqIDs look like: R1234567890-201-D-E03) (or leave/comment out, if just have CID):
LibNum_split_Lin = df_lineages0['sample_id'].str.split("-")
#print(LibNum_split_Lin)
# store the 2nd value between -'s as a variable (this is for samples that start with E or R (named like R1234567890-201-D-E03)):
LibNum0_Lin = df_lineages0['sample_id'].str.split("-").str[1]
#print(LibNum0_Lin)
# store the 3rd value btwn -'s as a variable (this is for pos/neg cntrls (named like: NEG20210331-nCoVWGS-201-D)):
LibNum1_Lin = df_lineages0['sample_id'].str.split("-").str[2]
#print(LibNum1_Lin)
# store the 1st value (before 1st -) - the sampleID, as a variable:
SampleID_Lin = df_lineages0['sample_id'].str.split("-").str[0]
#print(SampleID_Lin)
#store the LibNum0_Lin length in a variable:
SampleLength_Lin = LibNum0_Lin.str.len()
#print(SampleLength_Lin)
#print(SampleLength_Lin.loc[1])    



#REPLACE SAMPLE string in sample column with SampleID variable (just the CID):

conditions = [
    (SampleLength_Lin < 5),    
    (SampleLength_Lin > 5)
]

choices = [SampleID_Lin, df_lineages0['sample_id']]

df_lineages0['sample_id'] = np.select(conditions, choices, default= df_lineages0['sample_id'])
#print(df_lineages0['sample_id'])  #correct


# Replace contents of SampleID_RunID with the concatenated field values
SampleID_RunID_lin = (df_lineages0["sample_id"].astype(str)) + '_' + (df_lineages0["run_id"].astype(str))
#print(SampleID_RunID_lin)    #correct


# Create New column for, and Combine, SampleID_RunID:
df_lineages0.insert(11, "SampleID_RunID", SampleID_RunID_lin)
#print(df_lineages0)   # 11 columns, inc index


# Sort & Remove repeats/duplicates (based on new SampleID_RunID column created above): (Now that everything on diff runs should have a unique name)
df_lineages0 = df_lineages0.sort_values('SampleID_RunID', ascending=False)
df_lineages0 = df_lineages0.drop_duplicates(subset=['SampleID_RunID'], keep='last') #if a sample is repeated b/c it failed the first time, keep the 2nd/last occurrence.
#print(df_lineages0)   # 11 columns, inc index



#-------------------------MERGE 2 OUTPUT FILES (QC Summary and Lineages) INTO FINAL FILE------------------

# Merge QC summary output and lineages output (based on SampleID_RunID column created in each) 
# (if you didn't create this column (I created it, to create a more unique ID, so repeats don't conflict), then merge based on the columns in each that match - e.g. sample and sample_id)
df_QCsummary_UpdatedLineages_merge = pd.merge(df_QCsummary0, df_lineages0, how='left', left_on='SampleID_RunID', right_on='SampleID_RunID')
#print(df_QCsummary_UpdatedLineages_merge) #works (46 columns, inc index)

# Just Keep Columns you want from merged file:
df_QCsummary_UpdatedLineages_merge3a = df_QCsummary_UpdatedLineages_merge[['UselessNumber', 'sample', 'run_name', 'num_consensus_snvs', 'num_consensus_n', 'num_consensus_iupac', 'num_variants_snvs', 'num_variants_indel', 'num_variants_indel_triplet', 'mean_sequencing_depth', 'median_sequencing_depth', 'qpcr_ct', 'collection_date', 'num_weeks', 'scaled_variants_snvs', 'genome_completeness_x', 'qc_pass_x', 'lineage', 'watch_mutations', 'watchlist_id', 'num_observed_mutations', 'num_mutations_in_watchlist', 'proportion_watchlist_mutations_observed', 'note_y', 'pangoLEARN_version_y', 'pct_N_bases', 'pct_covered_bases', 'longest_no_N_run', 'num_aligned_reads', 'qc_pass_y', 'sample_name', 'VariantYesNo', 'VariantType', 'LibraryNum', 'RunNum', 'SampleID_RunID', 'pangolin_version']]

# Format Coll Date column so output is like '2021-01-26' (with no time):
df_QCsummary_UpdatedLineages_merge3[['collection_date']] = pd.to_datetime(df_QCsummary_UpdatedLineages_merge3a['collection_date']).dt.date


# Sort by Run_Name (run_name column), then qc_pass_y (descending), then pct_covered_bases (Descending), then sample:
df_QCsummary_UpdatedLineages_merge4 = df_QCsummary_UpdatedLineages_merge3.sort_values(['run_name', 'qc_pass_y', 'pct_covered_bases', 'sample'], ascending = (True, False, False, True))  




#--------------------Re-Call VoCs in New File Using NEW Lineages-------------

# You can add to these, and they'll be called below:
Positive_values = ['B.1.1.7', 'B.1.351', 'P.1', 'B.1.617', 'B.1.617.1', 'B.1.617.2', 'B.1.617.3']
VUI_Values = ['B.1.427', 'B.1.429', 'B.1.525', 'B.1.526', 'B.1.526.1', 'B.1.1.318', 'P.1.1', 'P.2', 'P.3', 'A.23.1', 'A.27']
Other_values = ['B.1.618']

df_VariantReqMatch0 = df_QCsummary_UpdatedLineages_merge4


# Fill VariantYesNo Column with Yes/No/Failed/Possible values based on criteria: (don't need to update values here or in conditions below)
conditions = [
    #Fail anything with Excess Ambiguity:
    (df_VariantReqMatch0['qc_pass_x'].astype(str).str.contains('EXCESS_AMBIGUITY')),
    #Fail everything else that fails:
    # Fails:
    #updated to capture anything with blank values (removed from pipeline b/c not enough data) as Failed as well (otherwise are erroneously assigned as Not a Voc)
    (df_VariantReqMatch0['pct_covered_bases'] < 85.00),
    #(df_VariantReqMatch0['lineage'].isnull()),
    #(df_VariantReqMatch0['lineage'].eq('None')) & (df_VariantReqMatch0['pct_covered_bases'] == 0),
    (df_VariantReqMatch0['lineage'].eq('None')) & (df_VariantReqMatch0['pct_covered_bases'] < 85.00),
    (pd.isnull(df_VariantReqMatch0['lineage'])) & (pd.isnull(df_VariantReqMatch0['pct_covered_bases'])),
    #Capture Positives, VOIs, Other: 
    (df_VariantReqMatch0['lineage'].isin(Positive_values)),
    (df_VariantReqMatch0['lineage'].isin(VUI_Values)),
    (df_VariantReqMatch0['lineage'].isin(Other_values)),
    # Possibles:
    (df_VariantReqMatch0['lineage'].eq('None')) & (df_VariantReqMatch0['num_observed_mutations'] > 4),
    # Warnings: (Include Warning flag for samples with a non-VoC/VUI/VoI lineage AND num_observed_mutations > 4 (may be mixed sample):
    (~df_VariantReqMatch0['lineage'].eq('None')) & (pd.notnull(df_VariantReqMatch0['lineage'])) & (~df_VariantReqMatch0['lineage'].isin(Positive_values) | ~df_VariantReqMatch0['lineage'].isin(VUI_Values) | ~df_VariantReqMatch0['lineage'].isin(Other_values)) & (df_VariantReqMatch0['num_observed_mutations'] > 4),  
    #(df_VariantReqMatch0['lineage'].eq('none')) & (df_ncovtoolsSummary_plusMissing['pct_covered_bases'] < 85.00),
    # Not a VoC:
    (df_VariantReqMatch0['lineage'] != 'None')
]

choices = ['Failed (Excess Ambiguity)','Failed', 'Failed','Failed','Yes','Yes (VOI)', 'Yes (Other Variant of Interest)', 'Possible','Warning','No']


df_VariantReqMatch0['VariantYesNo'] = np.select(conditions, choices, default='No')
#print(df_VariantReqMatch0)  #correct


# You can add to these (add a new line(s) (e.g. below line 230) and copy the above line, but change the lineage of interest. Remember to add the comma after, like the others)
# ***If you add to conditions2, you'll need to add to choices2, as well
conditions2 = [
    (df_VariantReqMatch0['VariantYesNo'].eq('Failed (Excess Ambiguity)')),
    (df_VariantReqMatch0['VariantYesNo'].eq('Failed')),
    (df_VariantReqMatch0['lineage'] == "B.1.1.7"),
    (df_VariantReqMatch0['lineage'] == "B.1.351"),
    (df_VariantReqMatch0['lineage'] == "P.1"),
    (df_VariantReqMatch0['lineage'] == "B.1.617"),
    (df_VariantReqMatch0['lineage'] == "B.1.617.1"),
    (df_VariantReqMatch0['lineage'] == "B.1.617.2"),
    (df_VariantReqMatch0['lineage'] == "B.1.617.3"),
    (df_VariantReqMatch0['lineage'] == "B.1.525"),
    (df_VariantReqMatch0['lineage'] == "B.1.427"),
    (df_VariantReqMatch0['lineage'] == "B.1.429"),
    (df_VariantReqMatch0['lineage'] == "B.1.526"),
    (df_VariantReqMatch0['lineage'] == "B.1.526.1"),
    (df_VariantReqMatch0['lineage'] == "P.1.1"),
    (df_VariantReqMatch0['lineage'] == "P.2"),
    (df_VariantReqMatch0['lineage'] == "P.3"),
    (df_VariantReqMatch0['lineage'] == "B.1.1.318"),
    (df_VariantReqMatch0['lineage'] == "A.23.1"),
    (df_VariantReqMatch0['lineage'] == "A.27"),
    (df_VariantReqMatch0['lineage'] == "B.1.618"),
    (df_VariantReqMatch0['VariantYesNo'].eq('Possible')),
    (df_VariantReqMatch0['VariantYesNo'].eq('Warning')),
    (df_VariantReqMatch0['VariantYesNo'].eq('No'))
]

# ***Add to these as well if you add to the above list. Order is important, you must add your new entry to the correct spot, e.g for the 5th row in conditions above (B.1.427), it's choice must be 5th below - 'California VUI (B.1.427)') (you can have it say whatever you want, just surround it in single quotes and put a comma after)
choices2 = ['Failed WGS QC','Failed WGS QC','UK (B.1.1.7)','SA (B.1.351)','Brazil (P.1)','India (B.1.617)','India (B.1.617.1)','India (B.1.617.2)','India (B.1.617.3)','Nigerian VOI (B.1.525)','California VOI (B.1.427)','California VOI (B.1.429)','New York VOI (B.1.526)','B.1.526.1 (VOI)','P.1.1 (VOI)','P.2 (VOI)','P.3','B.1.1.318 (VOI)','A.23.1 (VOI)','A.27 (VOI)','B.1.618 (Other - triple mutant)',('Possible ' + df_VariantReqMatch0['watchlist_id']),('Possible Pangolin error, new VOI, or Contamination with ' + df_VariantReqMatch0['lineage'] + ' and ' + df_VariantReqMatch0['watchlist_id']),'Not a VoC']

df_VariantReqMatch0['VariantType'] = np.select(conditions2, choices2, default='Not a VoC')
#print(df_VariantReqMatch0)  #correct




#-------------------------SAVE Output-------------------------

# Drop extra index row:
df_VariantReqMatch0.set_index('UselessNumber', inplace=True)

# Save file:
df_VariantReqMatch0.to_excel('S:/Path/To/Save/OutputFile/Runs_CombinedQCsummary_PlusNewestLineages' + '_' + Today + '.xlsx')

# People can now grab this file (for reporting, etc) to get the most updated lineage data (and VoC/VUI calls will be redone based on these), on ALL data, even for older samples. 
# File is dated so people know what day it's for, and for tracking changes in data.
# You can link this file to a dashboard to create data summaries (link to the folder it's in, to grab the newest file each time).
