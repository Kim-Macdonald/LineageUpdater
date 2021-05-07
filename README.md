# LineageUpdater

Merge the QC summary (product of mergeQCresults_plusMissing then VoCcaller, saved as excel file) with a csv of updated lineages (when run an updated pangolin on all prior and current samples).

The script will: 

1. <b>Read</b> in the output file(s) of VoCcaller (single file or merged output file (instructions below)) and https://github.com/BCCDC-PHL/pangolin-nf (an updated version of pangolin that's run on all data in the covid sequence directory - output file is called [date]_pangolin_lineages.csv). 

![image](https://user-images.githubusercontent.com/72042148/117079561-dcb65f00-acf0-11eb-826c-2b0b07cdd9f1.png)

(example data only, to show VoCcaller output)

(click on image to view in new window, then click to zoom, and scroll to see entire table)


![image](https://user-images.githubusercontent.com/72042148/117406288-b8f64300-aec1-11eb-9446-003e1eb6cce5.png)

(example data only, to show pangolin pipeline output)


2. <b>Split the FastqID</b> in sample (QCsummary) and sample_id (lineages file) columns in each file. (Assuming your fastqs are named like: A1234567890-201-D-E03 (split by dashes))

3. Create a <b>new column</b> in each table (QCsummary and lineages) called <b>SampleID_RunID</b>. (the sample and run_name columns concatenated to create a unique sample ID. This will allow repeats of the same sampleID/CID to be processed individually)

4. <b>Sort and remove duplicates</b> (based on SampleID_RunID column in each) - keep last/latest duplicate (if you're repeating a sample, it's likely b/c the first failed).
 
 
3. <b>Merge</b> the 2 output files to update the Runs_CombinedQCsummary.xlsx with the <b>Newest lineages</b> and other relevant columns for all samples (lineage, note, pangoLEARN version, pangolin version columns) from the [date]_pangolin_lineages.csv file. 



4. <b>Re-call VoCs/VUIs based on the new lineages.</b> 

5. <b>Save</b> an output file with today's date, to a location you specify in the script. 

![image](https://user-images.githubusercontent.com/72042148/117085402-7d5f4b80-acfe-11eb-99f1-98ce120d9ae9.png)

(example data only, to show LineageUpdater output)


Headers highlighted in <b>yellow</b>, are the columns replaced with those from the updated pangolin_lineages.csv file.

Headers highlighted in <b>blue</b>, are the columns added by the LineageUpdater script.

<b>Unhighlighted</b> headers are the original columns from the Runs_CombinedQCsummary.xlsx file. 



# Assumptions:

Same as described here:

https://github.com/Kim-Macdonald/VoCcaller#assumptions


Also assuming your run this pangolin pipeline separately, on all sequence data (to update lineages for all samples at same time):

https://github.com/BCCDC-PHL/pangolin-nf

(it updates itself to the newest pangolin version first, then runs on all [MiSeqRunID] directories in the analysis directory (e.g. sequence/analysis/run/directory/[MiSeqRunID] )


# Usage:

## Do once: 

Save the mergeQCresults_plusMissing.py (or _v5b.py script) and addVoCcalls_RunNum_v2.py scripts somewhere on your server or unix PC.

Save the LineageUpdater script on your PC. Install Anaconda Navigator. 


## Do Every time:

### Create QC Summary file:

1. Run mergeQCresults_plusMissing.py on the server, as per mergeQCresults_plusMissing.py instructions (https://github.com/Kim-Macdonald/mergeQCresults_plusMissing ). (Command is below)

2. Then run VoCcaller script (Command is combined with Step 1's command, in commands shown below), as per VoCcaller instructions (https://github.com/Kim-Macdonald/VoCcaller ) 

 (replace [MiSeqRunID] with your MiSeqRunID/RunName or Directory for the sequencing run of interest):

    cd sequence/analysis/run/directory/[MiSeqRunID]; conda activate pandas; python3 path/to/mergeQCresults_plusMissing.py; python3 path/to/addVoCcalls_RunNum_v2.py; conda deactivate


    OR for artic v1.3 and ncov-tools v1.5:

    cd sequence/analysis/run/directory/[MiSeqRunID]; conda activate pandas; python3 path/to/mergeQCresults_plusMissing_v5.py; python3 path/to/addVoCcalls_RunNum_v2.py; conda deactivate

The output file of interest is ([MiSeqRunID]_MissingPlus_QC_lineage_VoC_OrderedFinal_PlusVoCcalls.csv ).


### Merge Output for multiple runs:

You may want to merge the output for multiple runs, to keep a file for all runs to-date (I recommend doing this):


1. <b>Navigate to the analysis directory</b> (1 level above your run directories - e.g. if your runs are in /Path/to/analysis/[MiSeqRunID] then cd to /Path/to/analysis/ )

2. <b>Merge the files for each run into 1</b> (replace "Runs1-145" in the output file with whatever makes sense for your runs)
  
       cat ./*/*_MissingPlus_QC_lineage_VoC_OrderedFinal_PlusVoCcalls.csv > Runs1-145_combined_QC_lineage_VoC_OrderedFinal_PlusVoCcalls.csv

3. <b>Remove the header rows</b> from all the files except the first: (replace both instances of "Runs1-145" below with whatever you used in your output file above)

       header=$(head -n 1 Runs1-145_combined_QC_lineage_VoC_OrderedFinal_PlusVoCcalls.csv); (printf "%s\n" "$header"; grep -vFxe "$header" Runs1-145_combined_QC_lineage_VoC_OrderedFinal_PlusVoCcalls.csv) > Runs_CombinedQCsummary.csv
    
  You May also want to add a date to the beginning or end of the output file in the command above (e.g. Runs_CombinedQCsummary_[date].csv) 

  (if you add a date, you'll need to add a * to the LineageUpdater Script that reads in the Runs_CombinedQCsummary output file) (replace the line of code on line 28 with all these lines:) 

    ~~~python

    path1 = "C:/Path/to/QCsummaryFile/Runs_CombinedQCsummary*.xlsx"
    
    for filename in glob.glob(path1):
        with open(filename, 'r') as f:
            print(f)
            df_QCsummary0 = pd.read_excel(f, sheet_name=0)
    ~~~


4. <b>Transfer the Runs_CombinedQCsummary.csv output file to your PC</b> from the server (e.g. via Cyberduck, FileZilla, etc).

5. Open the Runs_CombinedQCsummary.csv file and <b>Save As .xlsx</b> (or change the input file extension to .csv in the LineageUpdater script, and use read_csv instead of read_excel).


### Transfer the Updated Lineages file (From pangolin pipeline)
Assuming you've run this pipeline: https://github.com/BCCDC-PHL/pangolin-nf (or the newest pangolin version on all data)

And produced an output file that looks like: [date]_pangolin_lineages.csv

1. <b>Transfer the file</b> (saved in pangolin-nf-v0.1-output directory, within the [MiSeqRunID] directory) to your PC from the server (e.g. via Cyberduck, FileZilla, etc).


### Run LineageUpdater Script (on PC):

1. <b>Update paths</b> to files (Runs_CombinedQCsummary.xlsx and [date]_pangolin_lineages.csv and where you want your <b>output file</b> saved), in the script, as per your set-up. (lines 28, 87, 259)

2. <b>Launch Spyder</b>, or other IDE on your PC. 

3. Open and <b>run script</b> in Spyder on your PC.

4. The file should appear in the folder you specified for saving (at end of LineageUpdater script).

5. Use this file to report the newest lineages, summarize updated VoC/VUI data, trends, etc. 

  (e.g. link output file (or the folder it's in, to take the newest one each refresh) to a dashboard, to summarize data for reports, etc.





