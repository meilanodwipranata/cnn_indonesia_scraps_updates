import itertools
import time
import json
import bs4
import sys
import requests
from requests import Response
from bs4 import BeautifulSoup
from datetime import datetime
 
on_off = 1
hasil_scan_data = []

def scan_json():
  
    try:
      print("Scanning")
      with open('data.json' ,'r',encoding='utf-8') as json_file:
        data = json.load(json_file)
      while True:
          for i in itertools.count():
            data_scan = data[i]['article']['content_url']
            hasil_scan_data.append(data_scan)
            time.sleep(0.1)
    except IndexError:  
      print("Scan selesai")
    except FileNotFoundError:
      print("data belum ada ya")
    except Exception as e:
      print(e)
      
  
def add_dic_json(new_data):
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            existing_data = json.load(f)
            if isinstance(existing_data, dict):
                existing_data = [existing_data]
    except FileNotFoundError:
        existing_data = []

    if isinstance(new_data, dict):
        existing_data.append(new_data)

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

def get_page(url):  
  req = requests.get(url , headers={'User-Agent': 'Mozilla/5.0'})
  response = BeautifulSoup(req.text,'html.parser')
  page = response.find_all('article')
  if req.status_code == 200:
    return page
  
    
  
def get_article(out_pages):
  try:
    req_article = requests.get(out_pages, timeout=  12, headers={'User-Agent': 'Mozilla/5.0'})
    res_article = BeautifulSoup(req_article.text,'html.parser')
    time.sleep(0)
    return res_article
  except Exception as e:
    print(f"Error article url ,{out_pages}")
    
    
    
   
def dic_data(out_get_article,out_pages,url_pages):
  #ambil data
  domain = out_pages.split('/')[2]
  crawling_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  crawling_time_epoch = int(time.time())
  title = out_get_article.find('h1').get_text(strip=True)
  url = url_pages
  contain_url = out_pages
  categories = out_pages.split('/')[3]
  media_url = out_get_article.find_all('img')[0]['src']
  
  articles = out_get_article.find_all('p')
  article = ' '.join([p.get_text(strip=True) for p in articles])
  if article == "":
    article = "-"
        
  tags = []
  posted = out_get_article.find('div' ,class_='text-cnn_grey').get_text(strip=True)
  #print(url)
  
  data_set = {
                "domain": "www.cnnindonesia.com",
                "crawling_time": crawling_time ,
                "crawling_time_epoch": crawling_time_epoch,
                "url": url,
                "title": title,
                "categories": categories,
                "article": {
                    "content_url": contain_url,
                    "posted": posted,
                    "media_url": media_url,
                    "tags": tags,
                    "article": article}
                }
  return data_set


def start():   
  if on_off :
    print("Program is running")
  else:
    sys.exit()
  url = "https://www.cnnindonesia.com/indeks/2?page="
  page = 1
  scan_json()  
  breaks = 20    
  while on_off > 0:
    url_page = url + str(page)
    pages = get_page(url+str({page})) 
    if page == 2 :
      print("Loading Crawling. . .") 
    
    for article in pages:
      out_page_url = article.find('a')
      out_page_url = out_page_url['href']
      if out_page_url not in hasil_scan_data:
        if "https" in out_page_url :
          print(out_page_url)
          artikel_mentah = get_article(out_page_url)
          #print(artikel_mentah)
          hasil_mentah = dic_data(artikel_mentah,out_page_url,url_page)
          #print(hasil_mentah)
          add_dic_json(hasil_mentah)
        
        
    if  "90" in out_page_url:
      print("Sedang Crawling. . .") 
    
    
    page = page + 1
    time.sleep(0)


start()