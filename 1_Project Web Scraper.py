#!/usr/bin/env python
# coding: utf-8

# In[4]:


from requests import get
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import pandas as pd

if __name__ == '__main__':
    
    result = []
    duration = []
    champions = [] 
    kills = []
    deaths = []
    assists = []
    kda_ratio = []
    multikills = []
    level = []
    cs = []
    cspm = []
    kill_participation = []
    wards = []
    champ_type = []
    
    # List of 20 high ranked players in the North America region
    players = ['Santorin', 'John5un','Sophist+Sage', 'Revenge', 'Tony+Top', 'Johnsun1', 'Saaantorin', 
               'Anivia+Kid', 'ADCADC123', 'Winstón', 'Pobelter', 'ONETRICKPOLICE', 'Gamer+Girl', 'Tomo9', 
              'Value', 'Julien1', 'S2NANA', 'aphromoo', 'Imaqtpie', 'Shiphtur']
    
    # List of AD (Attack Damage) type champions
    AD = ["Aatrox", "Ashe", "Caitlyn", "Camille", "Corki", "Darius", "Draven", "Ezreal", "Fiora", "Gangplank", 
         "Garen", "Gnar", "Graves", "Hecarim", "Illaoi", "Irelia", "Jarvan IV", "Jax", "Jayce", "Jhin", "Jinx", 
         "Kai'Sa", "Kalista", "Kayn", "Kha'Zix", "Kindred", "Kled", "Kog'Maw", "Lee Sin", "Lucian", "Master Yi", 
         "Miss Fortune", "Nasus", "Nocturne", "Olaf", "Pantheon", "Poppy", "Pyke", "Qiyana", "Quinn", "Renekton",
         "Rengar", "Riven", "Senna", "Shaco", "Shen", "Shyvana", "Sion", "Sivir", "Skarner", "Talon", "Thresh", 
         "Tristana", "Trundle", "Tryndamere", "Twitch", "Udyr", "Urgot", "Varus", "Vayne", "Vi", "Volibear", 
         "Warwick", "Wukong", "Xayah", "Yasuo", "Yorick", "Zed"]
    
    # Iterating through players list which is a string of players, in order to manipulate the url
    for player in players:

        # Controlling crawl rate to prevent overloading the server with too many requests
        sleep(randint(2,5)) 
        
        response = get('https://na.op.gg/summoner/userName=' + player)

        html_soup = BeautifulSoup(response.text , 'html.parser')

        match_containers = html_soup.find_all('div' , class_ = 'GameItemWrap')

        # Iterating through match containers
        for match in match_containers:

            # Scraping the match result (Victory / Defeat / Remake)
            match_result = match.find('div', class_ = 'GameResult')
            match_result = match_result.text.strip('\t\n')
            result.append(match_result)


            # Scraping the match duration in minutes
            match_duration = match.find('div', class_ = 'GameLength')
            mins = int(match_duration.text.split(' ')[0].strip('m')) #converting 31m 20s to integer 
            duration.append(mins)


            # Scraping the champion and checking whether the champion is AD(Attack Damage) or AP (Ability Power)
            match_champion = match.find('div', class_ = 'ChampionName')
            match_champion = match_champion.a.text
            champions.append(match_champion)
            if match_champion in AD:
                champ_type.append('AD')
            else:
                champ_type.append('AP')


            # Scraping the number of kills in a match
            match_kills = match.find('span', class_ = 'Kill')
            match_kills = int(match_kills.text)
            kills.append(match_kills)


            # Scraping the number of deaths in a match
            match_deaths = match.find('span', class_ = 'Death')
            match_deaths = int(match_deaths.text)
            deaths.append(match_deaths)


            # Scraping the number of assists in a match
            match_assists = match.find('span', class_ = 'Assist')
            match_assists = int(match_assists.text)
            assists.append(match_assists)


            # Determining the KDA Ratio (Kill-Deaths-Assists ratio)
            if match_deaths == 0:
                kda_ratio.append(100.0)
            else:
                match_kdaratio = (match_kills + match_assists) / match_deaths
                kda_ratio.append(float(match_kdaratio))


            # Scraping the highest multikill in a match    
            match_multikill = match.find('div', class_ = 'MultiKill')
            if str(type(match_multikill)) == "<class 'NoneType'>":
                multikills.append(0)
            elif match_multikill.span.text == 'Double Kill':
                multikills.append(2)
            elif match_multikill.span.text == 'Triple Kill':
                multikills.append(3)
            elif match_multikill.span.text == 'Quadra Kill':
                multikills.append(4)
            elif match_multikill.span.text == 'Penta Kill':
                multikills.append(5)
          


            # Scraping champion level
            match_level = match.find('div', class_ = 'Level')
            match_level = int(match_level.text.strip('\t\n').strip('Level'))
            level.append(match_level)


            # Scraping the CS in a match (Creep Score)
            match_cs = match.find('div', class_ = 'CS')
            li = match_cs.span.text.split(' ')
            cs.append(int(li[0]))
            cspm.append(float(li[1].strip('()')))

            # Scraping Kill Participation in a match
            match_killparticipation = match.find('div' , class_ = 'CKRate')
            match_killparticipation = match_killparticipation.text.strip('\n\t').strip('P/Kill ').strip('%')
            kill_participation.append(int(match_killparticipation))


            # Scraping the wards placed in a match
            match_wards = match.find('div' , class_ = 'Trinket')
            if str(type(match_wards)) == "<class 'NoneType'>":
                wards.append(0)  
            else:
                wards.append(int(match_wards.text.strip('\n\t').strip('Control Ward ')))



    # Creating a data frame using pandas
    test_df = pd.DataFrame({'Result' : result,
                           'Duration' : duration,
                           'Champion' : champions,
                           'Type' : champ_type,
                           'Kills' : kills,
                           'Deaths' : deaths,
                           'Assists' : assists,
                           'KDA Ratio' : kda_ratio,
                           'Multikill' : multikills,
                           'Level' : level,
                           'CS' : cs,
                           'CS per min' : cspm,
                           'Kill Participation' : kill_participation,
                           'Wards' : wards
                           })

    print(test_df.info())
    
    
    # Writing the created data frame to a csv file
    test_df.to_csv('LeagueData.csv')


# In[ ]:




