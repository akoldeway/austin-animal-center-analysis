# Austin Animal Center Analysis


## Project Outline
Our project is to uncover patterns of behaviors related to abandonded pets entering the Austin Animal Center.  We will examine the kinds of animals entering the facility, the frequency they are being admitted and the reasons why.  We will establish any trends or patterns based on gender, age, breed, etc. We’ll also look into the outcomes of these intakes - adoption, euthanasia, returned to owner, etc. 

## Data Sources
  * Austin Animal Center Intakes and Outcomes: https://www.kaggle.com/aaronschlegel/austin-animal-center-shelter-intakes-and-outcomes

## Data Cleaning
aacdata.py is a file that can be imported that will clean the data we get from Austin Animal Center.  The file has the following functions that we will use:

### clean_file_intake(filepath)

  Takes a file path of the Austin Aniaml Center Intake data and returns dataframe after 
      performing the following clean up tasks:
      
      - Parses Date Time into Intake Month and Intake Year columns
      - Parses Sex on Intake into Gender column (Male, Female, Unknown)
      - Removed the following columns: MonthYear, Sex upon Intake
      
### clean_file_outcome(filepath)
  Takes a file path of the Austin Aniaml Center Outcome data and returns dataframe after 
    performing the following clean up tasks:
    
    - Parses Date Time into Outcome Month and Outcome Year columns
    - Removed the following columns: MonthYear, Date of Birth,  Sex upon Outcome

### find_duplicate_animals(df)
  Takes a dataframe and returns a dataframe with ONLY duplicates based on Animal ID

### remove_duplicate_animals(df)
  Takes a dataframe and returns a dataframe WITHOUT duplicates based on Animal ID (dupes are removed)

### combine_intake_outcome(df_intake, df_outcome)
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