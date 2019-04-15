from cqhttp import CQHttp
import requests
import urllib,urllib3
import sys,time
from bs4 import BeautifulSoup


list = []
working={}

def sleepRefresh(sec,context):
    secc=sec;
    print("Refresh in "+str(sec)+" seconds")
    for i in range(101):
#        print(working[str(context["user_id"])])
        if working[str(context["user_id"])]!=True:
            return
        sys.stdout.write('\r')
        sys.stdout.write("%s%% |%s" %(int(i%101), int(i%101)*'#'))
        sys.stdout.flush()
        time.sleep(0.01*sec)
    print ("\n")

def kijijian(keyword,minPrice,maxPrice,context):
    #response =requests.get()
    working[str(context["user_id"])]=True
    url=url_maker(keyword,minPrice,maxPrice)
    #bot.send(context,url)
    print("Here is the url for u:"+url)
    print("Let's get into this.")
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'
    headers={'User-agent':user_agent}
    while working[str(context["user_id"])]:
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
            if productDate!=None:
                productDate=str(productDate.text).strip()
            else:
                productDate="Not Given"
            productUrl=str(productUrl).strip()
            if productTitle.find(keyword) != -1:
                if not productDescription in list:
                    list.append(productDescription)
                    print(productTitle+"\n"+str(productPrice)+"\n"+productDescription+"\n"+productDate+"\n")
                    print("\n\n\n\n")
                    bot.send(context,productTitle+"\n"+"Price:"+str(productPrice)+"\n"+"Info:"+productDescription+"\n"+"updated at:"+productDate+"\n"+"Click here to take a look"+"https://www.kijiji.ca"+productUrl)
                else:
                    print(productTitle+" is out of date.\n")
    #    time.sleep(5)
        sleepRefresh(600,context)
    bot.send(context,"Kijijian has been Stoped!")
    list.clear()
    return

def url_maker(keyword,minPrice,maxPrice):
    url="https://www.kijiji.ca/b-buy-sell/ottawa/"+keyword+"/k0c10l1700185?price="+minPrice+"__"+maxPrice
    return url



bot = CQHttp(api_root='http://127.0.0.1:5700/',
             access_token='123',
             secret='abc')


@bot.on_message()
def handle_msg(context):
    if "kijijian" in context['message']:
        mess=context['message']
        agrr=mess.split()
        proKeyword=agrr[1]
        proMinPr=agrr[2]
        proMaxPr=agrr[3]
        megg="keyword:"+proKeyword+" MinPrice:"+proMinPr+" MaxPrice:"+proMaxPr
        bot.send(context,megg)
        kijijian(proKeyword,proMinPr,proMaxPr,context)
    if context['message'] == "Working?":
        bot.send(context,"works!")
    if context['message'] == "stopkja":
        working[str(context["user_id"])]=False
    return

bot.run(host='127.0.0.1', port=8080)
