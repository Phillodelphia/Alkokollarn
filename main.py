import url_parser as up
import requests as req
from requests import Session
import json
import os

base_url = "https://www.systembolaget.se"
sub_url = "https://www.systembolaget.se/sortiment/"
api_url = "https://api-extern.systembolaget.se/sb-api-ecommerce/v1/productsearch/search"

with open("api_key.json", "r") as f:
    api_key = json.load(f)


def fetch_products_from_api():
    '''Fetches all products from systembolagets sortiment '''

    with Session() as s:
        query_string = "?page=1&size=30&sortBy=Score&sortDirection=Ascending"
        product_list = {}
        s.get(base_url)
        r = s.get(api_url+query_string, headers=api_key)
        first_page = r.json()
        for i in range(first_page['metadata']['totalPages']+1):
            query_string = "?page=" + str(i) + "&size=30&sortBy=Score&sortDirection=Ascending"
            r = s.get(api_url+query_string, headers=api_key)
            product_list = { "product": r.json()["products"] }
            with open("products/prod_pages_"+str(i)+".json", "w") as f:
                json.dump(product_list,f)

def search_for_article(art_num):
    '''Once the product data exists, search for a article number'''

    prod = os.listdir("./products")
    for i in prod:
        with open("./products/"+str(i), "r") as f:
            j = json.load(f)
            for prod in j["product"]:
                if art_num == int(prod["productNumberShort"]):
                    
                    print(f"articlenumber found! Located in ./products/{str(i)}")
                    print(f"Articlenumber: {prod["productNumberShort"]} | Product name is: {prod["productNameBold"]} {prod["productNameThin"]}")

def search_top_ascending():
    '''Once the product data exists, sort the data to top 30 article numbers'''

    prod = os.listdir("./products")
    listed = {}
    for i in prod:
        with open("./products/"+str(i), "r") as f:
            j = json.load(f)
            for prod in j["product"]:
                if 30 >= int(prod["productNumberShort"]):
                    listed[int(prod['productNumberShort'])] = prod
    for key, prod in sorted(listed.items()):
        print(f"Articlenumber: {key} | Product name is: {prod["productNameBold"]} {prod["productNameThin"]}")

search_for_article(1)
search_top_ascending()

# Use when fetch is needed
#fetch_products_from_api()
#print("product data fetched")
