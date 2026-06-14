import requests
import pandas as pd
from bs4 import BeautifulSoup

URL1 = "https://www.flipkart.com/mobile-phones-store?..."

r = requests.get(URL1)
soup1 = BeautifulSoup(r.content, "html.parser")

company = soup1.find_all("a", {"class": "h1Fvn6"})

for i in range(len(company)):
    company[i] = "https://www.flipkart.com" + company[i]['href']

all_link = []

for com in company:
    r1 = requests.get(com)
    mobile_data = BeautifulSoup(r1.content, "html.parser")
    all_mobile = mobile_data.find_all("a", {"class": "_1fQZEK"})
    
    for i in range(len(all_mobile)):
        all_link.append("https://www.flipkart.com" + all_mobile[i]['href'])

all_mobile_data = []

for i in all_link:
    r2 = requests.get(i)
    mobile_data = BeautifulSoup(r2.content, "html.parser")

    mob_name = mobile_data.find("span", {"class": "B_NuCI"})
    mob_price = mobile_data.find("div", {"class": "_30jeq3 _16Jk6d"})

    highlights = mobile_data.find_all("li", {"class": "_21Ahn-"})
    highlights = [h.text for h in highlights]
    mob_highlight = " ".join(highlights)

    mob_image = mobile_data.find_all("img", {"class": "q6DClP"})
    mob_image = mob_image[0]['src'] if mob_image else None

    all_mobile_data.append([
        mob_name.text if mob_name else None,
        mob_price.text if mob_price else None,
        mob_highlight,
        mob_image
    ])

df = pd.DataFrame(all_mobile_data,
                  columns=["Mobile_name", "Mobile_price", "Mobile_description", "Mobile_image_link"])

df.to_excel("flipkart_mobiles.xlsx", index=False)