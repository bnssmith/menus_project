"""
Purpose: Appends pages of menus together.
Author: Sebastian Brown (sebastian.brown80@gmail.com)
Last edited on 11 September 2018 by Ben Smith
"""

from os import chdir
from glob import glob
import re
import pandas as pd

states = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado',
          'Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho',
          'Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine',
          'Maryland','Massachusetts','Michigan','Minnesota','Mississippi',
          'Missouri','Montana','Nebraska','Nevada','New Hampshire',
          'New Jersey','New_Mexico','New_York','North_Carolina','North_Dakota',
          'Ohio','Oklahoma','Oregon','Pennsylvania','Rhode_Island',
          'South_Carolina','South_Dakota','Tennessee','Texas','Utah',
          'Vermont','Virginia','Washington','West_Virginia','Wisconsin',
          'Wyoming']

base_dir = 'R:\\JoePriceResearch\\school_menus\\Testing\\file_renaming\\PDF_menus_2017\\CSV_menus_2017\\'

#for state in states:
state = 'Alabama'
state_dir = base_dir + '\\' + state
appending_dir = state_dir + '\\Appended'
chdir(state_dir)
state_file_list = []

# Gets list of all file names in folder
for file_name in glob('*csv'):
    #print(file_name)
    state_file_list.append(file_name)
state_file_sublists = []

# Creates a list of lists where each sublist lists the file names of a menu's pages
for i in range(len(state_file_list)):
    sublist = []
    for j in range(len(state_file_list)):
        if re.match('\w+2017',state_file_list[i]) != None and re.match('\w+2017',state_file_list[j]) != None:
            if re.match('\w+2017',state_file_list[j]).group(0) == re.match('\w+2017',state_file_list[i]).group(0) \
            and re.match('\w+2017',state_file_list[j]).group(0) not in sublist:
                #print(state_file_list[j])
                sublist.append(state_file_list[j])
    sublist = sorted(sublist) # likely unecessary, but ensures uniform sorting so no list of pages gets added more than one due to a difference in ordering
    if sublist not in state_file_sublists:
        state_file_sublists.append(sublist)

# Excludes empty sublist from list
state_file_sublists = [sublist for sublist in state_file_sublists if len(sublist) >= 1]

# Appends pages
for sublist in state_file_sublists:
    #print(sublist)
    appending_df = pd.DataFrame([])
    for file in sublist:
        #print(file)
        #with open(file, 'r') as f:
        #    text = f.read()
        #    print(text)
        try:
            file_df = pd.read_csv(file, encoding='latin1', error_bad_lines=False)
            appending_df = pd.concat([appending_df,file_df])
        except:
            print('\n' + file + ' skipped\n')
      
    chdir(appending_dir)
    #appending_df.to_csv(re.sub('_1','',sublist[0]), index=False)
    appending_df.to_csv(re.sub('_1','',sublist[0]), encoding='utf-8', index=False)
    chdir(state_dir)

del appending_df
del file_df

