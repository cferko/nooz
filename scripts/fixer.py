"""
This script takes the captured news files and 'fixes' them by subtracting
off the 5 hour time difference from GMT and removes duplicates.
"""
import glob, string, datetime, dateutil, pytz
import pandas as pd, numpy as np

def GMT_to_EST(time_string):
    """Takes a representation of a GMT stamp and converts to EST
    """
    
    this_timestamp = dateutil.parser.parse(time_string)    
    time_adjusted = this_timestamp - datetime.timedelta(hours=5)
    
    return time_adjusted    

def fix(my_filename):
    """Takes an unfixed CSV and saves a fixed version
    """
    unfixed_csv = pd.read_csv(my_filename, sep='|',
                              lineterminator='}',
                              header=None)

    fixed_timestamps = unfixed_csv[0].apply(lambda row: GMT_to_EST(row))
    unfixed_csv[0] = fixed_timestamps
    
    n_cols = len(unfixed_csv.columns)
    ## Get rid of duplicates
    unfixed_csv = unfixed_csv.drop_duplicates(subset=range(1, n_cols))
    
    new_name = my_filename.split(".")[0] + "_fixed.csv"
    
    unfixed_csv.to_csv(new_name)

    return

if __name__=="__main__":
    these_csvs = glob.glob("./*.csv")
    unfixed = [csv for csv in these_csvs if "fixed" not in csv 
                and csv.split(".")+"_fixed.csv" not in these_csvs]
    
    for thing in unfixed:
        fix(thing)