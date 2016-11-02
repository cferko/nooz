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
    my_text = [clean_text(summary) for summary in df["summary"].values]
    my_cv = CountVectorizer()
    X = my_cv.fit_transform(my_text)
    
    out = pd.concat( (df, pd.DataFrame(X.todense())), axis=1)
    
    return out

def process_time_string(time_string):
    try:
        timestamp = dateutil.parser.parse(time_string)
        time_adjusted = timestamp - datetime.timedelta(hours=5)
        time_adjusted = unix_time_millis(time_adjusted)    
        
        return time_adjusted
    execept:
        return 0
    
if __name__ == "__main__":
    ## Process all unfixed files

    raw_files = glob.glob("./*.csv")
    raw_files = [f for f in raw_files if "fixed" not in f]

    for f in raw_files:
        this_frame = pd.read_csv(f, sep="|", lineterminator="}", header=None,
                                 names=["timestamp", "title", "summary", "url"])
        
        this_frame["timestamp"] = this_frame["timestamp"].apply(lambda x: process_time_string(x))        
        features = get_feature_frame(this_frame)
        
        name = f.split("/")[1].split(".csv")[0]
        features.to_csv(name+"_features.csv")
        
    