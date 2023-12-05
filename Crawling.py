from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import subprocess
import time
import pickle
import requests

subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')
option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

path = 'C:\\Users\\vjslv\\PycharmProjects\\exam1\\Dataset02\\'
driver = webdriver.Chrome(options=option)
time.sleep(1)
driver.get("https://www.piku.co.kr/w/rank/5me7Mp")
time.sleep(1)

# 브라우저 창 크기 조절
driver.set_window_size(1200, 800)

data = []
k = 1
for i in range(2):
    # 반응형 테이블 크롤링
    table = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_0"]')
    rows = table.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        tmp = []
        cells = row.find_elements(By.TAG_NAME, "td")
        for cell in cells:
            text = cell.text
            try:
                link = cell.find_element(By.TAG_NAME, "a").get_attribute("href")
                res = requests.get(link)
                file_name = 'Data02_' + str(k) + '.jpg'
                f = open(path + file_name, 'wb')
                f.write(res.content)
                tmp.append(link)
                k += 1
            except:
                tmp.append(text)
        if len(tmp) != 0:
            data.append(tuple(tmp))

    next_button = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_0_next"]')

    try:
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(2)
    except:
        break

with open('Dataset02.pkl', 'wb') as f:
    pickle.dump(data, f)

# 브라우저 닫기
driver.quit()