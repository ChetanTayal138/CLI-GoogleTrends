import argparse
from pytrends.request import TrendReq
from datetime import date
from send_email import generate_email 



def generate_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kw1" , help = "First Interest")
    parser.add_argument("--kw2" , help = "Second Interest")
    parser.add_argument("--kw3" , help = "Third Interest")
    parser.add_argument("--kw4" , help = "Fourth Interest")
    parser.add_argument("--kw5" , help = "Fifth Interest")
    parser.add_argument("--location", help = "Location of interest. IN- India, Defaults to Worldwide")
    parser.add_argument("--timezone" , help = "timeframe for data. -all : all time data, defaults to 5 years")
    parser.add_argument("--download" , help = "set to true to download csv file")
    parser.add_argument("email_id" , help = "Recipients Email ID")
    args = parser.parse_args()
    
    return parser,args


def main():
    parser,args = generate_parser()
    PyTrends = TrendReq(hl = 'en-US',tz=360)
    lists = []
    kw_list = [args.kw1,args.kw2,args.kw3,args.kw4,args.kw5]
    for key in kw_list:
        if key is not None:
            lists.append(key)
    
    if args.timezone == None:
        PyTrends.build_payload(lists,cat=0,timeframe="today 5-y",geo=args.location,gprop='')
    else:
        PyTrends.build_payload(lists, cat=0, timeframe=args.timezone, geo=args.location, gprop='')
                                                                                        
    
    df = PyTrends.interest_over_time()
    df = df.iloc[:,:-1]
    today = date.today()
    if(args.download):
        print("Generating CSV File")
        filename = "interest_over_time_" + str(today) + ".csv"
        df.to_csv(filename)
        print("Sending Email")
        generate_email(filename, args.email_id)


        

        
if __name__ == "__main__":
    main()

