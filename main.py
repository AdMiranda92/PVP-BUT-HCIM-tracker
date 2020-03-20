from bs4 import BeautifulSoup
import requests
import sys
import os
import time
import datetime

def get_data(url):
    data = []
    page = requests.get(url=url)
    contents = page.content

    clean = BeautifulSoup(contents, 'html.parser')
    hiscores = clean.find('div', {'id' : 'contentHiscores'})
    stats = hiscores.find('table')
    rows = stats.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    return data

def active(previous_data, url):
    current_data = get_data(url)
    for i in range(35, len(previous_data)-1):
        if int(current_data[i][2].replace(',', '')) > int(previous_data[i][2].replace(',', '')):
            return current_data[i][0]

    for i in range(26, 3, -1):
        if int(current_data[i][3].replace(',', '')) > int(previous_data[i][3].replace(',', '')):
            return current_data[i][0]

    return None

def main():
    url='https://services.runescape.com/m=hiscore_oldschool_hardcore_ironman/hiscorepersonal.ws?user1=pvp_but_hcim'
    tracking_data = get_data(url=url)
    # at this point we have a fully generated list of lists for stats with the following format:
    # ['Skill', 'Rank', 'Level', 'XP'] or ['Name', 'rank', 'killcount']

    print("Tracking Pvp But Hcim, will alert you when a change is found")
    while True:
        currently_active = active(tracking_data, url)

        if currently_active is not None:
            print("Pvp But Hcim change detected in: {0} on {1}".format(currently_active, datetime.datetime.now()))
            tracking_data = get_data(url)
        else:
            time.sleep(60)
            

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)