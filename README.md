# Project FROG Monitoring #

![alt text](http://projectfrog.com/assets/img/pf_logo.png "Logo")

-----------------

## How To Update Dashboard ##
http://frog.4dapt.com/

Update PosgreSQL Database:

* Follow Instructions on Either the "FROG Data Retrieval Script.ipynb" or the "FROG Update Script.py" file
* To run the .py file you need to open the file and change the month that was recently completed at the bottom of page then save and close the script. Navigate to file on local machine using the terminal, in the correct directory type in "python 'FROG Update Script.py'" (https://www.youtube.com/watch?v=Txt-cLLa_vo)
* To run the jupyter notebook (http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/execute.html) Then follow instruction on page

Update Tableau Dashboard:

* Open Tableau File found at (/Volumes/data1/820 HNEI - FROG Monitoring Extension P3/03-Working/Dashboard/FROG Dashboard.twb)
* Enter Credentials to connect to PostgreSQL Database (Username: rh1, Password: Anal1st-R0undH0use)
* Navigate to the "FROG Monitoring" Tab and select "Data/frog_data+(rh1)/Refresh" in the header
* Navigate to  the "Weather Monitoring" Tab and select "Data/frog_weather (rh1)/Refresh" in the header
* Navigiate to the "FROG" Tab and select "Server/Publish Workbook" in the header
* Enter Tableau Online Creditials (Username: office@roundhouseone.com, Password: 1500PeetsPhilz)
* Select Project: FROG Monitoring Dashboard
* Select Name: FROG Story
* Select Sheets: Just Select 'FROG'
* Press Publish and choose to overwrite existing
* Data should now be updated @ http://frog.4dapt.com/

## Update Monthly Report ##

Find Template at: "data1/820 HNEI - FROG Monitoring Extension P3/03-Working/FROG Classroom Monitoring Del 4 Template/Classroom Monitoring Del 4 Monthly Template2.indd"

Update Summary to Date

* Available Dataset = the total number of columns found in dataset (Note: Kawaikini West, do not count Air Speed and Air Temperature)
* Total Data Collected to Date (cumulative) = Navigigate to Cleaned Data and open file for the specified room and month and count datapoints + month prior (/Volumes/data1/820 HNEI - FROG Monitoring Extension P3/03-Working/Postgres Database Files/FROG Data/Cleaned Data)
* Highlight all rows of all columns except data/time and source to get count of all data point

Update Montly Summary

* Total Data Expected in Month = ((Datapoints per hour) * 24) * (Days in Month) * (Columns in Dataset)
* Total Data Collected in month = Navigigate to Cleaned Data and open file for the specified room and month and count datapoints (Highlight all rows of all columns except data/time and source to get count of all data point)
* Data with Errors in Month = Navigate to data summary and count the number of too high, too low and missing data points (/Volumes/data1/820 HNEI - FROG Monitoring Extension P3/03-Working/Postgres Database Files/FROG Data/Data Summary)

Update Error Summary

* Call out Errors that pass a certian threshold specified by Mayssen

-----------------

## Phase 1 ##

Task 1: Configuration and Implementation

* No RH1 Hours Allocated

Task 2: System Functionality Testing

* No RH1 Hours Allocated

Task 3: Analysis and Visualization Support (4 Hours)

* Provide analysis, visual & export tools and training (up to 4 hrs) to use the 4daptive platform

## Phase 2 ##

Licensing:

* No RH1 Hours Allocated

Data Collection & Hardware Support: (1 Hour)

* Retrieve data from Database Processing Server at the end of each month. There are two CSV files per site

* Need clarification as to what the “hardware support” entails -> This should be more for L+U so not RH1

Transform: (2 Hours)

* Transform data to remove errors

⋅⋅1. Correction of Timestamps (from UTC to location specific)

⋅⋅2. Ensure dataset units are clear (e.g. deg F, deg C, kW, kWh)

⋅⋅3. Address data gaps

⋅⋅4. Select importing of the relevant columns of data

⋅⋅5. Monitor sensor status from data files. Communicate to MKThink with any issues and report findings in the Monthly Summary Report

Storage:

* No RH1 Hours Allocated

* Store data in secure cloud-based redundant system

Analysis & Visualization Support: (4 Hours)

* See monthly summary report draft template. Note, the monthly summary template has not been finalized but is expected by August 31. RH1 would be responsible for filling in the following information into the InDesign Monthly Activity Report Template (pg 7-9).

⋅⋅1. Quantity of data collected by site to date and from project start (August 1, 2017)

* Data Error Summary

⋅⋅1. Categorize each sensor error by the 4 qualitative error types outlined in the FROG Classroom Monitoring Deliverable 2 (i.e. “missing, bad, too high, and too low”).

⋅⋅2. Describe the frequency and duration of each sensor error

⋅⋅3. Create graph(s) of significant errors to show frequency and duration to be included in report (as needed)

⋅⋅4. Provide Training and assistance in understanding the 4Daptie platform’s analysis and visualization capabilities (on an as needed basis)