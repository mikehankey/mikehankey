# This version is using the Flourish app to generate the animation
import csv
import os, sys
import numpy as np
import datetime

from utils import *


def clean_date_format(tmp_date):
   # Transform date format
 
   _date =  tmp_date[0:4]+'-'+tmp_date[4:6]+'-'+tmp_date[6:8]
   d_day = _date.split('-') 
   d = datetime.date(int(d_day[0]),int(d_day[1]),int(d_day[2]))
   return d.strftime("%m-%d-%Y")


def prepare_data(_type,_7avg,per_pop):

   # per_pop = we need the population of each state
   if(per_pop==True):
      with open(US_POPULATION, newline='') as csvPopfile:
         pop_rows = csv.reader(csvPopfile)
         popDict = {rows[0]:rows[1] for rows in pop_rows}
   
   # Get the data from daily.csv
   with open(TMP_DATA_PATH + os.sep + 'daily.csv', newline='') as csvfile:
      rows = csv.reader(csvfile)
      r_counter = 0

      new_rows_to_build = []
      all_dates =[]
      all_states =[]

      for row in rows: 

         # We remove all the rows that aren't 'type' 
         if(r_counter == 0):
            index_of_date     = row.index('date')
            index_of_type     = row.index(_type) 
            index_of_state    = row.index('state') 
 
         else: 

            if(row[index_of_type]==''):
               row[index_of_type] = 0

            new_rows_to_build.append({
               'state':  row[index_of_state],
               'date':   clean_date_format(row[index_of_date]),
               'value':  row[index_of_type]
            }) 
            
            all_dates.append(clean_date_format(row[index_of_date]))
            all_states.append(row[index_of_state])

         r_counter+=1

   # We now build a csv parsable with the flourish app

   # First row, "state" + all the dates
   all_dates  = list(set(all_dates))
   all_dates = sorted(all_dates)
  

   all_states = list(set(sorted(all_states))) 
   first_row = ['state'] + all_dates
   all_other_rows = []
   test = False
   
   # Now we need a row my state
   for state in US_STATES:
 
      cur_row = [US_STATES[state]]
      
      #print('Taking care of',US_STATES[state]) 
   
      # For each date
      for date in all_dates:
         test = False

         # Now we add the data for all the dates
         for new_row in new_rows_to_build:
         
            if(new_row['date']==date and new_row['state']==state):
               v = int(new_row['value'])/int(popDict[state])*100000
               cur_row.append(str(round(float(v),2)))
               test = True
            
         if(test is False):
            cur_row.append('0')

      all_other_rows.append(cur_row)


   # For death we need the daily value!
   # We replace all_val_for_state by non_cumulative data
   if(_type=="death"):
      for row in all_other_rows:
         state = row[0]
         all_val_for_state = row[1:]

         first_val = all_val_for_state[0]
         for i,v in enumerate(all_val_for_state):
            if(v!=0):
               v = v - all_val_for_state[i-1]
            else:
               v = v



   max_day = 7


   # We compute the 7-day avg for every row
   for row in all_other_rows:
      tempValForAvg = []
      tempValFormax_day = []

      all_x_avg = []
      all_y_avg = []

      new_vals_for_row = []

      for index, v in enumerate(row):

         if(index!=0):

            # For average of _type
            tempValForAvg.append(float(v))

            if(len(tempValForAvg) <  max_day):
               tempValFormax_day = tempValForAvg 
            else: 
               tempValFormax_day = tempValForAvg[len(tempValForAvg)-max_day:len(tempValForAvg)] 
                  
            # We have strings...
            tempValFormax_day = [float(i) for i in tempValFormax_day]
   
            
            new_vals_for_row.append(np.mean(tempValFormax_day))   

      row = [row[0]] + new_vals_for_row


   print(','.join(first_row))             
   for row in all_other_rows:
      print(','.join(row))  
      #print(str(len(row)))
 
if __name__ == "__main__":  
   # python new_barchart_race.py  > ./tmp_json_data/race_deaths_per_10000.csv
   #prepare_data('death',True,True)
   
   # python new_barchart_race.py  > ./tmp_json_data/race_cases_per_10000.csv
   #prepare_data('positive',True,True)


   #python new_barchart_race.py  > ./tmp_json_data/race_7DAVG_daily_cases_per_10000.csv
   #prepare_data('positiveIncrease',True,True)


   #python new_barchart_race.py  > ./tmp_json_data/race_daily_deaths_per_10000.csv
   prepare_data('death',True,True)