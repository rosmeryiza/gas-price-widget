'''
Getting average gas prices for Florida and Miami
'''

import csv
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd

# Link to the AAA page for FL
url = "https://gasprices.aaa.com/?state=FL"

# Function to get the average gas prices in Miami, Ft. Lauderdale and FL
def priceScraper(url):
    # identify User Agent to avoid 403 Error
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')

    # grab the Florida avg table
    fl_stats = soup.find("table") 

    # filter out current and yesterday's numbers
    currentStats = fl_stats.find_all("tr")[1]
    yesterdayStats = fl_stats.find_all("tr")[4]

    # format and save FL prices into variables
    flReg = '$' + str(round(float(currentStats.find_all('td')[1].text[1:]), 2))
    flDiesel = '$' + str(round(float(currentStats.find_all('td')[4].text[1:]), 2))
    flMonthReg = '$' + str(round(float(yesterdayStats.find_all('td')[1].text[1:]), 2))
    flMonthDiesel = '$' + str(round(float(yesterdayStats.find_all('td')[4].text[1:]), 2))

    cities = soup.find_all('h3')

    # Index of Ft Lauderdale in the table is 3
    ftLaud = cities[3]
    # Index of Miami in the table is 10
    miami = cities[10]

    # grab the rows that contain current and month ago avgs for Miami and Ft Lauderdale
    ftLaudRow = ftLaud.find_next_sibling().find_all("tr")[1]
    ftLaudMonthRow = ftLaud.find_next_sibling().find_all("tr")[4]
    miamiRow = miami.find_next_sibling().find_all("tr")[1]
    miamiMonthRow = miami.find_next_sibling().find_all("tr")[4]

    # save and format variables for Miami and Ft Lauderdale
    miamiReg = '$' + str(round(float(miamiRow.find_all('td')[1].text[1:]), 2))
    miamiDiesel = '$' + str(round(float(miamiRow.find_all('td')[4].text[1:]), 2))
    miamiMonthReg = '$' + str(round(float(miamiMonthRow.find_all('td')[1].text[1:]), 2))
    miamiMonthDiesel = '$' + str(round(float(miamiMonthRow.find_all('td')[4].text[1:]), 2))
    ftLaudReg = '$' + str(round(float(ftLaudRow.find_all('td')[1].text[1:]), 2))
    ftLaudDiesel = '$' + str(round(float(ftLaudRow.find_all('td')[4].text[1:]), 2))
    ftLaudMonthReg = '$' + str(round(float(ftLaudMonthRow.find_all('td')[1].text[1:]), 2))
    ftLaudMonthDiesel = '$' + str(round(float(ftLaudMonthRow.find_all('td')[4].text[1:]), 2))

    '''
    print("Miami's current average gas prices are: \n" + "Regular: " + miamiReg + "\n" + "Diesel: " + miamiDiesel)
    print()
    print("Miami's average gas prices a month ago were: \n" + "Regular: " + miamiMonthReg + "\n" + "Diesel: " + miamiMonthDiesel)
    print("-----------------------------------------------------")
    print("Fort Lauderdale's current average gas prices are: \n" + "Regular: " + ftLaudReg + "\n" + "Diesel: " + ftLaudDiesel)
    print()
    print("Fort Lauderdale's average gas prices a month ago were: \n" + "Regular: " + ftLaudMonthReg + "\n" + "Diesel: " + ftLaudMonthDiesel)
    print("-----------------------------------------------------")
    print("Florida's current average gas prices are: \n" + "Regular: " + flReg + "\n" + "Diesel: " + flDiesel)
    print()
    print("The state's average gas prices a month ago were: \n" + "Regular: " + flMonthReg + "\n" + "Diesel: " + flMonthDiesel)
    '''

    dict = { '':['Miami', 'Miami (Month Ago)', 'Fort Lauderdale', 'Fort Lauderdale (Month Ago)', 'Florida', 'Florida (Month Ago)'],
            'Regular': [miamiReg, miamiMonthReg, ftLaudReg, ftLaudMonthReg, flReg, flMonthReg],  
            'Diesel': [ miamiDiesel, miamiMonthDiesel, ftLaudDiesel, ftLaudMonthDiesel, flDiesel, flMonthDiesel]
            }

    df = pd.DataFrame(dict)
    #print(df)

    df.to_csv('gasPrices.csv', index=False)

#Call the function
priceScraper(url)

