#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re


# In[2]:


def parse_gender(s):
    '''
    Pass in Sex upon Intake value from dataframe and will return age in months
    '''
    # use regex to see if Male or Female is in the string and return that, ele return string
    if bool(re.search('Female', s)):
        return 'Female'
    elif bool(re.search('Male', s)):
        return 'Male'
    else:
        return s


# In[3]:


def parse_age(a):
    '''
    Pass in Age upon Intake or Age upon Outcome value from dataframe and will return age in months
    '''
    #split string and return age as months
    age = a.split()
    total_months = 0
    if age[1] in('month', 'months'):
        if int(age[0]) < 0:
            total_months = 0
        else:
            total_months = int(age[0])
    elif age[1] in('year', 'years'):
        if int(age[0]) < 0:
            total_months = 0
        else:
            total_months = int(int(age[0])*12)
    elif age[1] in('week', 'weeks', 'day', 'days'):
        total_months = 0
    return total_months


# In[4]:


def clean_intake_data(filepath):
    '''
    Takes a file path of the Austin Aniaml Center Intake data and returns dataframe after 
    performing the following clean up tasks:
    
    - Parses Date Time into Intake Month and Intake Year columns
    - Parses Sex on Intake into Gender column (Male, Female, Unknown)
    - Parses Age upon Intake into Intake Age in Months
    - Removed the following columns: MonthYear, Sex upon Intake
    '''
    
    df_intake = pd.read_csv(filepath)
    
    # parse the intake month and year into seperate fields
    df_intake['Intake Month'] = pd.DatetimeIndex(df_intake['DateTime']).month
    df_intake['Intake Year'] = pd.DatetimeIndex(df_intake['DateTime']).year
    
    # first, fill any nan's on the Sex upon Intake column to Unkown
    df_intake['Sex upon Intake'] = df_intake['Sex upon Intake'].fillna('Unknown')

    # now create a new column with parsed gender or "unknown"
    df_intake['Gender'] = df_intake['Sex upon Intake'].apply(parse_gender)
    
    # create column for age in months
    df_intake['Intake Age in Months'] = df_intake['Age upon Intake'].apply(parse_age)
    
    # drop columns we don't need
    drop_columns=['MonthYear', 'Sex upon Intake']
    df_intake.drop(columns=drop_columns, inplace=True)
    

    return df_intake


# In[9]:


def clean_outcome_data(filepath):
    '''
    Takes a file path of the Austin Aniaml Center Outcome data and returns dataframe after 
    performing the following clean up tasks:
    
    - Parses Date Time into Outcome Month and Outcome Year columns
    - Removed the following columns: MonthYear, Date of Birth,  Sex upon Outcome
    '''
    df_outcome = pd.read_csv(filepath)
    
    # DateTime and MonthYear values are both full date times.  Will require some parsing
    df_outcome['Outcome Month'] = pd.DatetimeIndex(df_outcome['DateTime']).month
    df_outcome['Outcome Year'] = pd.DatetimeIndex(df_outcome['DateTime']).year
    
    # drop columns we don't need
    drop_columns=['MonthYear', 'Date of Birth', 'Sex upon Outcome']
    df_outcome.drop(columns=drop_columns, inplace=True)
    
    return df_outcome


# In[6]:


def find_duplicate_animals(df):   
    '''
    Takes a dataframe and returns a dataframe with ONLY duplicates based on Animal ID ()
    '''
    # return only the dupes
    df_result = df[df.duplicated(subset='Animal ID', keep=False)].reset_index(drop=True)
    return df_result;


# In[7]:


def remove_duplicate_animals(df):
    '''
    Takes a dataframe and returns a dataframe WITHOUT duplicates based on Animal ID (dupes are removed)
    '''
    # remove all duplicates, including first one it finds
    df_result = df.drop_duplicates(subset ='Animal ID', keep = False).reset_index(drop=True)
    return df_result;


# In[8]:


def combine_intake_outcome(df_intake, df_outcome):
    '''
    Takes intake and outcome dataframes and returns a single merged dataframe based on following:
    
    - merged on Animal ID
    - how = inner
    - includes all columns on intake dataframe and selects the following from outcome dataframe:
       - DateTime
       - Outcome Type
       - Outcome Subtype
       - Age upon Outcome
       - Outcome Month
       - Outcome Year
    - creates new columns:
       - Date Intake (intake date formatted as Date)
       - Date Outcome (intake date formatted as Date)
       - Days in Center (Date Outcome - Date Intake)
    '''
    df_combined = pd.merge(df_intake, df_outcome[['Animal ID', 'DateTime', 'Outcome Type', 
                                                  'Outcome Subtype', 'Age upon Outcome', 'Outcome Month', 'Outcome Year']], 
                           how='inner', on='Animal ID', suffixes=(' Intake', ' Outcome'), copy=False)
    
    # add new fields to parse intake and outceom date as date
    df_combined['Date Intake'] = pd.to_datetime(df_combined["DateTime Intake"]).dt.date
    df_combined['Date Outcome'] = pd.to_datetime(df_combined["DateTime Outcome"]).dt.date
    
    # calc number of days in center
    df_combined['Days in Center'] = (df_combined['Date Outcome'] - df_combined['Date Intake']).dt.days
    
#     # drop columns we don't need
#     drop_columns=['Date Intake', 'Date Outcome']
#     df_combined.drop(columns=drop_columns, inplace=True)
    

    return df_combined


# In[ ]:




