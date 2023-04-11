# https://scrapfly.io/blog/web-scraping-with-selenium-and-python/
import requests, json, sys, selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pyautogui

# configure webdriver
options = Options()
# options.add_argument('--headless')   # hide GUI
options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
options.add_argument("start-maximized")  # ensure window is full-screen

# we're generating searchterms so we can parse the data (which range in years from 1900 to 2015) 
# as comprehensively as possible. we add the question mark, since some dates are only guessed at and
# thus marked with a ?
searchterms = list(map(str,list(range(1900, 2016))))
searchterms += [ele + '?' for ele in searchterms]

# load webpage
driver = webdriver.Chrome(options=options)
url = 'http://cine-holocaust.de/site/cdh.php'
driver.get(url)


res = []
# searchterms = ['\''] # for testing
for searchterm in searchterms:
    print(searchterm)
    element = WebDriverWait(driver=driver, timeout=5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class=srchctrl]')))
    ele = driver.find_element(By.XPATH, '//input[@id="srchinput"]').send_keys(searchterm, Keys.ENTER)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tags = soup.find('div', {'id': 'resultzone'}).descendants
    numbers =  re.findall(r'\d+', soup.find('div', {'id': 'resultzone'}).find('p').text[:-6])
    print('numbers', numbers)
    # if there are search results
    if numbers:
        num_results = max(map(int, re.findall(r'\d+', soup.find('div', {'id': 'resultzone'}).find('p').text[:-6])))
        num_page_turns = math.ceil(num_results/20)
        print(num_page_turns, num_results)
        for i in range(num_page_turns):
            for child in tags:
                tbl = child.find('div')
                if tbl and isinstance(tbl, Tag):
                    tmp = [e.get_text() for e in tbl.find_all('p')]
                    dct = {tmp[i]:tmp[i+1] for i in range(0,len(tmp)-1,2)}
                    res.append(dct)
            print(i)
            if i == 0 and num_page_turns > 1:
                # if first page
                driver.find_element(By.XPATH, '//p[@class="respaging"]/a[1]').click() #a[1] because xpath not zero indexed
                time.sleep(1)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                tags = soup.find('div', {'id': 'resultzone'}).descendants
            elif i < num_page_turns-1 and i != 0:
                print(driver.find_element(By.XPATH, '//p[@class="respaging"]/a').text)
                driver.find_element(By.XPATH, '//p[@class="respaging"]/a[2]').click()
                time.sleep(1)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                tags = soup.find('div', {'id': 'resultzone'}).descendants
            
    # delete searchterm in searchbar to free it for new searchterm
    driver.find_element(By.XPATH, '//input[@id="srchinput"]').clear()
print(len(res))
