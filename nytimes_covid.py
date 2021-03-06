#!/bin/env python3

#![Imgur](https://i.imgur.com/CrzzuEZ.png)

from pprint import pprint
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys
import json
state_names = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana",
               "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
# todo fix args
if len(sys.argv) == 2:
    chosencounty = sys.argv[1]
if len(sys.argv) > 2:
    chosencounty = sys.argv[1]
    chosenstate = sys.argv[2]
with open('counties.json', 'r') as f:
    countieslist = json.load(f)


def countyRows(file, chosencounty):  # Parses CSVs
    head = ['date', 'county', 'state', 'fips', 'cases', 'deaths']

    file = open(file, 'r').read().splitlines()
    rows = [head] + [i.rstrip(',').split(',') for i in file]
    # if i.split(',')[1].lower()==chosencounty.lower()]
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


def plotCovid(rows, chosencounty, state):
    cases = [int(i[-2]) for i in rows[1:]]
    deaths = [int(i[-1]) for i in rows[1:]]
    date = '/'.join(rows[-1][0].split('-')[1:] + [rows[-1][0].split('-')[0]])
    # Create 2x2 sub plots
    gs = gridspec.GridSpec(2, 2)

    fig = plt.figure()

    ax1 = fig.add_subplot(gs[0, 1])  # row 0, col 0
    ax1.plot(cases, 'r.-')
    if state == chosencounty:
        ax1.set(xlabel='Days since 3/8/2020', ylabel='Cases',
                title=f'{chosencounty.capitalize()} - COVID-19 cases')
    else:
        ax1.set(xlabel='Days since 3/8/2020', ylabel='Cases',
                title=f'{chosencounty.capitalize()} County - COVID-19 cases')

    ax2 = fig.add_subplot(gs[1, 1])  # row 0, col 1
    ax2.plot(deaths, 'm.')
    if state == chosencounty:
        ax2.set(xlabel='Days since 3/8/2020', ylabel='Total deaths',
                title=f'{chosencounty.capitalize()} - COVID-19 deaths')
    else:
        ax2.set(xlabel='Days since 3/8/2020', ylabel='Total deaths',
                title=f'{chosencounty.capitalize()} County - COVID-19 deaths')
    ax2.plot([0, 1])

    ax3 = fig.add_subplot(gs[:, 0])  # row 1, span all columns
    ax3.plot(cases, 'r')
    ax3.plot(deaths, 'm')
    plt.fill_between(np.arange(0, len(cases)), deaths, cases,
                     facecolor="orange",  # The fill color
                     color='r',       # The outline color
                     alpha=0.2)
    plt.fill_between(np.arange(0, len(cases)), deaths,
                     facecolor="orange",  # The fill color
                     color='m',       # The outline color
                     alpha=0.2)
    if state == chosencounty:
        ax3.set(xlabel='Days since 3/8/2020', ylabel='COVID-19 cases and deaths',
                title=f'COVID-19 Tracking\n{chosencounty.capitalize()} \n3/8/2020 - {date}')
    else:
        ax3.set(xlabel='Days since 3/8/2020', ylabel='COVID-19 cases and deaths',
                title=f'COVID-19 Tracking\n{chosencounty.capitalize()} County\n3/8/2020 - {date}')

    fig.set_size_inches(15, 15)

    if not os.path.exists(f'graphs\{state.capitalize()}\\'):
        os.makedirs(f'graphs\{state.capitalize()}\\')
    if chosencounty == state:
        plt.savefig(
            f"graphs\{chosencounty.capitalize().replace(' ','_')}_COVID_plots.png", dpi=100)
    else:
        plt.savefig(
            f"graphs\{state}\{chosencounty.capitalize().replace(' ','_')}_County_COVID_plots.png", dpi=100)
    plt.close()


if __name__ == '__main__':
    if len(sys.argv) > 2:
        print('Curling NY times COVID-19 CSV specifc state and county')
        print(
            f'curl "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv" | rg "{chosencounty.title()},{chosenstate.capitalize()}" > {chosencounty.capitalize().replace(" ","_")}_nytimes.csv')
        os.system(
            f'curl "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv" | rg "{chosencounty.title()},{chosenstate.capitalize()}" > {chosencounty.capitalize().replace(" ","_")}_nytimes.csv')

    elif len(sys.argv) == 1:
        print('Curling NY times COVID-19 CSV all states')
        os.system(
            f'curl "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv" > Covid_nytimes.csv')
        os.system(
            f'curl "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv" > states_covid_data.csv')

    else:
        print('Curling NY times COVID-19 CSV one state only')
        chosenstate = sys.argv[1]
        os.system(
            f'curl "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv" | rg "{chosenstate.title()}" > {chosenstate.capitalize().replace(" ","_")}_nytimes.csv')
        print(
            f'curl "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv" | rg "{chosenstate.title()}" > states_covid_data.csv')
        os.system(
            f'curl "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv" | rg "{chosenstate.title()}" > states_covid_data.csv')

    if len(sys.argv) > 2:
        curledCsv = f'{chosencounty.capitalize().replace(" ","_")}_nytimes.csv'
        rows = countyRows(curledCsv, chosencounty)
        print(chosencounty, chosenstate)
        plotCovid(rows, chosencounty, chosenstate)
        '''
        if sys.platform == 'win32':
            os.system(
                f"explorer.exe graphs/{chosenstate.capitalize()}/{chosencounty.capitalize()}_County_COVID_plots.png")
        else:
            os.system(
                f"xdg-open graphs/{chosenstate.capitalize()}/{chosencounty.capitalize()}_County_COVID_plots.png")
        '''
        finalRows = [['Date', 'Cases', 'Deaths']] + \
            [i for i in reversed(rowStr(rows))]
    # should edit to be any state and find the list of counties
    elif len(sys.argv) == 2:
        # one state only
        state = sys.argv[1]
        curledCsv = f'{state.capitalize().replace(" ","_")}_nytimes.csv'
        counties = list(x.replace('county', '').replace('County', '').strip()
                        for x in countieslist[state.title()].keys())
        # need to grep for each county, maybe make the csv then delete
        for county in counties:
            filename = county.replace(' ', '_')
            print(
                f'rg -i "{county}" {state.capitalize().replace(" ","_")}_nytimes.csv > {filename}temp.csv')
            os.system(
                f'rg -i "{county}" {state.capitalize().replace(" ","_")}_nytimes.csv > {filename}temp.csv')
            curledCsv = f'{filename}temp.csv'
            rows = countyRows(curledCsv, county)
            plotCovid(rows, county, state)
            os.system(f'del {filename}temp.csv')
        # plotting state
        curledCsv = f'states_covid_data.csv'
        rows = countyRows(curledCsv, state)
        plotCovid(rows, state, state)
        os.remove(f'{state.capitalize().replace(" ","_")}_nytimes.csv')

    else:
        curledCsv = f'Covid_nytimes.csv'

        #counties = ['Baker', 'Benton', 'Clackamas', 'Clatsop', 'Columbia', 'Coos', 'Crook', 'Curry', 'Deschutes', 'Douglas', 'Gilliam', 'Grant', 'Harney', 'Hood', 'River', 'Jackson', 'Jefferson', 'Josephine', 'Klamath', 'Lake', 'Lane', 'Lincoln', 'Linn', 'Malheur', 'Marion', 'Morrow', 'Multnomah', 'Polk', 'Sherman', 'Tillamook', 'Umatilla', 'Union', 'Wallowa', 'Wasco', 'Washington', 'Wheeler', 'Yamhill']
        # need to grep for each county, maybe make the csv then delete
        for state in state_names:
            counties = list(countieslist[state.title()].keys())
            print(state)
            os.system(
                f'rg ",{state}" Covid_nytimes.csv > {state.replace(" ","_")}temp.csv')
            for county in counties:
                countyname = county.replace(
                    "county", "").replace("County", "").strip()
                filename = county.replace("county", "").strip(
                ).replace(" ", "_") + "countytemp.csv"
                print(
                    f'rg -i "{countyname},{state}" {state.replace(" ","_")}temp.csv > {filename}')
                os.system(
                    f'rg -i "{countyname},{state}" {state.replace(" ","_")}temp.csv > {filename}')
                curledCsv = f"{filename}"
                rows = countyRows(curledCsv, countyname)
                plotCovid(rows, countyname, state)
                os.system(f'del {curledCsv}')
            os.system(f'del {state.replace(" ","_")}temp.csv')
            # need to curl new csv https://github.com/nytimes/covid-19-data/blob/master/us-states.csv
            curledCsv = f'states_covid_data.csv'
            os.system(
                f'rg ",{state}" {curledCsv} > {state.replace(" ","_")}temp.csv')
            curledCsv = f'{state.replace(" ","_")}temp.csv'
            rows = countyRows(curledCsv, state)
            plotCovid(rows, state, state)
            os.system(f'del {state.replace(" ","_")}temp.csv')

    '''
    outputCsv = f'All_{chosencounty.capitalize()}_Data_Provided--{finalRows[1][0]}.csv'
    with open(outputCsv, 'w+') as f:
        for i in finalRows:
            f.write(','.join(i))
            f.write('\n')
    '''
