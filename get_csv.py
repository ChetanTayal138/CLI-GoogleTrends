import argparse
from pytrends.request import TrendReq
from datetime import date
from send_email import generate_email 
import math
import pandas as pd 


def generate_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kw1" , help = "First Interest")
    parser.add_argument("--kw2" , help = "Second Interest")
    parser.add_argument("--kw3" , help = "Third Interest")
    parser.add_argument("--kw4" , help = "Fourth Interest")
    parser.add_argument("--kw5" , help = "Fifth Interest")
    parser.add_argument("--filename" , help = "File containing names of keywords")
    parser.add_argument("--location", help = "Location of interest. IN- India, Defaults to Worldwide")
    parser.add_argument("--timezone" , help = "Data timeframe. all : all time data, defaults to 5 years")
    parser.add_argument("--download" , help = "set to true to download csv file")
    parser.add_argument("email_id" , help = "Recipients Email ID")
    args = parser.parse_args()
    
    return parser,args



def read_file(filename):
    keywords = []
    f = open(filename, "r")
    for line in f:
        line = line.strip('\n')
        keywords.append(line)

    return keywords




def read_keywords(filename):
    lists = []
    if(filename):
        lists = read_file(filename)

    else:
        kw_list = [args.kw1,args.kw2,args.kw3,args.kw4,args.kw5]
        for key in kw_list:
            if key is not None:
                lists.append(key)

    return lists 





def generate_wordsets(lists):
    

    num_groups = int(math.ceil(len(lists)/5)) #Since Google Trends supports a maximum of 5 keywords to be searched at a time
    groups = []
    for i in range(num_groups):
        groups.append([])
    
    count = 0 
    j = 0

    for word in lists:
        groups[count].append(word)
        j = j + 1 
        if(j==5):
            count = count + 1 
            j = 0 

    return groups






def main():
    parser,args = generate_parser()
    PyTrends = TrendReq(hl = 'en-US', tz=360)
    lists = read_keywords(args.filename)   
    DF = pd.DataFrame(columns=['date'])

    if args.timezone == None:
        if len(lists) > 5:
            wordset = generate_wordsets(lists)
            for listset in wordset:
                i = 0
                PyTrends.build_payload(listset,cat=0,timeframe="today 5-y",geo=args.location,gprop='')
                df = PyTrends.interest_over_time()
                df = df.iloc[:,:-1]
                df = df.iloc[:,:-1]      
                df = df.reset_index()
                DF = pd.merge(DF,df,on='date',how='outer')
                
                
            
                

        else:
            PyTrends.build_payload(lists,cat=0,timeframe="today 5-y", geo=args.location,gprop='')

    else:
        PyTrends.build_payload(lists, cat=0, timeframe=args.timezone, geo=args.location, gprop='')
                                                                                        
    
    
    
    today = date.today()
    
    if(args.download):
        print("Generating CSV File")
        filename = "csvfiles/interest_over_time_" + str(today) + ".csv"
        DF.to_csv(filename)
        print("Sending Email")
        generate_email(filename, args.email_id)


        

        
if __name__ == "__main__":
    main()
   

