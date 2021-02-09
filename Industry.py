import requests
from requests.exceptions import Timeout


#code to get the industry and sector information for an individual stock
def Industry_screen(ticker):

    path = 'https://finance.yahoo.com/quote/' + ticker + '/profile?p=' + ticker
    Bool_except = 0
    try:
        
        x = requests.get(path, timeout=2)
        
    except Timeout as ex:
        
        print("Exception Riased: ", ticker)
        Bool_except = 1
    
    while Bool_except:
     
        try:
            x = requests.get(path, timeout=2)
            Bool_except = 0
            
        except Timeout as ex:
            
            print("Exception Raised: ", ticker)
            Bool_except = 1
        
        
        
        
        
    
    str_x = x.text
    
    
    
    find = str_x.find('Sector')
    
    #makes a substring
    subx = str_x[find:find+8000]
    #print(subx)
     
    
    #looks for a unique identifyer in the code
    val = subx.find('data-reactid')
    
    #makes a much smaller substring
    sub = subx[val:val+150]
    
    
    
    #finds the indexes for the value we are looking for
    begin = sub.find('>')
    
    begin+=1
    
    end = sub.find('<')
    
    str_sector = sub[begin:end]
    
    str_sector = str_sector.replace('&amp;','&')
    
    find = str_x.find('Industry')
    
    subx = str_x[find:find+8000]
    
    val = subx.find('data-reactid')
    
    #makes a much smaller substring
    sub = subx[val:val+150]
    
   
    
    #finds the indexes for the value we are looking for
    begin = sub.find('>')
    
    begin+=1
    
    end = sub.find('<')
    
    str_industry = sub[begin:end]
    
    #replace the html text for &amp with just &
    str_industry = str_industry.replace('&amp;','&')
    
    return(str_sector,str_industry)
    


#change the path to where your list of stocks are located
def main(sort=0):
    
    file = open(r"Penny_Options_$10.txt",'r')
    
    our_list = []
    
    industry_options = []
    
    
    for line in file:
        
        #dont need the first line for our purposes
        if 'Symbol' in line:
            
            continue
        
        this_line = line
        
        ticker = this_line.rsplit('\t',1)[0]
        
        #gets a list of stock tickers
        our_list.append(this_line)    
    
    #print(our_list)
    print('Ticker, Price, Sector, Industry')
    for line in our_list:
        
        #lazy way of fixing text file problems
        ticker = line.rsplit('\t',1)[0]     
        tickers = ticker.rsplit(',')
        tickers[0]= tickers[0][1:]
        tickers[1] = tickers[1][:-1]
        price = tickers[1]
        price = price.strip()
        price = price[1:-1]
        price = price[:-1]
        ticker = tickers[0][1:-1]
        
        
        sector,industry = Industry_screen(ticker.strip())
        
        industry_options.append((ticker,price,sector,industry))
        print(ticker+', '+price+', '+sector+', '+industry+'\n')
        
    file.close()
    file1 = open(r"Industry.txt",'w')
    file1.write('Ticker, Price, Sector, Industry\n')
    
    #allows for the code to be sorted.
    #if you want it sorted by the more general sector
    #change it to lambda x: x[2]
    #otherwise by default it will screen by the specific industry
    if sort == 1:
        industry_options.sort(key = lambda x: x[2])
    for line in industry_options:
        
        this_line = line[0] + ', ' + line[1] + ', ' + line[2] +', ' + line[3]+'\n'
        print(this_line)
        file1.write(str(this_line))   
    
    file1.close()
