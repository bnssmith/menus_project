# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 10:12:34 2018

Purpose: Clean the xlsx files produced by ABBYY and prepare them for use in our project

Note: This program copies a lot of code from pdf_to_txt_pt_2_(3.6)_v3.py in the Python Programs folder
--Built for Python 3

@author: bnssmith
"""

import sys
sys.path.append('R:\\JoePriceResearch\\Python\\Anaconda3\\Lib\\site-packages')
import os
#import csv
#from xlsxwriter.workbook import Workbook
from glob import glob
#import xlrd
from pandas import read_excel
from itertools import chain
import io
#import numpy as np


xls_source_folder = "R:\\JoePriceResearch\\school_menus\\Testing\\file_renaming\\PDF_menus_2017\\XLS_menus_2017"
txt_saving_folder = "R:\\JoePriceResearch\\school_menus\\Testing\\file_renaming\\PDF_menus_2017\\TXT_menus_2017"

os.chdir(txt_saving_folder)

extension = '.xlsx'

min_state = ''

excluded_entries_list = ['START PAGE 0', 'START PAGE 1', 'START PAGE 2',
                         'END PAGE 0', 'END PAGE 1', 'END PAGE 2']

for subdir, dirs, files in os.walk(xls_source_folder):
    os.chdir(xls_source_folder)
    for state in dirs:
        if not state.isdigit() and not state.islower() and state >= min_state:
            print('state: ', state)
            os.chdir(xls_source_folder + "\\" + state)
            for file in list(glob('*.xlsx')): 
                os.chdir(xls_source_folder + "\\" + state)
                print('file: ',file)
                #This part of the code cleans the file and formats it to become the kind of txt we want
                
                
                
                
                
                
                #The rest of the code saves the file as a txt file
                
                # imports excel file
                menu_df = read_excel(file, index_col=None)
                
                
                #There is one file that has duplicates in its dataframe index. Here is one solution:
                #print(menu_df.index.duplicated())
                
                
                #Cullman_city's xlsx gives us duplicates in its index:
                if any(menu_df.index.duplicated()):
                    menu_df.reset_index(inplace=True)  #.pivot_table(values=3, index=[0, 1], columns=2, aggfunc='mean')
                
                # returns a series with all entries (comparable to a table with only one column)
                #Take transpose so that we go by row instead of by column (left-to-right instead of top-to-down)
                menu_df_transposed = menu_df.T
                
                menu_df_unstacked = menu_df_transposed.unstack()
                
                """
                builds a list of strings from series entries
                excludes material which cannot be converted to string format
                """
                
                menu_entry_list = []
                
                for i in menu_df_unstacked:
                    try:
                        new_element = str(i)
                        if new_element not in excluded_entries_list:
                            menu_entry_list.append(new_element)
                    except:
                        print(i)
                
                #removes invalid entries from list; converts \n to newline character
                menu_entry_list = [i for i in menu_entry_list if i != 'nan']
                menu_entry_list = [i.split('\n') for i in menu_entry_list]
                menu_entry_list = list(chain.from_iterable(menu_entry_list))
                
                # writes txt file from list entries
                os.chdir(txt_saving_folder + "\\" + state)
                with io.open(os.path.splitext(file)[0] + '.txt', 'w', encoding="utf-8") as file_object:
                    for i in range(len(menu_entry_list)):
                        file_object.write(menu_entry_list[i] + '\n')
                
                del menu_df
