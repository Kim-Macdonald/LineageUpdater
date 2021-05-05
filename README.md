# LineageUpdater

Merge the QC summary (product of mergeQCresults_plusMissing then VoCcaller, saved as excel file) with a csv of updated lineages (when run an updated pangolin on all prior and current samples).

The script will: 

1. Read in the output file(s) of VoCcaller (single file or merged output file (instructions below)) and https://github.com/BCCDC-PHL/pangolin-nf (an updated version of pangolin that's run on all data in the covid sequence directory - output file is called [date]_pangolin_lineages.csv). 

![image](https://user-images.githubusercontent.com/72042148/117079561-dcb65f00-acf0-11eb-826c-2b0b07cdd9f1.png)

(example data only, to show VoCcaller output)

(click on image to view in new window, then click to zoom, and scroll to see entire table)


![image](https://user-images.githubusercontent.com/72042148/117081476-cd391500-acf4-11eb-9f3a-e26a31dc75f1.png)

(example data only, to show pangolin pipeline output)


2. It will </b>merge the 2 output files to update the Runs_CombinedQCsummary.xlsx with the Newest lineages for all samples</b> (lineage, note, pangoLEARN version, pangolin version columns) from the [date]_pangolin_lineages.csv file. 



3. It will <b>re-call VoCs/VUIs based on the new lineages.</b> 

4. It will save an output file with today's date, to a location you specify in the script. 

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

Save the mergeQCresults_plusMissing.py (or _v5.py script) and addVoCcalls_RunNum_v2.py scripts somewhere on your server or unix PC.

Save the LineageUpdater script on your PC. Install Anaconda Navigator. 


## Do Every time:

### Create QC Summary file:

1. Run mergeQCresults_plusMissing.py on the server, as per mergeQCresults_plusMissing.py instructions (https://github.com/Kim-Macdonald/mergeQCresults_plusMissing )

2. Then run VoCcaller script (Both are combined in command below), as per VoCcaller instructions (https://github.com/Kim-Macdonald/VoCcaller ) 

(replace [MiSeqRunID] with your MiSeqRunID/RunName or Directory for the sequencing run of interest):

    cd sequence/analysis/run/directory/[MiSeqRunID]; conda activate pandas; python3 path/to/mergeQCresults_plusMissing.py; python3 path/to/addVoCcalls_RunNum_v2.py; conda deactivate


    OR for artic v1.3 and ncov-tools v1.5:

    cd sequence/analysis/run/directory/[MiSeqRunID]; conda activate pandas; python3 path/to/mergeQCresults_plusMissing_v5.py; python3 path/to/addVoCcalls_RunNum_v2.py; conda deactivate

The output file of interest is ([MiSeqRunID]_MissingPlus_QC_lineage_VoC_OrderedFinal_PlusVoCcalls.csv ).


### Merge Output for multiple runs:

You may need to merge the output for multiple runs, to keep a file for all runs to-date:


1. Navigate to the analysis directory (1 level above your run directories - e.g. if your runs are in /Path/to/analysis/[MiSeqRunID] then cd to /Path/to/analysis/ )

(replace "Runs1-145" in the output file with whatever makes sense for your runs)

    cat ./*/*_MissingPlus_QC_lineage_VoC_OrderedFinal_PlusVoCcalls.csv > Runs1-145_combined_QC_lineage_VoC_OrderedFinal_PlusVoCcalls.csv

2. Remove the header rows from all the files except the first: (replace both instances of "Runs1-145" below with whatever you used in your output file above)

You May also want to add a date to the beginning or end of the output file in the command below (e.g. Runs_CombinedQCsummary_[date].csv ) 

(if you add a date, you may need to add a * to the LineageUpdater Script that reads in the Runs_CombinedQCsummary output file)

    header=$(head -n 1 Runs1-145_combined_QC_lineage_VoC_OrderedFinal_PlusVoCcalls.csv); (printf "%s\n" "$header"; grep -vFxe "$header" Runs1-145_combined_QC_lineage_VoC_OrderedFinal_PlusVoCcalls.csv) > Runs_CombinedQCsummary.csv

3. <b>Transfer the Runs_CombinedQCsummary.csv output file from the server to your PC (e.g. via Cyberduck, FileZilla, etc).</b>

4. Open the Runs_CombinedQCsummary.csv file and Save As .xlsx (or change the input file extension to .csv in the LineageUpdater script, and use read_csv instead of read_excel).


### Transfer the Updated Lineages file (From pangolin pipeline)
Assuming you've run this pipeline: https://github.com/BCCDC-PHL/pangolin-nf (or the newest pangolin version on all data)

And produced an output file that looks like: [date]_pangolin_lineages.csv

1. Transfer the file (saved in pangolin-nf-v0.0-output directory, within the [MiSeqRunID] directory).


### Run LineageUpdater Script (on PC):

1. Update paths to files (Runs_CombinedQCsummary.xlsx and [date]_pangolin_lineages.csv and where you want your <b>output file</b> saved), in the script, as per your set-up.

2. Launch Spyder, or other IDE on your PC. 

3. Open and run script in Spyder on your PC.

4. The file should appear in the folder you specified for saving (at end of LineageUpdater script).

5. Use this file to report the newest lineages, summarize updated VoC/VUI data, trends, etc. 

(e.g. link output file (or the folder it's in, to take the newest one each refresh) to a dashboard, to summarize data for reports, etc.





