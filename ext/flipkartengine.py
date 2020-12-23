
import time
import re
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
from datetime import datetime,timedelta
from dateutil.parser import parse

def getReview_link(s, u):
            if s != "stop":
                cookie = {}
                header = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
                uu = requests.get(u, cookies=cookie, headers=header)
                soup = BeautifulSoup(uu.content, 'html.parser')
                error="go"
                rev=soup.find('div',class_="_2c2kV-")
                rev=rev.find_next_sibling("a").get("href")
                rev_link="https://www.flipkart.com"+rev+"&aid=overall&certifiedBuyer=false&sortOrder=MOST_RECENT"
                nm=soup.find('h1',class_="yhB1nd")
                p_name=nm.find("span").get_text()
                return rev_link,p_name,error

                #except:
                  #rev_link="not_available"
                  #p_name="not_available"
                  #error="error"
                  #return rev_link,p_name,error

def getReviews(url, pg):
    cookie = {}
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

    ur = url + "&page=" + str(pg)
    try:
        page = requests.get(ur, cookies=cookie, headers=header)
        r_h = []
        r_b = []
        r_t = []
        r_s = []
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            r="g"
            if r == "f":
                return r_h, r_b, r_t,r_s, pg
            else:

                rt = soup.find_all("p", class_= "_2-N8zT")

                for i in rt:
                    if i is None:
                        r_h.append(None)
                    else:
                        v = i.get_text()
                        r_h.append(v)
                rb = soup.find_all("div",class_="t-ZTKy")

                for i in rb:
                    if i is None:
                        r_b.append(None)
                    else:
                        v = i.get_text()
                        v = v.strip("READ MORE")
                        r_b.append(v)
                dt = soup.find_all("p", class_= "_2sc7ZR")
                for i in range(len(dt)):
                    if dt[i] is None:
                        r_t.append(None)
                    else:
                        if i%2==0:
                          continue
                        else:
                          v=dt[i].get_text()
                          r_t.append(v)

                rs = soup.find_all("div", class_= "_3LWZlK")
                for i in rs:
                    if i is None:
                        r_s.append(None)
                    else:
                        if i is None:
                          r_s.append(None)
                        else:
                          v=i.get_text()
                          r_s.append(v)
                del r_s[0]

                nextp=[]
                netp = soup.find_all("a", class_="_1LKTO3")
                for i in netp:
                    g=i.find("span")
                    if g is None:
                        nextp.append(None)
                    else:
                        nextp.append(g.get_text())

                npg = 0
                if pg==1 and nextp[0]=="Next":
                  npg = pg + 1
                  return r_h, r_b, r_t,r_s, npg
                elif pg!=1 and nextp[0]=="Previous":
                  if len(nextp)==2:
                    npg = pg + 1
                    return r_h, r_b, r_t,r_s, npg
                  else:
                    return r_h, r_b, r_t,r_s, npg
    except ConnectionError:
        npg=0
        return r_h, r_b, r_t,r_s, npg



def ago_do_date(ago):
    if "day" in ago:
      if "Today" in ago:
        d = datetime.today()
        return(d.strftime('%Y-%m-%d'))
      elif "days" in ago:
        a=int(ago.strip(" days ago"))
        d = datetime.today() - timedelta(days=a)
        return(d.strftime('%Y-%m-%d'))
      else:
        a=int(ago.strip(" day ago"))
        d = datetime.today()- timedelta(days=1)
        return(d.strftime('%Y-%m-%d'))

    elif "month" in ago:
      if "months" in ago:
        a=int(ago.strip(" months ago"))
        d = datetime.today() - timedelta(days=a*30)
        return(d.strftime('%Y-%m-%d'))

      else:
        a=int(ago.strip(" month ago"))
        d = datetime.today() - timedelta(days=a*30)
        return(d.strftime('%Y-%m-%d'))
    else:
      dt = parse(ago)
      return(dt.strftime('%Y-%m-%d'))

def Review_extract(purl):
                    p=purl
                    #if request.method == 'POST':
                        #product_u= request.form.get('comment')
                        #print(product_u)
                        #message = request.form.get('message')
                        #p = str(product_u)
                    print("enterd")
                    cookie = {}
                    header = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

                    Reviews = pd.DataFrame()
                    page = requests.get(p, cookies=cookie, headers=header)

                    if page.status_code == 200:
                        st = "GO"
                    else:
                        st = "stop"
                    H = []
                    B = []
                    D = []
                    S = []
                    rev_link,prd_name,error = getReview_link(st, p)
                    error="go"
                    if rev_link=="not_available":
                        error="error"

                    else:
                        pg = 1
                        ntpg = 1
                        while (pg >= ntpg):
                            print(pg)

                            r_h = []
                            r_b = []
                            r_t = []
                            r_s = []
                            r_h, r_b, r_t,r_s, ntpg = getReviews(rev_link, pg)

                            H.extend(r_h)
                            B.extend(r_b)
                            D.extend(r_t)
                            S.extend(r_s)
                            if ntpg > pg:
                                pg = ntpg
                                continue
                            else:
                                break

                    Reviews = pd.DataFrame(({"Review_title": H,
                                                 "Review_body": B,
                                                 "Review_rating":S,
                                                 "Review_date": D}))
                    Reviews["Review_rating"]= pd.to_numeric(Reviews["Review_rating"])
                    Reviews["Review_date"]=Reviews["Review_date"].apply(ago_do_date)
                    Reviews.to_csv("reviews_fkart.csv")
                    return Reviews,prd_name,error
