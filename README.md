# CLI-GoogleTrends

Command Line Interface built on top of PyTrends, a pseudo-API for obtaining data from Google Trends Searches. 

https://github.com/GeneralMills/pytrends


## USAGE

### Using a text file containing the keywords
    python3 get_csv.py --filename keywords.txt --download True reciever_email
    
### Using only keywords 
    python3 get_csv.py --kw1 keyword_one --kw2 --keyword_two --download True reciever_email
