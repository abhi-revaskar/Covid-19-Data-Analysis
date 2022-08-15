For each question that requires coding, the code is written in Python 3 and the files have extension ".py".
Following packages have been used for the Python code,
numpy, pandas, matplotlib,datetime,dateutil
The time-period of analysis is taken from 15th March 2020 to 14th August 2021 for each question.
For the questions involving analysis for state and overall, the "districtid" field mentioned in the question is replaced by "stateid" for state data and "id" for overall data.
The solution for each question is explained in following points.

(1) The modified JSON file is named as "neighbor-districts-modified.json" which contains the modified information of districts.

(2)The code file for this question is named as "Q2.py" which can be invoked from "edge-generator.sh" and output file is named as "edge-graph.csv". The output file contains all the districts along with their neighboring districts.

(3)The code file for this question is named as "Q3.py" which can be invoked from "case-generator.sh" and output files are named as,
"cases-week.csv" for week-wise cases in each district,
"cases-month.csv" for month-wise cases in each district,
"cases-overall.csv" for overall cases in each district.
"timeid" field is taken as "overall" in "cases-overall.csv" file.
The cases before the date on which the recording of cases was started are taken as zero.
Total no. of cases per week are taken as difference between no. of cases at the end of the week and at the start of the week. Similar calculations are done for no. of cases per month.

(4)The code file for this question is named as "Q4.py" which can be invoked from "peaks-generator.sh" and output files are named as,
"district-peaks.csv" for district peaks,
"state-peaks.csv" for state peaks,
"overall-peaks.csv" for overall peaks.
A peak is considered as the week or month having highest total number of cases arised in that particular week or month.
The wave 1 calculated as the week or month with highest number of cases between 15th March 2020 and 31th December 2020 and 2nd wave is calculated between 1st January 2021 and 14th August 2021.

(5)The code file for this question is named as "Q5.py" which can be invoked from "vaccinated-count-generator.sh" and output files are named as,
"district-vaccinated-count-week.csv" for week-wise count of vaccination for each district,
"district-vaccinated-count-month.csv" for month-wise count of vaccination for each district,
"district-vaccinated-count-overall.csv" for overall count of vaccination for each district,
"state-vaccinated-count-week.csv" for week-wise count of vaccination for each state,
"state-vaccinated-count-month.csv" for month-wise count of vaccination for each state,
"state-vaccinated-count-overall.csv" for overall count of vaccination for each state.

(6)The code file for this question is named as "Q6.py" which can be invoked from "vaccination-population-ratio-generator.sh" and output files are named as,
"vaccination-population-ratio-district.csv" for the ratio of each district,
"vaccination-population-ratio-state.csv" for the ratio of each state,
"vaccination-population-ratio-overall.csv" for the overall ratio.
The districts from census data which didn't match their names with any district from the modified JSON file are dropped from analysis as mentioned in the question and hence the number of districts analysed for this question are less than the usual district count.

(7)The code file for this question is named as "Q7.py" which can be invoked from "vaccine-type-ratio-generator.sh" and output files are named as,
"vaccine-type-ratio-district.csv" for district data,
"vaccine-type-ratio-state.csv" for state data,
"vaccine-type-ratio-overall.csv" for overall data.
For the districts and states in which the number of people vaccinated with Covaxin are zero, the ratio is marked as "NA" in "vaccineratio" field.

(8)The code file for this question is named as "Q8.py" which can be invoked from "vaccinated-ratio-generator.sh" and output files are named as,
"vaccinated-dose-ratio-district.csv" for districts,
"vaccinated-dose-ratio-state.csv" for states,
"vaccinated-dose-ratio-overall.csv" for overall.

(9)The code file for this question is named as "Q9.py" which can be invoked from "complete-vaccination-generator.sh" and output file is named as "complete-vaccination.csv".
The rate of vaccination for each state is taken as it was from 8th August 2021 to 14th August 2021 i.e. the last week of analysis period.
