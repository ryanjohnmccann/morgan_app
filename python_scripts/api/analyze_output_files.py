# Last updated by:
# Ryan McCann

# Last updated:
# 05/09/20

# Purpose:
# Analyzes output files from our machine learning algorithms. Displays mean, std, and the median

# Issues/Needed Improvements:
# None known at this point in time


import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# TODO: Make these calculations suggestions for more trials of the machine learning
# TODO: Eventually combine these scripts?

des_dir = '/Users/ryanmccann/Desktop/misc/programming/finance_project/winner_data/'
file_names = [f for f in os.listdir(des_dir) if '.json' in f]
des_data_list = list()
pd.set_option('display.max_columns', None)
for obj in file_names:
    curr_file = json.load(open(des_dir + obj))
    des_data_list.append(curr_file)
des_df = pd.DataFrame(des_data_list)
print(des_df)
print("\n\n\n")
print("*** PURCHASE PRICE ***")
print("Mean -->", des_df['purchase_price'].mean())
print("Standard Deviation -->", des_df['purchase_price'].std())
print("Median -->", des_df['purchase_price'].median())

print('\n\n')
print('*** DOWN PAYMENT ***')
print("Mean -->", des_df['down_payment'].mean())
print("Standard Deviation -->", des_df['down_payment'].std())
print("Median -->", des_df['down_payment'].median())

print('\n\n')
print('*** LOAN DURATION ***')
print("Mean -->", des_df['loan_duration'].mean())
print("Standard Deviation -->", des_df['loan_duration'].std())
print("Median -->", des_df['loan_duration'].median())

print('\n\n')
print('*** INTEREST RATE ***')
print("Mean -->", des_df['interest_rate'].mean())
print("Standard Deviation -->", des_df['interest_rate'].std())
print("Median -->", des_df['interest_rate'].median())

print('\n\n')
print('*** YEARLY PAYMENTS ***')
print("Mean -->", des_df['yearly_payments'].mean())
print("Standard Deviation -->", des_df['yearly_payments'].std())
print("Median -->", des_df['yearly_payments'].median())

print('\n\n')
print('*** WEALTH PERCENT ***')
print("Mean -->", des_df['wealth_percent'].mean())
print("Standard Deviation -->", des_df['wealth_percent'].std())
print("Median -->", des_df['wealth_percent'].median())
