import sys
import os
import json
import numpy as np
import glob

from generate_graphs import generate_graph_with_avg
from international_covid import US_STATES_DATA_PATH

#################################################################################################
# GLOBAL VARS
dir_path = os.path.dirname(os.path.realpath(__file__))
if('/var/www/projects/' in dir_path):
   from conf_vince import *   
else:
   from conf import *

US_STATES_ABBR = { 'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'Washington DC', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming', }
GBU_IMAGE_RELATIVE = os.sep + 'gbu_images'
GBU_IMAGE_PATH = ORG_PATH + GBU_IMAGE_RELATIVE
GBU_MAIN_TEMPLATE = ORG_PATH + os.sep + 'templates' + os.sep + 'gbu.html'
GBU_STATE_TEMPLATE = ORG_PATH + os.sep + 'templates' + os.sep + 'gbu_state.html'
 
# Create Groups of Good, Ugly & Bad States
# for main GBU page
def rank_states():
   
   print("Ranking the states...")

   groups = {'good': [], 'bad': [], 'ugly': []} 
   tmp_cases = []

   for st in US_STATES_ABBR: 
      #print("Parsing " + US_STATES_ABBR[st] +  " data") 

      # Open related json file under covid-19-intl-data
      tmp_json = open(US_STATES_DATA_PATH + "/" + st + ".json",  'r')
      state_data = json.load(tmp_json)
      max_val = 0

      for day in state_data:
         tmp_cases.append(float(state_data[day]['ncpm'])) # Here we take the Number of cases per million into account
         
         if len(tmp_cases) < 7:
            avg = int(np.mean(tmp_cases))
         else: 
            avg = int(np.mean(tmp_cases[-7:]))
         
         if avg > max_val:
            max_val = avg

      last_val_perc = avg / max_val 
      if last_val_perc >= .8 and avg > 5:
         groups['ugly'].append(st) 
      elif .4 < last_val_perc < .8 and avg > 5:
         groups['bad'].append(st) 
      else:
         groups['good'].append(st) 
   
   return groups


# Rank counties for a given state
def rank_counties(st):
   
   print("Ranking the counties for "  + US_STATES_ABBR[st])

   groups = {'good': [], 'bad': [], 'ugly': []} 
   tmp_cases = []

   # Glob the related directory
   all_countries_json_file = glob.glob(US_STATES_DATA_PATH + os.sep + st + os.sep + "*.json")
    
   for st in all_countries_json_file: 
      
      # Open related json file under covid-19-intl-data
      tmp_json = open(st,  'r')
      state_data = json.load(tmp_json)
      max_val = 0

      for day in state_data:
         tmp_cases.append(float(state_data[day]['ncpm'])) # Here we take the Number of cases per million into account
         
         if len(tmp_cases) < 7:
            avg = int(np.mean(tmp_cases))
         else: 
            avg = int(np.mean(tmp_cases[-7:]))
         
         if avg > max_val:
            max_val = avg

      last_val_perc = avg / max_val 
      if last_val_perc >= .8 and avg > 5:
         groups['ugly'].append(st) 
      elif .4 < last_val_perc < .8 and avg > 5:
         groups['bad'].append(st) 
      else:
         groups['good'].append(st) 
   
   return groups

# Create Graphics for all states 
# and insert them into the GBU template (main page)
def generate_gbu_graphs_and_main_page(groups): 
   color = ""

   # Open Template
   f_template =  open(GBU_STATE_TEMPLATE,  'r')
   template = f_template.read() 
   f_template.close() 

   # Create Directory for GBU images
   if not os.path.exists(GBU_IMAGE_PATH):
      os.makedirs(GBU_IMAGE_PATH) 

   for group in groups:

      if(group == 'ugly'):
         color = "r"
      elif(group == 'bad'):
         color = "o"
      else:
         color = "g"
      
      domEl = ""

      for state in groups[group]:

         # Generate the Image
         generate_graph_with_avg(state, 'ncpm', color, GBU_IMAGE_PATH, '')

         # Get the DOM Element
         domEl += create_state_DOM_el(state)

      # Add to the template 
      template = template.replace('{'+group.upper()+'}',domEl)
    
   # Save Template as main gbu page
   main_gbu_page = open('./corona-calc/main_gbu.html','w')
   main_gbu_page.write(template)
   main_gbu_page.close()

   print("Main gbu page (main_gbu.html) created")


# Create the GBU page for a given state 
def generate_gbu_graphs_and_state_page(state, groups):
   # Open Template
   f_template =  open(GBU_MAIN_TEMPLATE,  'r')
   template = f_template.read() 
   f_template.close()
  
   # Create Directory for GBU images
   if not os.path.exists(GBU_IMAGE_PATH):
      os.makedirs(GBU_IMAGE_PATH) 

   for group in groups:

      if(group == 'ugly'):
         color = "r"
      elif(group == 'bad'):
         color = "o"
      else:
         color = "g"
      
      domEl = ""

      for county in groups[group]:
 
         # Get county name
         county_name = os.path.basename(county)
         ind = county_name.index('--')
         county_name = county_name[0:ind] 

         # Generate the Image
         print("Create Graph for " + county_name)
         generate_graph_with_avg(state, 'ncpm', color, GBU_IMAGE_PATH, county)
       

         # Get the DOM Element
         domEl += create_county_DOM_el(state,county_name)

      # Add to the template 
      template = template.replace('{'+group.upper()+'}',domEl)
    
   # Save Template as main gbu page
   main_gbu_page = open('./corona-calc/'+state+'_gbu.html','w')
   main_gbu_page.write(template)
   main_gbu_page.close()

   print("State gbu page ("+state+"_gbu.html) created")


# Create State HTML Element with image
def create_state_DOM_el(st) :
   return '<div class="graph_g"><h3 class="nmb">'+US_STATES_ABBR[st]+'</h3><a href="./gbu/'+st+'.html"><img src="..'+GBU_IMAGE_RELATIVE+os.sep+st+'.png" "idth="345" alt="'+US_STATES_ABBR[st]+'"/></a></div>' 

# Create County HTML Element with image
def create_county_DOM_el(st,ct) :
   return '<div class="graph_g"><h3 class="nmb">'+ct+', ' + st +'</h3><img src="..'+GBU_IMAGE_RELATIVE+os.sep+ct+'_'+st+'.png" "idth="345" alt="'+ct+'"/></div>' 


def main_menu():

   print("---------------")
   print("Select Function")
   print("---------------")
   print("0) Exit") 
   print("1) Create Main GBU Page") 
   print("2) Create a State Page")  
   print("3) Create all States Page")  

   cmd = input("Run: ")
   cmd = int(cmd) 

   if cmd == 1: 
      generate_gbu_graphs_and_main_page(rank_states())
      print("\n>>>TASK DONE \n\n") 
   elif cmd== 2:
      cmd = input("State code: ")
      generate_gbu_graphs_and_state_page(cmd,rank_counties(cmd))
      print("\n>>>TASK DONE \n\n") 
   elif cmd== 3:
      for st in US_STATES_ABBR:
         generate_gbu_graphs_and_state_page(st,rank_counties(st))
      print("\n>>>TASK DONE \n\n") 
   elif cmd== 0:
      print("Exit.")
      sys.exit(0)


if __name__ == "__main__":
   os.system("clear") 
   main_menu() 