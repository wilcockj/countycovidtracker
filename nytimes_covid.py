#!/bin/env python3

#![Imgur](https://i.imgur.com/CrzzuEZ.png)

from pprint import pprint
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys
import json
state_names = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
#todo fix args 
if len(sys.argv) == 2:
    chosencounty = sys.argv[1]
if len(sys.argv) > 2:
    chosencounty = sys.argv[1]
    chosenstate = sys.argv[2]
with open('counties.json', 'r') as f:
    countieslist = json.load(f)
def countyRows(file,chosencounty): # Parses CSVs
    head = ['date','county','state','fips','cases','deaths']

    file = open(file, 'r').read().splitlines()
    rows =  [head] + [i.rstrip(',').split(',')  for i in file]
    #if i.split(',')[1].lower()==chosencounty.lower()]
    '''
    for x in file:
        print(x.split(',')[1].lower(),chosencounty.lower())
    '''
    return rows

def rowStr(rows):
    returnRows = []

    previous = rows[1]
    for i in rows[2:]:
        row = ['-'.join(i[0].split('-')[1:] + [i[0].split('-')[0]])]
        caseDiff = f'{i[-2]} ==> diff={int(i[-2]) - int(previous[-2])}'
        deathDiff = f'{i[-1]} ==> diff={int(i[-1]) - int(previous[-1])}'

        row.extend((caseDiff, deathDiff))
        returnRows.append(row)
        previous = i

    return returnRows

def plotCovid(rows,chosencounty,state):
    cases = [int(i[-2]) for i in rows[1:]]
    deaths = [int(i[-1]) for i in rows[1:]]
    date = '/'.join(rows[-1][0].split('-')[1:] + [rows[-1][0].split('-')[0]])
    if chosencounty == state:
        print(cases)
    # Create 2x2 sub plots
    gs = gridspec.GridSpec(2, 2)

    fig = plt.figure()

    ax1 = fig.add_subplot(gs[0, 1]) # row 0, col 0
    ax1.plot(cases, 'r.-')
    if state == chosencounty:
        ax1.set(xlabel='Days since 3/8/2020', ylabel='Cases',
            title=f'{chosencounty.capitalize()} - COVID-19 cases')
    else:
        ax1.set(xlabel='Days since 3/8/2020', ylabel='Cases',
            title=f'{chosencounty.capitalize()} County - COVID-19 cases')

    ax2 = fig.add_subplot(gs[1, 1]) # row 0, col 1
    ax2.plot(deaths, 'm.')
    if state == chosencounty:
        ax2.set(xlabel='Days since 3/8/2020', ylabel='Total deaths',
           title=f'{chosencounty.capitalize()} - COVID-19 deaths')
    else:
        ax2.set(xlabel='Days since 3/8/2020', ylabel='Total deaths',
           title=f'{chosencounty.capitalize()} County - COVID-19 deaths')
    ax2.plot([0,1])

    ax3 = fig.add_subplot(gs[:, 0]) # row 1, span all columns
    ax3.plot(cases, 'r')
    ax3.plot(deaths, 'm')
    plt.fill_between(np.arange(0, len(cases)), deaths, cases,
                 facecolor="orange", # The fill color
                 color='r',       # The outline color
                 alpha=0.2)
    plt.fill_between(np.arange(0, len(cases)), deaths,
                 facecolor="orange", # The fill color
                 color='m',       # The outline color
                 alpha=0.2)
    if state == chosencounty:
        ax3.set(xlabel='Days since 3/8/2020', ylabel='COVID-19 cases and deaths',
           title=f'COVID-19 Tracking\n{chosencounty.capitalize()} \n3/8/2020 - {date}')
    else: 
        ax3.set(xlabel='Days since 3/8/2020', ylabel='COVID-19 cases and deaths',
           title=f'COVID-19 Tracking\n{chosencounty.capitalize()} County\n3/8/2020 - {date}')

    fig.set_size_inches(15, 15)

    if not os.path.exists(f'graphs\{state}\\'):
        os.makedirs(f'graphs\{state}\\')
    if chosencounty == state:
        plt.savefig(f"graphs\{chosencounty.capitalize()}_COVID_plots.png", dpi = 100)
    else:
        plt.savefig(f"graphs\{state}\{chosencounty.capitalize()}_County_COVID_plots.png", dpi = 100)
    plt.close()


if __name__ == '__main__':
    if '-getdata' in sys.argv and len(sys.argv) > 2:
        os.system(f'curl "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv" | grep {chosencounty.capitalize()},{chosenstate.capitalize()} > {chosencounty.capitalize()}_nytimes.csv')
        print('Curling NY times COVID-19 CSV')
    elif len(sys.argv) == 1:
        os.system(f'curl "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv" > Covid_nytimes.csv')
        os.system(f'curl "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv" > states_covid_data.csv')
        print('Curling NY times COVID-19 CSV')
    else:
        chosenstate = sys.argv[1]
        os.system(f'curl "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv" | grep {chosenstate.capitalize()} > {chosenstate.capitalize()}_nytimes.csv')
        print('Curling NY times COVID-19 CSV')
    if len(sys.argv) > 2:   
        curledCsv = f'{chosenstate.capitalize()}_nytimes.csv'
        rows = countyRows(curledCsv,chosencounty)
        plotCovid(rows,chosencounty,chosenstate)
        if sys.platform == 'win32': 
            os.system(f"explorer.exe {chosencounty.capitalize()}_County_COVID_plots.png")
        else:
            os.system(f"xdg-open {chosencounty.capitalize()}_County_COVID_plots.png")
        finalRows = [['Date', 'Cases', 'Deaths']] + [i for i in reversed(rowStr(rows))]
    #should edit to be any state and find the list of counties
    elif len(sys.argv) == 2:
        print("one state only")
        curledCsv = f'{sys.argv[1].capitalize()}_nytimes.csv'
        counties = list(x.replace('county','').replace('County','').strip() for x in countieslist[sys.argv[1].capitalize()].keys())
        #counties = ['Baker', 'Benton', 'Clackamas', 'Clatsop', 'Columbia', 'Coos', 'Crook', 'Curry', 'Deschutes', 'Douglas', 'Gilliam', 'Grant', 'Harney', 'Hood', 'River', 'Jackson', 'Jefferson', 'Josephine', 'Klamath', 'Lake', 'Lane', 'Lincoln', 'Linn', 'Malheur', 'Marion', 'Morrow', 'Multnomah', 'Polk', 'Sherman', 'Tillamook', 'Umatilla', 'Union', 'Wallowa', 'Wasco', 'Washington', 'Wheeler', 'Yamhill']
        #need to grep for each county, maybe make the csv then delete
        for county in counties:
            filename = county.replace(' ','_')
            print(f'grep -i "{county}" {chosenstate.capitalize()}_nytimes.csv > {filename}temp.csv')
            os.system(f'grep -i "{county}" {chosenstate.capitalize()}_nytimes.csv > {filename}temp.csv')
            curledCsv = f'{filename}temp.csv'
            rows = countyRows(curledCsv,county)
            plotCovid(rows,county,sys.argv[1])
            os.system(f'del {filename}temp.csv')
        #plotting state
        curledCsv = f'Covid_nytimes.csv'
        rows = countyRows(curledCsv,sys.argv[1])
        plotCovid(rows,sys.argv[1],sys.argv[1])

    else:
        curledCsv = f'Covid_nytimes.csv'
        print(sys.argv)
        
        #counties = ['Baker', 'Benton', 'Clackamas', 'Clatsop', 'Columbia', 'Coos', 'Crook', 'Curry', 'Deschutes', 'Douglas', 'Gilliam', 'Grant', 'Harney', 'Hood', 'River', 'Jackson', 'Jefferson', 'Josephine', 'Klamath', 'Lake', 'Lane', 'Lincoln', 'Linn', 'Malheur', 'Marion', 'Morrow', 'Multnomah', 'Polk', 'Sherman', 'Tillamook', 'Umatilla', 'Union', 'Wallowa', 'Wasco', 'Washington', 'Wheeler', 'Yamhill']
        #need to grep for each county, maybe make the csv then delete
        for state in state_names:
            counties = list(countieslist[state.title()].keys())
            print(state)
            for county in counties:
                print(f'rg -i "{county.title().replace("county","").replace("County","").strip()},{state}" Covid_nytimes.csv > {county.replace("county","").strip().replace(" " ,"_")}temp.csv')
                os.system(f'rg -i "{county.title().replace("county","").replace("County","").strip()},{state}" Covid_nytimes.csv > {county.replace("county","").strip().replace(" " ,"_")}temp.csv')
                curledCsv = f"{county.replace('county','').strip().replace(' ','_')}temp.csv"
                county = county.replace("county","").replace("County","")
                rows = countyRows(curledCsv,county)
                plotCovid(rows,county,state)
                os.system(f'del {curledCsv}')
            #need to curl new csv https://github.com/nytimes/covid-19-data/blob/master/us-states.csv
            curledCsv = f'states_covid_data.csv'
            os.system(f'rg ",{state}" {curledCsv} > {state.replace(" ","_")}temp.csv')
            curledCsv = f'{state}temp.csv'
            rows = countyRows(curledCsv,state)
            plotCovid(rows,state,state)
            os.system(f'del {state}temp.csv')

    

    '''
    outputCsv = f'All_{chosencounty.capitalize()}_Data_Provided--{finalRows[1][0]}.csv'
    with open(outputCsv, 'w+') as f:
        for i in finalRows:
            f.write(','.join(i))
            f.write('\n')
    '''
