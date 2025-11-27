#import libraries
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

#define url yang dituju
urls = ['https://vt.tiktok.com/ZSyNYVCKu/',
'https://vt.tiktok.com/ZSDMkoRuN/?_ia=1lcsh7lqaegidE',
'https://www.tiktok.com/@rian_nrd/video/7542703230149463301',
'https://vt.tiktok.com/ZSAmo3kbG/',
'https://www.tiktok.com/@rinaldinurofficial/video/7542707208941882630',
'https://vt.tiktok.com/ZSDkxp57j/',
'https://www.tiktok.com/@dragungspjp/video/7555526913809337656',
'https://vt.tiktok.com/ZSUunC2Sg/',
'https://vt.tiktok.com/ZSA5cRTwP/',
'https://vt.tiktok.com/ZSDBo3h7A/',
'https://vt.tiktok.com/ZSDd4BjTm/',
'https://vt.tiktok.com/ZSUfc1W9q/',
'https://www.tiktok.com/@_ninitata_/video/7559555996478147851',
'https://www.tiktok.com/@naktekpang/video/7558823420591426828',
'https://vt.tiktok.com/ZSUHvmyKA/',
'https://vt.tiktok.com/ZSD2dUfVa/',
'https://vt.tiktok.com/ZSyetYWsC/',
'https://vt.tiktok.com/ZSye3XJsg/',
'https://www.tiktok.com/@heytarbul/video/7551357250166885643',
'https://vt.tiktok.com/ZSDNGY9HT/?_ia=1lcj2z5or1lbsE',
'https://www.tiktok.com/@pak_ributguruviral/video/7547671424790449414',
'https://www.tiktok.com/@triadinata91/video/7547694330073369857',
'https://www.tiktok.com/@medicalhealthlife/video/7566486364275870983',
'https://vt.tiktok.com/ZSy2VxS3Y/',
'https://vt.tiktok.com/ZSyRSRpRV/',
'https://www.tiktok.com/@callme.jesh/video/7559199947174759687',
'https://vt.tiktok.com/ZSDSeAApM/',
'https://vt.tiktok.com/ZSDMBu223/?_ia=1lcs4qengd6aaE',
'https://www.tiktok.com/@bidan_syefiw/video/7564409162889760008',
'https://www.tiktok.com/@adityaspratamaa/video/7566921135330200852?',
'https://vt.tiktok.com/ZSyVJvwoE/',
'https://vt.tiktok.com/ZSyHBF5kq/',
'https://vt.tiktok.com/ZSfDHsfpA/',
'https://www.tiktok.com/@nadhiraafifa_/video/7574750896580463893',
'https://www.tiktok.com/@itsdoktermuda/video/7574730715691011349?lang=en-GB'
]

#define browser yang mau digunakan
driver= webdriver.Chrome()
#tentukan tempat menyimpan hasilnya
rows = []

def convert_to_number(txt):
    if txt is None: return None
    txt = txt.upper().replace(",", "").strip()

    if txt.endswith('K'):
        return int(float(txt[:-1])*1000)
    elif txt.endswith('M'):
        return int(float(txt[:-1])*1000000)
    elif txt.endswith('B'):
        return int(float(txt[:-1])*1000000000)
    
    try:
        return int(txt)
    except:
        return None

for i, url in enumerate(urls, start=1):
    driver.get(url)
    time.sleep(3)
    final_url = driver.current_url
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "strong[data-e2e='like-count']")))
    driver.execute_script("window.scrollTo(0, 500)")
    time.sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    def get_val(key):
        e = soup.find('strong', {'data-e2e':key})
        if not e:
            return None
        val = e.get_text() if e else None
        if val in ['Share', 'Save']:
            return 0
        return convert_to_number(val)
        # return e.get_text() if e else None

    username = final_url.split("/")[3].replace('@', '')
    rows.append({
            'No' : i,
            'Username': username,
            'URL' : final_url,
            'Views': get_val('video-view-count'),
            'Likes' : get_val('like-count'),
            'Comment': get_val('comment-count'),
            'Save': get_val('undefined-count'),
            'Share': get_val('share-count'),
            'Scrape_date': datetime.today().strftime('%Y-%m-%d')
            })
driver.quit()

df = pd.DataFrame(rows)
df.to_excel('Scrapping Energen.xlsx', index=False)
print(df)