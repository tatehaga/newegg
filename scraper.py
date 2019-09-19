#!/usr/bin/python3
import json
import urllib.request
from bs4 import BeautifulSoup
import re
import time


url = "https://www.newegg.com/icicle-gold-asus-zenbook-ux331ua-ds71-mainstream/p/N82E16834234966?Item=N82E16834234966&SortField=0&SummaryType=0&PageSize=10&SelectedRating=-1&VideoOnlyMark=False&IsFeedbackTab=true#scrollFullInfo"
#url = "https://www.newegg.com/dark-royal-blue-asus-zenbook-ux434fl-db77-mainstream/p/N82E16834235238"
url = "https://www.newegg.com/p/N82E16834230663"
category_url = "https://www.newegg.com/Laptops-Notebooks-Laptops-Notebooks/SubCategory/ID-32?Tid=6740&Order=REVIEWS&PageSize=96"

def getCategoryAndUrls(category_url):
    urls = []
    with urllib.request.urlopen(category_url) as read_file:
        soup = BeautifulSoup(read_file, "html.parser")
    category = soup.find("h1", {"class":"page-title-text"}).contents
    item_listing = soup.find_all("a", {"class":"item-title"})
    for item in item_listing:
        urls.append(item.get('href'))
    return category[0], urls


def pageReviews(url):
    subdata = {}
    with urllib.request.urlopen(url) as read_file:
        soup = BeautifulSoup(read_file, "html.parser")
    try:
        review_count = soup.find_all("span", {"itemprop":"reviewCount"})[0].contents[0]
    except:
        review_count = 0
    reviews = soup.find_all("div", {"itemprop":"review"})
    item = soup.find("input", {"id":"persMainItemNumber"}).get('value')
    print(item)
    subdata[item] = []
    for review in reviews:
        try:
            title = review.find("span", {"itemprop":"name"}).contents[0]
        except:
            title = ""
        rating = review.find("span", {"itemprop":"ratingValue"}).contents[0]
        PublishDate = review.find("span", {"itemprop":"datePublished"}).contents[0]
        LoginNickname = review.find("div", {"itemprop":"author"}).contents[0]
        pros_cons_review = review.find_all("strong")
        try:
            boughttime = review.find("div", {"class":"comments-text"}).contents[0]
            boughttime = boughttime.split(' ',1)[1]
        except:
            boughttime = ""
        if LoginNickname != "Anonymous":
            author = LoginNickname.text.strip()
        else:
            author = "Anonymous"
        try:
            owner = review.find("div", {"class":"comments-text comments-verified-owner"}).contents[0]
            verified = True
        except:
            verified = False
        pros, cons, review_text = "", "", ""
        for i in range(len(pros_cons_review)):
            if pros_cons_review[i].text == "Pros:":
                pros = pros_cons_review[i].next_sibling.strip()
            elif pros_cons_review[i].text == "Cons:":
                cons = pros_cons_review[i].next_sibling.strip()
            elif pros_cons_review[i].text == "Overall Review:":
                review_text = pros_cons_review[i].next_sibling.strip()
        numbers = review.find_all("span", {"class":"comments-text"})
        votes = re.findall(r"[\d]+\w* out of \w*[\d]+", str(numbers))
        if votes != []:
            matches = re.findall("(\d+)", votes[0])
            consented = matches[0]
            voted = matches[1]
        else:
            consented = 0
            voted = 0
        subdata[item].append({
            'Title': title,
            'Rating': int(rating),
            'PublishDate': PublishDate,
            'Author': author,
            'BoughtTimeTypeString': boughttime,
            'PurchaseMark': verified,
            'Cons': cons,
            'Pros': pros,
            'Comments':review_text,
            'VotesFor': consented,
            'VotesTotal': voted
        })

    return item, subdata

category, urls = getCategoryAndUrls(category_url)
data = {}
dataentry = {}
for url in urls:
    itemno, dataset = pageReviews(url)
    dataentry.update(dataset)
    time.sleep(5)
data[category] = dataentry
with open('data.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)