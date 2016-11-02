import pandas as pd, numpy as np, sklearn
import datetime, dateutil, string
from sklearn.feature_extraction.text import CountVectorizer
import re, nltk, glob
from bs4 import BeautifulSoup
from nltk.corpus import stopwords # Import the stop word list

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0
    
def clean_text( summary ):
    my_text = BeautifulSoup(summary).get_text() 
    letters_only = re.sub("[^a-zA-Z]", " ", my_text) 
    words = letters_only.lower().split()
    stops = set(stopwords.words("english"))                  
    meaningful_words = [w for w in words if not w in stops]   
    return( " ".join( meaningful_words ))   

def get_feature_frame(df):
    my_text = [clean_text(summary) for summary in my_frame["summary"].values]
    my_cv = CountVectorizer()
    X = my_cv.fit_transform(my_text)
    
    out = pd.concat( (df, pd.DataFrame(X)), axis=1)
    
    return out

def process(line):
    naive_split = line.split(',')
    try:
        timestamp = dateutil.parser.parse(naive_split[0])
    except:
        print "failed on", line
        raise Exception
    title = naive_split[1]
    url = naive_split[-1]
    summary = string.join(naive_split[2:-1])
    
    ## Server saves GMT by default but we're five hours behind
    
    time_adjusted = timestamp - datetime.timedelta(hours=5)
    time_adjusted = unix_time_millis(time_adjusted)    
    
    new_line = str(time_adjusted) + '|' + title + '|' + summary + '|' + url
    
    return new_line
    
if __name__ == "__main__":
    ## Process all unfixed files

    raw_files = glob.glob("./*.csv")
    raw_files = [f for f in raw_files if "fixed" not in f]

    for f in raw_files:
        this_file = open(f, "r")
        new_file = open(f+"_fixed.csv", "w")
        for line in this_file.readlines():
            try:
                new_file.write(process(line)+"\n")
            except:
                print f
        this_file.close()
        new_file.close() 
        
    fixed_files = glob.glob("./*_fixed.csv")
    for f in fixed_files:
        this_frame = pd.read_csv(f)
        features = get_feature_frame(this_frame)
        
        name = f.split("/")[1].split("_")[0]
        features.to_csv(name+"_features.csv")
        
    