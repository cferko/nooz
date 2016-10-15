import pandas as pd, numpy as np, dateutil

def split(my_fixed_file):
    unfixed_csv = pd.read_csv(my_filename, sep='|',
                              lineterminator='}',
                              header=None,
                              error_bad_lines = False)
    
    all_stamps = [dateutil.parser.parse(derp) for derp in 
                        unfixed_csv[0].values]
    
    all_dates = np.unique([derp.date for derp in all_stamps])
    
    for date in all_dates:
        this_subset = unfixed_csv[unfixed_csv.apply(lambda row:
                        dateutil.parser.parse(row[0]) == date)]
        
        this_subset.to_csv(date+"_split.csv")
    
    return
    
if __name__=="__main__":
    these_csvs = glob.glob("./*_fixed.csv")

    for thing in these_csvs:
        print "trying to split", thing
        split(thing)