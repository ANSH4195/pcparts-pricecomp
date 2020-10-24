import requests
from bs4 import BeautifulSoup
from time import sleep
import re

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'})


def search_kharidiye(search_for):
    data = []

    search = search_for.replace(" ", "+").lower()
    search_for = list(search_for.lower().split())

    khrd_url = f"https://www.kharidiye.com/?s={search}&post_type=product"

    page = requests.get(khrd_url, headers=headers)
    soup = BeautifulSoup(page.content, features='lxml')

    if(soup.find(class_="woocommerce-info") != None):
        return None

    if(soup.find(class_="entry-summary")):
        d = {}

        title = str(soup.find(class_="entry-title").text)

        title = re.sub(r'\([^)]*\)', '', title)

        d["name"] = title.replace(
            "-", "").replace("®", "").replace("™", "").upper()

        price = str(
            soup.find(class_="electro-price").ins.span.bdi.text).replace(".00", "").replace(",", "").replace("₹", "")
        d["price"] = price

        d["link"] = khrd_url

        data.append(d)
    else:
        for info in soup.find_all("div", {"class", "product-inner"}):
            d = {}

            title = str(info.find(
                class_="woocommerce-loop-product__title").text).replace("-", " ").replace("®", "").replace("™", "").lower()
            title = re.sub(r'\([^()]*\)', '', title)

            if all(x in title for x in search_for):

                d["name"] = title.upper()

                price = str(
                    info.find(class_="woocommerce-Price-amount amount").bdi.text)
                d["price"] = int(price.replace(
                    ".00", "").replace("₹", "").replace(",", ""))

                d["link"] = soup.find(
                    class_="woocommerce-LoopProduct-link woocommerce-loop-product__link")['href']
            else:
                continue

            data.append(d)

    data = sorted(data, key=lambda k: k['price'])

    return data


def search_mdcomputers(search_for):
    data = []
    search = search_for.replace(" ", "+").lower()
    search_for = list(search_for.lower().split())

    url = f"https://mdcomputers.in/index.php?category_id=0&search={search}&submit_search=&route=product%2Fsearch"

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, features='lxml')

    if(str(soup.find(id="content").p.text.lower())
       == "your shopping cart is empty!"):
        return None

    for info in soup.find_all("div", {"class", "product-item-container"}):
        d = {}

        title = str(info.find(class_="right-block right-b").h4.a.text).replace("-", " ").replace("®", "").replace("™", "").lower()  # nopep8
        title = re.sub(r'\([^)]*\)', '', title)

        if all(x in title for x in search_for):
            d["name"] = title.upper()

            price = str(
                info.find(class_="price-new").text).replace("₹", "")

            d["price"] = int(price.replace(",", ""))

            d["link"] = soup.find(
                class_="right-block right-b").h4.a['href']
        else:
            continue

        data.append(d)

    data = sorted(data, key=lambda k: k['price'])

    return data


def search_prime(search_for):
    data = []
    search = search_for.replace(" ", "+").lower()
    search_for = list(search_for.lower().split())

    url = f"https://www.primeabgb.com/?post_type=product&taxonomy=product_cat&s={search}"

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, features='lxml')

    if(soup.find(class_="woocommerce-info") != None):
        print(None)
        return

    for info in soup.find_all("div", {"class", "equal-elem"}):
        d = {}

        title = str(info.find(class_="product-name short").a.text).replace("-", " ").replace("®", "").replace("™", "").lower()  # nopep8
        title = re.sub(r'\([^)]*\)', '', title)

        if all(x in title for x in search_for):
            d["name"] = title.upper()

            if(info.find(class_="woocommerce-Price-amount amount")):
                price = str(
                    info.find_all(class_="woocommerce-Price-amount amount")[1].text).replace("₹", "")
                d["price"] = int(price.replace(",", ""))
            else:
                d["price"] = 999999999

            d["link"] = soup.find(
                class_="product-name short").a['href']
        else:
            continue

        data.append(d)

    data = sorted(data, key=lambda k: k['price'])

    for entry in data:
        if entry['price'] == 999999999:
            entry['price'] = 'NA'

    return data
