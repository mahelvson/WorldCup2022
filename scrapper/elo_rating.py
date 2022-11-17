import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

MAIN_URL = 'https://www.eloratings.net/'

def get_elo_rating(main_url=MAIN_URL, dates=[1993]):
    """Iterate over dates to read elo ratings"""
    df_rating_full = pd.DataFrame()   
    for date in dates:
        df_rating_full = pd.concat([df_rating_full, read_single_date_ranking(date, main_url)], axis=0)          

    df_rating_full = df_rating_full.set_index('Year')
    df_rating_full.columns = ['RK', 'Team', 'Rating', 'AverageRank', 'AverageRating', 'YearRank', 'YearRating', 'MatchesTotal',
    'MathcesHome', 'MatchesAway', 'MatchesNeutral', 'MatchesWins', 'MatchesLosses', 'MatchesDraws', 'GoalsFor', 'GoalsAgainst'] 

    return df_rating_full

def read_single_date_ranking(date, main_url=MAIN_URL):
    """Read ranking for a single date"""
    service = Service(ChromeDriverManager().install())
    service.start()
    driver = webdriver.Chrome(service.path)
    driver.implicitly_wait(20)
    driver.get(main_url + f'{date}')
    element = driver.find_element_by_class_name('grid-canvas')
    html_content = element.get_attribute('outerHTML')
    soup_table = BeautifulSoup(html_content, 'html.parser')
    main_ranking = read_single_table(soup_table)
    df_single_rating = pd.DataFrame(main_ranking)
    df_single_rating['Year'] = date
    driver.close()
    return df_single_rating

def read_single_table(soup):
    """Read a single table for speecific year/date"""
    divs_content = [line for line in [bs4obj for bs4obj in list(soup.findAll(attrs={'class': 'ui-widget-content'}))]]
    main_ranking = []

    for content in divs_content:
        line_full = []
        for line in content:
            line_full.append(line.text)
        main_ranking.append(line_full) 

    return main_ranking