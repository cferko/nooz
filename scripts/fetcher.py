"""
This is a script that periodically checks various news sources,
parses their values, and saves the signals to a csv file.
"""

import datetime, feedparser

## For now let's just work with RSS feeds. Later we can expand
## to parsing raw websites.

MY_FEEDS = [
    "http://oilprice.com/rss/main",
    "https://www.eia.gov/rss/todayinenergy.xml",
    "http://feeds.feedburner.com/latest-news-ogj?format=xml",
    "https://www.eia.gov/about/new/WNtest3.cfm"
]

TODAY = str(datetime.datetime.now().date())

def store_info(entry):
    """Saves the data from a feedparser entry to disk
    
    Args:
        entry: a dictionary of the form output by feedparser
        
    Returns:
        None (saves information to disk)
    """
    
    now = str(datetime.datetime.now())
    
    f = open(TODAY + ".csv", "a")
    f.write(now + ",")
    f.write(entry["title"].encode('ascii', 'ignore') + ",")
    f.write(entry["summary"].encode('ascii', 'ignore') + ",")
    f.write(entry["link"].encode('ascii', 'ignore') +"\n")
    f.close()
    
    return

saved_titles = []

if __name__=="__main__":
    ## Main function loop

    f = open(TODAY+".csv", "w")
    f.write("timestamp,title,summary,link\n")

    last_title = {feed : '' for feed in MY_FEEDS}
    
    done = False    
    
    while not done:
        for feed in MY_FEEDS:
            d = feedparser.parse(feed)
            
            try:
                most_recent = d['entries'][0]
                
            except:
                continue
            
            this_title = most_recent['title']            
            
            ## If this is true, the feed hasn't changed
            if this_title == last_title[feed]:
                continue
            
            ## Otherwise, it has updated
            else:
                last_title[feed] = this_title
                
                for entry in d["entries"]:
                    
                    ## Check if we already have this one
                    if entry["title"] in saved_titles:
                        continue
                    
                    ## Save the information
                    else:
                        saved_titles += entry["title"]
                        store_info(entry)
        
        hour = datetime.datetime.now().time().hour
        
        ## Nasdaq closes at 4 pm, so kill ourselves then
        if hour >= 16:
            done = True