import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.mime.text import MIMEText

headers = {"User-Agent": "Mozilla/5.0","Accept-Language": "en-US,en;q=0.9"}

url=os.getenv("Apple_earphones_url")
email=os.getenv("email")
password=os.getenv("password")
response=requests.get(url=url,headers=headers)
print(response.status_code)
contents=response.text

soup=BeautifulSoup(contents,"html.parser")
price_tag = soup.select_one(".a-price-whole")
if price_tag:
    price = float(
        price_tag.get_text().replace(",", "")
    )
    print(price)
else:
    print("Price not found")
    exit()
title=soup.find(name="span",id="productTitle",class_="a-size-large product-title-word-break").get_text()

BUY_PRICE=2000
#title = soup.find(id="productTitle").get_text()
if price<BUY_PRICE:
    html=f"""   <h2>Price Dropped</h2>
                <p>{title} price has dropped below {BUY_PRICE}</p>
                <a href={url}>Open Product</a>"""
    message=MIMEText(html,"html","utf-8")
    message["subject"]="Price Check Alert"
    with smtplib.SMTP(host="smtp.gmail.com",port=587) as connection:
        connection.starttls()
        connection.login(user=email,password=password)
        connection.sendmail(from_addr=email,to_addrs="bhavyasripilla05@gmail.com",
                            msg=message.as_string().encode("utf-8"))
