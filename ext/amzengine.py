# amazon_extractor
from bs4 import BeautifulSoup
import requests
import emoji
import nltk
import enchant
import pandas as pd
from dateutil.parser import parse
import numpy as np
#from flask import Flask, render_template, url_for, request
from nltk.corpus import stopwords
import streamlit as st
#nltk.download('stopwords')

from nltk.stem import SnowballStemmer
import pickle
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
#from sklearn.externals import joblib
import string
import time

#"C:\Users\SANTOSH A PATIL\Documents\GitHub\Review_miner"
def getReview_link(s, u):
    if s != "stop":
        cookie = {}
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
        uu = requests.get(u, cookies=cookie, headers=header)
        soup = BeautifulSoup(uu.content, 'html.parser')
        rev = soup.find('div', id="reviews-medley-footer")
        t = rev.find('a').get('href')
        r_u = "https://www.amazon.in" + t + "&sortBy=recent"
        return r_u


def getReviews(url, pg):
    cookie = {}
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

    ur = url + "&pageNumber=" + str(pg) + "&sortBy=recent"
    page = requests.get(ur, cookies=cookie, headers=header)
    r_h = []
    r_b = []
    r_t = []
    r_s = []
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        r = soup.find('div', id="cm_cr-review_list")

        if r == "f":
            return r_h, r_b, r_t,r_s, pg
        else:

            ty = soup.find('div', class_="a-section a-spacing-none review-views celwidget")

            rt = ty.find_all("a", {'data-hook': "review-title"})
            stars=ty.find_all("i",{'data-hook': "review-star-rating"})

            for i in rt:
                if i is None:
                    r_h.append(None)
                else:
                    v = i.get_text()
                    v = v.strip("\n")
                    r_h.append(v)


            for star in stars:

                if star is None:
                    r_s.append(None)
                else:
                    s=star.get_text()
                    s=s.strip(" out of 5 stars")
                    s=float(s)
                    r_s.append(s)


            rb = soup.find_all("span", {'data-hook': "review-body"})
            for i in rb:
                if i is None:
                    r_b.append(None)
                else:
                    v = i.get_text()
                    v = v.strip("\n")
                    r_b.append(v)
            rti = soup.find_all("span", {'data-hook': "review-date"})
            for i in rti:
                if i is None:
                    r_t.append(None)
                else:

                    t = i.get_text()
                    date = parse(t, fuzzy=True, dayfirst=True)
                    r_t.append(date)

            nextp = soup.find("ul", class_="a-pagination")
            npg = 0
            if (nextp.find("li", class_="a-disabled a-last")) is not None:
                return r_h, r_b, r_t,r_s, npg
            elif (nextp.find("li", class_="a-last")) is not None:

                npg = pg + 1
                return r_h, r_b, r_t,r_s, npg


def Review_extract(purl):
                    p=purl
                    #if request.method == 'POST':
                        #product_u= request.form.get('comment')
                        #print(product_u)
                        #message = request.form.get('message')
                        #p = str(product_u)

                    cookie = {}
                    header = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

                    Reviews = pd.DataFrame()
                    page = requests.get(p, cookies=cookie, headers=header)
                    if page.status_code == 200:
                        st = page
                    else:
                        st = "stop"
                    H = []
                    B = []
                    D = []
                    S = []
                    rev_link = getReview_link(st, p)

                    pg = 1
                    ntpg = 1
                    while (pg >= ntpg):

                        #my_bar = st.progress(0)
                        #for percent_complete in range(pg):
                            #time.sleep(0.1)
                            #my_bar.progress(percent_complete + 1)
                        print(pg)
                        r_t = []
                        r_h = []
                        r_b = []
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
                    
                    #Reviews.to_csv("reviews.csv")
                    return Reviews

#def main(url):
#Review_extract(url)

#if __name__ == '__main__':
    #main(ur)
