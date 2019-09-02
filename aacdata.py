#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import re


# In[ ]:


def parse_gender(s):
    # use regex to see if Male or Female is in the string and return that, ele return string
    if bool(re.search('Female', s)):
        return 'Female'
    elif bool(re.search('Male', s)):
        return 'Male'
    else:
        return s


# In[ ]:


def clean_intake_data(filepath):
    '''
    Takes a file path of the Austin Aniaml Center Intake data and returns dataframe after 
    performing the following clean up tasks:
    
    - Parses Date Time into Intake Month and Intake Year columns
    - Parses Sex on Intake into Gender column (Male, Female, Unknown)
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
    
    # drop columns we don't need
    drop_columns=['MonthYear', 'Sex upon Intake']
    df_intake.drop(columns=drop_columns, inplace=True)
    

    return df_intake


# In[ ]:


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


# In[ ]:


def find_duplicate_animals(df):   
    '''
    Takes a dataframe and returns a dataframe with ONLY duplicates based on Animal ID ()
    '''
    # return only the dupes
    df_result = df[df.duplicated(subset='Animal ID', keep=False)].reset_index(drop=True)
    return df_result;


# In[ ]:


def remove_duplicate_animals(df):
    '''
    Takes a dataframe and returns a dataframe WITHOUT duplicates based on Animal ID (dupes are removed)
    '''
    # remove all duplicates, including first one it finds
    df_result = df.drop_duplicates(subset ='Animal ID', keep = False).reset_index(drop=True)
    return df_result;


# In[1]:


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
    '''
    df_combined = pd.merge(df_intake, df_outcome[['Animal ID', 'DateTime', 'Outcome Type', 
                                                  'Outcome Subtype', 'Age upon Outcome', 'Outcome Month', 'Outcome Year']], 
                           how='inner', on='Animal ID', suffixes=(' Intake', ' Outcome'), copy=False)
    return df_combined


# In[ ]:




