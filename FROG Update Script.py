# Set of libraries and settings necessary to run the remainder of the document

import os
import datetime
from datetime import date, timedelta
from itertools import accumulate
import numpy as np
import pandas as pd

# The following function has been translated from the following document 
# (smb://10.50.10.25/data1/820 HNEI - Energy Monitoring P1/2/2 - HNEI Part 2- Comparable Sites/06-Presentations/01-Working/Ilima/Q7/HNEI_Ilima_PV.xlsx)

def panelFeedFunction(test):
    n = 0
    energy = []
    kw = []

    try:
        for n in range(len(test)):
            if n == 0:
                energy.append(0)
                kw.append(0)
                n += 1
            else:
                PV1_Power = ((test.ix[n]["PV_Inverter_1_neg_kWh"] - test.ix[n - 1]["PV_Inverter_1_neg_kWh"]) - (test.ix[n]["PV_Inverter_1_pos_kWh"] - test.ix[n - 1]["PV_Inverter_1_pos_kWh"])) * 6 * 2
                PV2_Power = ((test.ix[n]["PV_Inverter_2_neg_kWh"] - test.ix[n - 1]["PV_Inverter_2_neg_kWh"]) - (test.ix[n]["PV_Inverter_2_pos_kWh"] - test.ix[n - 1]["PV_Inverter_2_pos_kWh"])) * 6 * 2
                
                Panel_Power = (((test.ix[n]["Panel_Feed_pos_kWh"] - test.ix[n - 1]["Panel_Feed_pos_kWh"]) - (test.ix[n]["Panel_Feed_neg_kWh"] - test.ix[n - 1]["Panel_Feed_neg_kWh"])) * 6) + PV1_Power + PV2_Power

                Panel_Energy = Panel_Power / 6
                energy.append(Panel_Energy)

                kw.append(Panel_Power)
                n += 1

        energy = list(accumulate(energy))

        test["Panel_Feed_kW"] = kw
        test["Panel_Feed_kWh"] = energy


    except:
        for n in range(len(test)):
            if n == 0:
                energy.append(0)
                kw.append(0)
                n += 1
            else:
                PV1_Power = ((test.ix[n]["PV_Inverter_central_neg_kWh"] - test.ix[n - 1]["PV_Inverter_central_neg_kWh"]) - (test.ix[n]["PV_Inverter_central_pos_kWh"] - test.ix[n - 1]["PV_Inverter_central_pos_kWh"])) * 6 * 2
                PV2_Power = ((test.ix[n]["PV_Inverter_micro_neg_kWh"] - test.ix[n - 1]["PV_Inverter_micro_neg_kWh"]) - (test.ix[n]["PV_Inverter_micro_pos_kWh"] - test.ix[n - 1]["PV_Inverter_micro_pos_kWh"])) * 6 * 2

                Panel_Power = (((test.ix[n]["Panel_Feed_pos_kWh"] - test.ix[n - 1]["Panel_Feed_pos_kWh"]) - (test.ix[n]["Panel_Feed_neg_kWh"] - test.ix[n - 1]["Panel_Feed_neg_kWh"])) * 6) + PV1_Power + PV2_Power

                Panel_Energy = Panel_Power / 6
                energy.append(Panel_Energy)
                
                kw.append(Panel_Power)
                n += 1

        energy = list(accumulate(energy))
        energy = energy[:-1]
        
        kw = kw[:-1]
        
        test["Panel_Feed_kW"] = kw
        test["Panel_Feed_kWh"] = energy

# Function used to pull frog sensor data from L+U server Data is then saved to Data1 Server at the following location
# smb://10.50.10.25/data1/820 HNEI - FROG Monitoring Extension P3/03-Working/Postgres Database Files/FROG Data

def frogFetch(source = "3", month = "6", year = "2017"):
    url = "https://coolretrievebeta.herokuapp.com/csv_data_m/" + str(source) + "/" + str(year) + "/" + str(month) + "/"
    df = pd.read_csv(url)
    
    ######### Save Raw File #########
    
    sourceList = {
        "3": "Kawaikini West Classroom",
        "4": "Kawaikini East Classroom",
        "5": "Kawaikini Weather Station",
        "11": "Ilima Classroom",
        "15": "Ewa Weather Station"
    }
    
    os.chdir("/Volumes/data1/820 HNEI - FROG Monitoring Extension P3/03-Working/Postgres Database Files/FROG Data/Raw Data")
    
    rawName = str(sourceList[source]) + "_Raw_" + str(month) + "_" + str(year)
    
    df.to_csv(str(rawName) + ".csv")
    
    ######### Data Formatting #########
    
    df.replace("missing", value = np.nan, inplace = True)
    
    panelFeedFunction(df)
    
    
    df["UTC time"] = df["UTC time"].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
    df["UTC time"] = df["UTC time"].apply(lambda x: x.replace(second = 0))
    df.set_index("UTC time", inplace = True)
    
    try:
         df = df.rename(columns = {"Exhaust_Fans_kW":"Exhaust_Fan_kW", 
                                   "Exhaust_Fans_kWh" : "Exhaust_Fan_kWh"})
    except:
        pass
    
    df.replace("missing", np.nan, inplace = True)
    
    def floater(x):
        try:
            return np.float(x)
        except:
            return np.nan
        
    for col in df.columns.tolist():
        df[col] = df[col].apply(floater)

        
    list5 = ["Ceiling_Fans_kW", "Exhaust_Fan_kW", "Fan_Coil_Unit_kW", "Lighting_Main_Space_kW", "Lighting_Wall_and_Exterior_kW", 
             "Louver_Actuator_kW", "PV_Inverter_central_neg_kW", "PV_Inverter_central_pos_kW", "PV_Inverter_micro_neg_kW",
             "PV_Inverter_micro_pos_kW", "PV_Inverter_1_neg_kW", "PV_Inverter_1_pos_kW", "PV_Inverter_2_neg_kW", 
             "PV_Inverter_2_pos_kW", "Lighting_Exterior_kW"]
    
    list20 = ["Condensing_Unit_kW", "Room_Air_Speed"]
    
    list50 = ["AIR_1_E", "AIR_2_W", "AIR_3_E", "AIR_4_W", "FSF_1_SE", "FSF_2_Center", "FSF_3_NW", "FSF_4_SE", 
              "FSF_5_Center", "FSF_6_NW", "PLE_1_SE", "PLE_2_Center", "PLE_3_NW", "PLE_4_SE", "PLE_5_Center", "PLE_6_NW",
              "Panel_Feed_kW", "Panel_Feed_neg_kW", "Panel_Feed_pos_kW", "Room_Air_Temperature_C", "Supply_Air_Temperature_C", 
              "WAL_1_E", "WAL_2_W", "WAL_3_E", "WAL_4_W", "E wall air temperature", "E wall surface temperature", 
              "SE plenum air temperature", "W wall air temperature", "Center floor surface temperature", 
              "Center plenum air temperature", "NW floor surface temperature", "NW plenum air temperature", 
              "SE floor surface temperature", "W wall surface temperature"]
    
    list100 = ["Room_Air_Humidity", "Suppy_Air_Humidity"]
    
    list350 = ["Room_Illuminance_Ceiling", "Room_Illuminance_WestWall"]
    
    list429 = ["Ceiling_Fans_kWh", "Condensing_Unit_kWh", "Exhaust_Fan_kWh", "Fan_Coil_Unit_kWh", "Lighting_Main_Space_kWh",
               "Lighting_Wall_and_Exterior_kWh", "Louver_Actuator_kWh", "PV_Inverter_central_neg_kWh", 
               "PV_Inverter_central_pos_kWh", "PV_Inverter_micro_neg_kWh", "PV_Inverter_micro_pos_kWh", 
               "Panel_Feed_kWh", "Panel_Feed_neg_kWh", "Panel_Feed_pos_kWh", "PV_Inverter_1_neg_kWh", 
               "PV_Inverter_1_pos_kWh", "PV_Inverter_2_neg_kWh", "PV_Inverter_2_pos_kWh", "Lighting_Exterior_kWh"]
    
    co2 = ["Room_Air_CO2"]
    
    ######### FROG Data Quality Summary #########
    
    rangeDict = {
        0: [0, 5], #List5
        1: [0, 20], #List20
        2: [0, 50], #List50
        3: [0, 100], #List100
        4: [0, 350], #List350
        5: [0, 4294967.296], #List429
        6: [250, 2000] #Listco2
    }
        
    holder = pd.DataFrame(columns = df.columns.tolist(), index = ["High", "Low", "Missing", "Good"])
    
    n = 0
    for group in [list5, list20, list50, list100, list350, list429, co2]:
        for col in group:
            if col in df.columns.tolist():
                good = 0
                low = 0
                high = 0
                missing = 0
                for x in df[col]:
                    if x >= rangeDict[n][0] and x <= rangeDict[n][1]:
                        good += 1
                    elif x < rangeDict[n][0]:
                        low += 1
                    elif x > rangeDict[n][1]:
                        high += 1
                    elif pd.isnull(x) == True:
                        missing += 1

                holder.set_value("Good", col, good)
                holder.set_value("Low", col, low)
                holder.set_value("High", col, high)
                holder.set_value("Missing", col, missing)
            else:
                pass
            
        n+=1
            
        
    ######### Saving FROG Data Quality Summary #########
    
    os.chdir("/Volumes/data1/820 HNEI - FROG Monitoring Extension P3/03-Working/Postgres Database Files/FROG Data/Data Summary")
    
    holderName = str(sourceList[source]) + "_Summary_" + str(month) + "_" + str(year)
            
    holder.to_csv(str(holderName) + ".csv")

     ######### FROG Data Transformation #########
    
    n = 0
    for group in [list5, list20, list50, list100, list350, list429, co2]:
        for col in group:
            if col in df.columns.tolist():
                df[col] = df[col].apply(lambda x: x if x >= rangeDict[n][0] and x <= rangeDict[n][1] else np.nan)
            else:
                pass
        n+=1
    
    df.fillna(method = "ffill", inplace = True)
    
    for col in df.columns.tolist():
        df[col] = df[col].fillna(df[col].mean())
    
    df["Source"] = source
    
    
    ######### Saving Transformed FROG Data #########

    os.chdir("/Volumes/data1/820 HNEI - FROG Monitoring Extension P3/03-Working/Postgres Database Files/FROG Data/Cleaned Data")
    
    dfName = str(sourceList[source]) + "_" + str(month) + "_" + str(year)
    
    df.reset_index().to_csv(str(dfName) + ".csv", index = False)


# Function used to pull weather data from L+U server Data is then saved to Data1 Server at the following location

def weatherFetch(source = "5", month = "6", year = "2017"):
    url = "https://coolretrievebeta.herokuapp.com/csv_data_m/" + str(source) + "/" + str(year) + "/" + str(month) + "/"
    df = pd.read_csv(url)
    
    ######### Save Raw File #########
    
    sourceList = {
         "3": "Kawaikini West Classroom",
         "4": "Kawaikini East Classroom",
         "5": "Kawaikini Weather Station",
         "11": "Ilima Classroom",
         "15": "Ewa Weather Station"
    }
    
    os.chdir("/Volumes/data1/820 HNEI - FROG Monitoring Extension P3/03-Working/Postgres Database Files/Weather Data/Raw Data")
    
    rawName = str(sourceList[source]) + "_Raw_" + str(month) + "_" + str(year)
    
    df.to_csv(str(rawName) + ".csv")
    
    ######### Data Formatting #########
    
    df["UTC time"] = df["UTC time"].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
    df["UTC time"] = df["UTC time"].apply(lambda x: x.replace(second = 0))
    df.set_index("UTC time", inplace = True)
    
    ######### Weather Data Quality Summary #########
    
    rangeDict = {
        "Batt" : [0, 5],
        "DewPt" : [0, 50],
        "Gust Speed": [0, 50],
        "Pressure": [850, 1100],
        "RH": [0, 100],
        "Rain": [0, 190],
        "Solar Rad": [0, 1500],
        "Solar Rad1": [0, 1500],
        "Temp": [0, 50],
        "Wind Dir": [0, 360],
        "Wind Speed": [0, 50]
    }
    
    holder = pd.DataFrame(columns = df.columns.tolist(), index = ["High", "Low", "Missing", "Good"])
    
    for col in holder.columns.tolist():
        good = 0
        low = 0
        high = 0
        missing = 0
        for x in df[col]:
            if x >= rangeDict[col][0] and x <= rangeDict[col][1]:
                good += 1
            elif x < rangeDict[col][0]:
                low += 1
            elif x > rangeDict[col][1]:
                high += 1
            elif pd.isnull(x) == True:
                missing += 1
    
        holder.set_value("Good", col, good)
        holder.set_value("Low", col, low)
        holder.set_value("High", col, high)
        holder.set_value("Missing", col, missing)
        
    ######### Saving Weather Data Quality Summary #########
    
    os.chdir("/Volumes/data1/820 HNEI - FROG Monitoring Extension P3/03-Working/Postgres Database Files/Weather Data/Data Summary")
    
    holderName = str(sourceList[source]) + "_Summary_" + str(month) + "_" + str(year)
            
    holder.to_csv(str(holderName) + ".csv")
        
    ######### Weather Data Transformation #########
    
    for col in df.columns.tolist():
        df[col] = df[col].apply(lambda x: x if x >= rangeDict[col][0] and x <= rangeDict[col][1] else np.nan)
    
    df.fillna(method = "ffill", inplace = True)
    
    df["Source"] = source
    
    ######### Saving Transformed Weather Data #########

    os.chdir("/Volumes/data1/820 HNEI - FROG Monitoring Extension P3/03-Working/Postgres Database Files/Weather Data/Cleaned Data")
    
    dfName = str(sourceList[source]) + "_" + str(month) + "_" + str(year)
    
    df.reset_index().to_csv(str(dfName) + ".csv", index = False)


# Function to push collected Frog sensor data into the Postgres Database
def frogDataPush(path = "/Volumes/data1/820 HNEI - FROG Monitoring Extension P3/03-Working/Postgres Database Files/FROG Data/Cleaned Data"):
    
    import psycopg2
    connect = "user='rh1' password='Anal1st-R0undH0use' host='rds-rh1.4dapt.com' dbname='rh1'"
    conn = psycopg2.connect(connect)
    cursor = conn.cursor()
    
    os.chdir(path)
    n = 0
    for file in os.listdir():
        if file == '.DS_Store':
            pass
        elif n == 0 :
            holder = pd.read_csv(file)
            n+=1
        else:
            df = pd.read_csv(file)
            common = []
            for col in df.columns.tolist():
                if col in holder.columns.tolist():
                    common.append(col)
                else:
                    pass
            
            holder = holder.merge(df, how = "outer", left_on = common, right_on = common)
    
    holder.sort_values(holder.columns[0], ascending = True)
    
    holder.fillna(-99999, inplace = True)
            
    os.chdir("/Volumes/data1/820 HNEI - FROG Monitoring Extension P3/03-Working/Postgres Database Files/FROG Data/Full Dataset")
    holder.to_csv("FROG Database Table.csv", header = False, index = False)
    
    try:
        cursor.execute("DROP TABLE frog_data;")
    except:
        cursor.execute("rollback;")
          
    cursor.execute("CREATE TABLE IF NOT EXISTS frog_data(Date_Time timestamp, Ceiling_Fans_kW double precision, Ceiling_Fans_kWh double precision, Center_floor_surface_temperature double precision, Center_plenum_air_temperature double precision, Condensing_Unit_kW double precision, Condensing_Unit_kWh double precision, E_wall_air_temperature double precision, E_wall_surface_temperature double precision, Exhaust_Fan_kW double precision, Exhaust_Fan_kWh double precision, Fan_Coil_Unit_kW double precision, Fan_Coil_Unit_kWh double precision, Lighting_Exterior_kW double precision,Lighting_Exterior_kWh double precision, Lighting_Main_Space_kW double precision, Lighting_Main_Space_kWh double precision, NW_floor_surface_temperature double precision, NW_plenum_air_temperature double precision, PV_Inverter_1_neg_kW double precision, PV_Inverter_1_neg_kWh double precision, PV_Inverter_1_pos_kW double precision, PV_Inverter_1_pos_kWh double precision, PV_Inverter_2_neg_kW double precision, PV_Inverter_2_neg_kWh double precision, PV_Inverter_2_pos_kW double precision, PV_Inverter_2_pos_kWh double precision, Panel_Feed_kW double precision, Panel_Feed_kWh double precision, Panel_Feed_neg_kW double precision, Panel_Feed_neg_kWh double precision, Panel_Feed_pos_kW double precision, Panel_Feed_pos_kWh double precision, Room_Air_CO2 double precision, Room_Air_Humidity double precision, Room_Air_Speed double precision, Room_Illuminance_Ceiling double precision, Room_Illuminance_WestWall double precision, SE_floor_surface_temperature double precision, SE_plenum_air_temperature double precision, Supply_Air_Temperature_C double precision, Suppy_Air_Humidity double precision, W_wall_air_temperature double precision, W_wall_surface_temperature double precision, Source int, AIR_3_E double precision, AIR_4_W double precision, FSF_4_SE double precision, FSF_5_Center double precision, FSF_6_NW double precision, Lighting_Wall_and_Exterior_kW double precision, Lighting_Wall_and_Exterior_kWh double precision, Louver_Actuator_kW double precision, Louver_Actuator_kWh double precision, PLE_4_SE double precision, PLE_5_Center double precision, PLE_6_NW double precision, Room_Air_Temperature_C double precision, WAL_3_E double precision, WAL_4_W double precision, AIR_1_E double precision, AIR_2_W double precision, FSF_1_SE double precision, FSF_2_Center double precision, FSF_3_NW double precision, PLE_1_SE double precision, PLE_2_Center double precision, PLE_3_NW double precision, PV_Inverter_central_neg_kW double precision, PV_Inverter_central_neg_kWh double precision, PV_Inverter_central_pos_kW double precision, PV_Inverter_central_pos_kWh double precision, PV_Inverter_micro_neg_kW double precision, PV_Inverter_micro_neg_kWh double precision, PV_Inverter_micro_pos_kW double precision, PV_Inverter_micro_pos_kWh double precision, WAL_1_E double precision, WAL_2_W double precision)")
    conn.commit()
    
    table = open("FROG Database Table.csv", "r")

    cursor.copy_from(table, "frog_data", sep = ",")
    conn.commit()


# Function to push collected weather data into the Postgres Database
def frogWeatherPush(path = "/Volumes/data1/820 HNEI - FROG Monitoring Extension P3/03-Working/Postgres Database Files/Weather Data/Cleaned Data"):
    
    import psycopg2
    connect = "user='rh1' password='Anal1st-R0undH0use' host='rds-rh1.4dapt.com' dbname='rh1'"
    conn = psycopg2.connect(connect)
    cursor = conn.cursor()
    
    os.chdir(path)
    n = 0
    for file in os.listdir():
        if file == '.DS_Store':
            pass
        elif n == 0:
            holder = pd.read_csv(file)
            holder.dropna(axis=1,how='all')
            n+=1
        else:
            loopHolder = pd.read_csv(file)
            loopHolder.dropna(axis=1,how='all')
            holder = pd.concat([loopHolder, holder])
            
    holder.sort_values(holder.columns[0], ascending = True)
    
    holder.fillna(-99999, inplace = True)
                
    os.chdir("/Volumes/data1/820 HNEI - FROG Monitoring Extension P3/03-Working/Postgres Database Files/Weather Data/Full Dataset")
    holder.to_csv("FROG Weather Database Table.csv", header = False, index = False)
    
    try:
        cursor.execute("DROP TABLE frog_weather;")
    except:
        cursor.execute("rollback;")
          
    cursor.execute("CREATE TABLE IF NOT EXISTS frog_weather (Date_Time timestamp, Batt double precision, DewPt double precision, Gust_Speed double precision, Pressure double precision, RH double precision, Rain double precision, Solar_Rad double precision, Solar_Rad1 double precision, Temp double precision, Wind_Dir double precision, Wind_Speed double precision, Source int)")
    conn.commit()
    
    table = open("FROG Weather Database Table.csv", "r")

    cursor.copy_from(table, "frog_weather", sep = ",")
    conn.commit()




############################################# Final Function ############################################### Final Function ############################################### Final Function ############################################### Final Function ###############################################




def runUpdate(month = 9):
	for x in ["3", "4", "11"]:
	    frogFetch(source = x, month = month, year = "2017")

	frogDataPush("/Volumes/data1/820 HNEI - FROG Monitoring Extension P3/03-Working/Postgres Database Files/FROG Data/Cleaned Data")


def runUpdateWeather(month = 9):
	for x in ["5", "15"]:
	    weatherFetch(source = x, month = month, year = "2017")
	    
	frogWeatherPush(path = "/Volumes/data1/820 HNEI - FROG Monitoring Extension P3/03-Working/Postgres Database Files/Weather Data/Cleaned Data")

############################################# START HERE ############################################### START HERE ############################################### START HERE ############################################### START HERE ############################################### START HERE
# At the beginning of each month update the month parameter

runUpdate(month = "9")
runUpdateWeather(month = "9")












