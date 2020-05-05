import os
import time
from glob import glob
from urllib.request import urlopen
from urllib.request import Request
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

def make_headers():
    headers = {}
    headers["User-Agent"] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"
    return headers

def make_request(page):
    req = Request(url.format(page=page), headers=make_headers())
    html = urlopen(req).read().decode("utf-8")
    return html

def get_last_page():
    page = "https://pkgs.alpinelinux.org/packages?branch=edge&arch=armv7"
    html = make_request(page)
    soup = BeautifulSoup(html, "html.parser")
    pagination = soup.find("div", {"id": "pagination"})
    list_items = pagination.findAll("a")
    list_item = list_items[-1]
    href = list_item.get("href")
    last_page = int(href.split("page=")[-1].split("&")[0])
    return last_page

def make_soup(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(attrs={"class": "table-responsive"})
    a = table.findAll(name="a")
    elements = {}
    for elem in ["license", "branch", "repo", "arch", "maintainer", "bdate"]:
        elements[elem] = table.findAll(attrs={"class": elem})
    return a, elements

def parse_a(a):
    ind = 0
    for i, j, k in zip(range(0, len(a)-1, 3), range(1, len(a), 3), range(2, len(a)+1, 3)):
        df.loc[ind, "description"] = a[i]["aria-label"]
        df.loc[ind, "pkg_url"] = a[i]["href"]
        df.loc[ind, "name"] = a[i].string
        df.loc[ind, "version"] = a[j].string
        df.loc[ind, "alpine_url"] = a[k]["href"]
        ind += 1
    pass

def parse_elements(elements):
    for elem in elements:
        for i in range(len(elements[elem])):
            df.loc[i, elem] = elements[elem][i].string
    pass

def unite_files():
    df = pd.DataFrame()
    files = glob("csvs/*.csv")
    for file in tqdm(files, desc="file"):
        temp = pd.read_csv(file, sep=";")
        df = pd.concat([df, temp], ignore_index=True)
    df.to_csv("data.csv", sep=";", index=False)
    pass

def clean_files():
    files = glob("csvs/*.csv")
    for file in tqdm(files, desc="deleting"):
        os.remove(file)
    os.rmdir("csvs/")
    pass

if __name__ == "__main__":
    os.makedirs("csvs", exist_ok=True)
    url = "https://pkgs.alpinelinux.org/packages?page={page}&branch=edge&arch=armv7"
    last_page = get_last_page()
    for i in tqdm(range(1, last_page + 1), desc="scrapping"):
        df = pd.DataFrame()
        html = make_request(page=i)
        a, elements = make_soup(html)
        parse_a(a)
        parse_elements(elements)
        df.to_csv("csvs/"+str(i)+".csv", sep=";", index=False)
        time.sleep(1)
    unite_files()
    clean_files()
