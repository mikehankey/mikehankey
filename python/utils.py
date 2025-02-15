import os 
import json
import numpy as np

# FOLDER FOR LOCAL TMP DATA (erased at each update)
TMP_DATA_PATH = "." + os.sep + "tmp_json_data"

# REPO FOR STATIC DATA
STATIC_DATA_PATH = "." + os.sep + "static_json_data"

US_STATES = { 'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'Washington DC', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming', }
US_STATES_INV = { 'Alabama':'AL', 'Alaska':'AK','Arizona':'AZ', 'Arkansas':'AR', 'California':'CA', 'Colorado':'CO', 'Connecticut':'CT', 'Delaware':'DE', 'Florida':'FL', 'Georgia':'GA', 'Hawaii':'HI','Idaho':'ID','Illinois':'IL', 'Indiana':'IN', 'Iowa':'IA','Kansas':'KS','Kentucky':'KY', 'Louisiana':'LA', 'Maine':'ME','Maryland':'MD', 'Massachusetts':'MA', 'Michigan':'MI', 'Minnesota':'MN', 'Mississippi':'MS', 'Missouri':'MO', 'Montana':'MT', 'Nebraska':'NE', 'Nevada':'NV','New Hampshire':'NH', 'New Jersey':'NJ', 'New Mexico':'NM', 'New York':'NY', 'North Carolina':'NC', 'North Dakota':'ND', 'Ohio':'OH','Oklahoma':'OK', 'Oregon':'OR','Pennsylvania':'PA', 'Rhode Island':'RI', 'South Carolina':'SC', 'South Dakota':'SD', 'Tennessee':'TN', 'Texas':'TX','Utah':'UT','Vermont':'VT', 'Virginia':'VA', 'Washington':'WA', 'Washington DC':'DC', 'West Virginia':'WV', 'Wisconsin':'WI', 'Wyoming':'WY'}

PATH_TO_STATES_FOLDER = '..' +  os.sep + 'corona-calc' + os.sep + 'states'
 

GBU_MAIN_TEMPLATE       = '..' + os.sep + 'templates' + os.sep + 'gbu.html'
GBU_MAIN_HOSPI_TEMPLATE = '..' + os.sep + 'templates' + os.sep + 'gbu_hospitalizations.html'
GBU_MAIN_TESTS_TEMPLATE = '..' + os.sep + 'templates' + os.sep + 'gbu_tests.html'
GBU_MAIN_DEATH_TEMPLATE = '..' + os.sep + 'templates' + os.sep + 'gbu_deaths.html'
GBU_MAIN_CASE_FATALITY_TEMPLATE = '..' + os.sep + 'templates' + os.sep + 'gbu_case_fatality.html'

GBU_STATE_TEMPLATE = '..' + os.sep + 'templates' + os.sep + 'gbu_state.html'

HOTSPOTS_TEMPLATE = '..' + os.sep + 'templates' + os.sep + 'hotspots.html' 
ALERTS_TEMPLATE = '..' + os.sep + 'templates' + os.sep + 'alerts.html'
ALERTS_TEMPLATE_DELTA = '..' + os.sep + 'templates' + os.sep + 'alerts-d.html'

COUNTY_POP =  '..' + os.sep + 'data' + os.sep + 'pop_est_2019.csv'
COUNTY_NAMES =  '..' + os.sep + 'data' + os.sep + 'county_fips_master.csv'

# KEY DATES (lockdown)
KEY_DATES =   STATIC_DATA_PATH + os.sep + 'key-dates.csv'

# US POPULATION
US_POPULATION = STATIC_DATA_PATH + os.sep + 'us_states_pop.csv'
 
############# INTERNATIONAL
INTL_TMP_DATA_PATH = TMP_DATA_PATH + os.sep + 'intl' 
INTL_DATA_URL = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/ecdc/"
INTL_FILE_TYPES = ['new_cases_per_million','new_deaths_per_million','total_cases_per_million','total_deaths_per_million']
INT_DATA = '..' +  os.sep + 'corona-calc' + os.sep + 'data'

############## UWASH
UWASH_FILE_TO_USE = {
  "estimation" : "Reference_hospitalization_all_locs.csv",
  "masks"      : "Best_mask_hospitalization_all_locs.csv",
  "easing"     : "Worse_hospitalization_all_locs.csv"
}

############# FOR MD ONLY
MD_LOCAL_CSV_FILE = "MD_ZIP_DATA"
MD_ZIP_CODES      = "MD_ZIP_REL_DATA"
MD_ZIPS_TEMPLATE = '..' + os.sep + 'templates' + os.sep + 'gbu_MD_zip.html'
MD_ALERTS_TEMPLATE = '..' + os.sep + 'templates' + os.sep + 'alerts_MD.html'
MD_MOST_ACTIVE_TEMPLATE = '..' + os.sep + 'templates' + os.sep + 'most_active_MD.html'

############  SVG
SVG_TEMPLATES = '..' + os.sep + 'templates' + os.sep + 'states' + os.sep 

SVG_FLASHCARD_OUT1 =  "." + os.sep + "flashcards_data" 

# How many legend partition for the svg maps 
MAP_COLORS = [
   '#fee7dc',
   '#fdd4c2',
   '#fcbaa0',
   '#fc9f81',
   '#fb8464',
   '#fa6949',
   '#f24a35',
   '#e32f27',
   '#ca171c',
   '#b11117',
   '#8f0912',
   #'#7d0810',
   #'#6c060d',
   #'#56050a',
   #'#410408',
   #'#2c0205',
   #'#030000'
]
    
 

###############
LARGE_NUMBER = 99999999999999999




def display_us_format(_float,prec): 
   _format =  '{:,.'+str(prec)+'f}'
   return _format.format(_float)


# Compute X day average on set of data
def get_X_day_avg(max_day,data,_type):
 
   # X days average 
   tempValForAvg = []
   tempValFormax_day = []

   all_x_avg = []
   all_y_avg = []

   for d in data:
      for day in d:
 
         # For average of _type
         tempValForAvg.append(d[day][_type])

         if(len(tempValForAvg) <  max_day):
            tempValFormax_day = tempValForAvg 
         else: 
            tempValFormax_day = tempValForAvg[len(tempValForAvg)-max_day:len(tempValForAvg)] 
               
         # We have strings...
         tempValFormax_day = [float(i) for i in tempValFormax_day]
 
         all_x_avg.append(day)
         all_y_avg.append(np.mean(tempValFormax_day))   
   

   cur_new_cases     = all_y_avg[-1] 
   max_day = 0 - max_day

   # For barely impacted counties
   try:
      last_new_cases = all_y_avg[max_day] 
   except IndexError:
      last_new_cases = 0
    

   
   if last_new_cases  > 0:
      delta = cur_new_cases / last_new_cases
   else:
      delta = 0
   
   return all_x_avg, all_y_avg, delta


# Get X day average cases data for a state
def get_avg_data(max_day,state,_type):

   # Open the related json
   json_ftmp = open(PATH_TO_STATES_FOLDER + os.sep + state + os.sep + state + '.json')
   data = json.load(json_ftmp)
   json_ftmp.close()
 
   return get_X_day_avg(max_day, data['stats'],_type) 

# String YYYYMMDD to YYYY-MM-DD
def st_date_readable_st_date(tmp_date):
   if(tmp_date is not None):
      return  tmp_date[0:4]+'-'+tmp_date[4:6]+'-'+tmp_date[6:8] 
   else:
      return '1979-01-01'

if __name__ == "__main__":
   print(display_us_format(46854684864653.5665,2))