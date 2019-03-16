import requests
import urllib,urllib3
import sys,time
from bs4 import BeautifulSoup

def url_maker(keyword,minPrice,maxPrice):
    url="https://www.kijiji.ca/b-buy-sell/ottawa/"+keyword+"/k0c10l1700185?price="+minPrice+"__"+maxPrice
    return url

def sleepRefresh(sec):
    secc=sec;
    print("Refresh in "+str(sec)+" seconds")
    for i in range(101):
        sys.stdout.write('\r')
        sys.stdout.write("%s%% |%s" %(int(i%101), int(i%101)*'#'))
        sys.stdout.flush()  ##随时刷新到屏幕上
        time.sleep(0.05)
    print ("\n")

list = []
keyword=input("What are u looking for?")
minPrice=input("What is the bottomline of price?")
maxPrice=input("No more than? ")
#response =requests.get()
url=url_maker(keyword,minPrice,maxPrice)
print("Here is the url for u:"+url)
print("Let's get into this.")
user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'
headers={'User-agent':user_agent}
while True:
    response=requests.get(url,headers)
    soup = BeautifulSoup(response.text,'lxml')
    #print(soup)
    productsList = soup.find_all("div",class_="info-container")
    #print(productsList)
    for product in productsList:
        soupP = BeautifulSoup(str(product),'lxml')
        productTitle=soupP.find(class_="title")
        productPricec=soupP.find(class_="price")
        productDescription=soupP.find(class_="description")
        productDate=soupP.find(class_="date-posted")
        productUrl=soupP.find(class_="title").a['href']

        productTitle=str(productTitle.text).strip()
        productPricec=((str((productPricec.text).strip()).replace("$","")).replace(",","")).replace(" ","")
        productPrice=int(productPricec[0:productPricec.find(".")])
        productDescription=str(productDescription.text).strip()
        productDate=str(productDate.text).strip()
        productUrl=str(productUrl).strip()
        if productTitle.find(keyword) != -1:
            if not productDescription in list:
                list.append(productDescription)
                print(productTitle+"\n"+"仅仅只卖:"+str(productPrice)+"\n"+"详情:"+productDescription+"\n"+"在"+productDate+"发售的"+"\n"+"点击查看:"+"https://www.kijiji.ca"+productUrl)
                print("\n\n\n\n")
            else:
                print(productTitle+" is out of date.\n")
    sleepRefresh(5)
