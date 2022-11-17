import json

import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def connect_fifa_ranking(all_ranking=True, start_id=1):
    """First connection to check some page specifications"""

    main_url = 'https://www.fifa.com/fifa-world-ranking/men'

    service = Service(ChromeDriverManager().install())
    service.start()

    driver = webdriver.Chrome(service.path)
    driver.implicitly_wait(10)
    driver.get(main_url)

    new_url = driver.current_url
    last_id = new_url.split('id')[1]
    template_url = new_url.split('id')[0]

    rankings = [start_id, int(last_id), template_url]
    dict_of_dates = read_all_dates(driver)
    driver.quit()

    return rankings, dict_of_dates

def read_all_dates(driver):
    """Read all dates available"""
    element = driver.find_element_by_id('__NEXT_DATA__')
    html_content = element.get_attribute('outerHTML')
    soup_parser = BeautifulSoup(html_content, 'html.parser')
    list_of_dates = json.loads(soup_parser.string)["props"]["pageProps"]["pageData"]["ranking"]["dates"]
    dict_of_dates = {item['id']: item['text'] for item in list_of_dates}

    return dict_of_dates

def check_pages_number(driver):
    """Check the number of pages to append in full rank"""
    element = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/main/section[2]/div/div/div[2]/div/div/div/div/div[2]')   
    html_content = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    number_of_pages = [value.string for value in soup.findChild('div')]
    
    return number_of_pages

def get_single_table(driver, number_of_pages):
    """Single table consult"""
    df_full_ranking = pd.DataFrame()
    #accept_cookies(driver)
    for _ in number_of_pages: # click to the next (page number_of_pages) times
        driver.implicitly_wait(15)
        element_table = driver.find_element_by_class_name("table_rankingTable__7gmVl")
        html_content_table = element_table.get_attribute('outerHTML')
        soup_table = BeautifulSoup(html_content_table, 'html.parser')
        table = soup_table.find(name='table')
        df_single_table = pd.read_html(str(table))[0]
        df_full_ranking = pd.concat([df_full_ranking, df_single_table], axis=0)
        element = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/main/section[2]/div/div/div[2]/div/div/div/div/div[3]/div/button/div")
        driver.execute_script("arguments[0].scrollIntoView();", element)
        driver.execute_script("arguments[0].click();", element)
        
    df_full_ranking = df_full_ranking[['RK', 'Team', 'Total PointsPTS']]
    df_full_ranking.columns = ['RK', 'Team', 'PTS']

    return df_full_ranking


def read_single_date_ranking(ranking_id, template, dict_of_dates):
    """Read ranking for a single date"""
    if ranking_id in dict_of_dates.keys():
        main_url = template + ranking_id
        print(f'main_url = {main_url}')
        service = Service(ChromeDriverManager().install())
        service.start()
        driver = webdriver.Chrome(service.path)
        driver.get(main_url)
        driver.implicitly_wait(15)
        number_of_pages = check_pages_number(driver)
        print(f'{len(number_of_pages)} page(s) to scrap')
        df_single_ranking = get_single_table(driver, number_of_pages)
        driver.quit()

        return df_single_ranking

    else:

        return f'The id{ranking_id} does not exist in dict_of_dates'

def read_a_list_of_dates(list_of_ids, template, dict_of_dates):
    """Read a list of dates given as ids"""
    multiple_rankings = pd.DataFrame()
    for id in list_of_ids:
        print(f'Scrapping Ranking in {dict_of_dates[id]}')
        df_single_ranking = read_single_date_ranking(id, template, dict_of_dates)
        df_single_ranking['WorldCup'] = pd.to_datetime(dict_of_dates[id]).year
        df_single_ranking = df_single_ranking.set_index('WorldCup')
        multiple_rankings = pd.concat([multiple_rankings, df_single_ranking], axis = 0)

    return multiple_rankings

