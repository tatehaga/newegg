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
category_111 = "https://www.newegg.com/Laptops-Notebooks-Laptops-Notebooks/SubCategory/ID-32/Page-2?Tid=6740&Order=REVIEWS&PageSize=96"
graphics_url = "https://www.newegg.com/Desktop-Graphics-Cards-Desktop-Graphics-Cards/SubCategory/ID-48/Page-1?Order=REVIEWS&PageSize=96"
test_url = "https://www.newegg.com/zotac-geforce-gtx-1060-zt-p10620a-10m/p/N82E16814500454"
cases_url = "https://www.newegg.com/Computer-Cases/SubCategory/ID-7/Page-1?Order=REVIEWS&PageSize=96"

def getPagesfromCategory(category_url):
    urls = []
    end = False
    count = 1
    split_link = category_url.rsplit('1',1)
    print(split_link)
    with urllib.request.urlopen(category_url) as read_file:
        soup = BeautifulSoup(read_file, "html.parser")
    category = soup.find("h1", {"class":"page-title-text"}).contents
    review_counts = soup.find_all("span", {"class":"item-rating-num"})
    while not end:
        split_link = category_url.rsplit('1',1)
        new_link = split_link[0] + str(count) + split_link[1]
        with urllib.request.urlopen(new_link) as read_file:
            soup = BeautifulSoup(read_file, "html.parser")
        review_counts = soup.find_all("span", {"class":"item-rating-num"})
        for i in range(len(review_counts)):
            #print(review_counts[i].contents[0][1:-1])
            if int(review_counts[i].contents[0][1:-1].replace(',','')) <= 2:
                end = True
        urls.append(new_link)
        count+=1
    return urls

        
        
            
    
    
    

def getCategoryAndUrls(category_url):
    urls = []
    with urllib.request.urlopen(category_url) as read_file:
        soup = BeautifulSoup(read_file, "html.parser")
    category = soup.find("h1", {"class":"page-title-text"}).contents
    item_listing = soup.find_all("a", {"class":"item-title"})
    for item in item_listing:
        urls.append(item.get('href'))
    return category[0], urls


def newReviews(url):
    subdata = {}
    item = url.rsplit('/', 1)[1]
    print(item)
    with urllib.request.urlopen(url) as read_file:
        soup = BeautifulSoup(read_file, "html.parser")
    #print(soup.prettify())
    comments = soup.find_all("div", {"class":"comments-cell has-side-left is-active"})
    review_count = len(comments)
    subdata[item] = []
    for comment in comments:
        try:
            title = str(comment.find("span", {"class":"comments-title-content"}).contents[0])
        except:
            title = ""
        rating = int(comment.find("span").contents[0])
        publish_date = comment.find("span", {"class":"comments-text comments-time comments-time-right"}).get('content')
        author = comment.find("div", {"class":"comments-name"}).contents[0]
        pros_cons_review = comment.find_all("strong")
        if author != "Anonymous":
            author = str(author.contents[0])
        else:
            author == "Anonymous"
        try:
            author_id = str(comment.find("a").get('href').rsplit('/',1)[1])
        except:
            author_id = ""
        try:
            boughttime = str(comment.find("div", {"class":"comments-text"}).contents[0])
        except:
            boughttime = ""
        try:
            owned = comment.find("div", {"class":"comments-text comments-verified-owner"})
            purchased = True
        except:
            purchased = False
        pros, cons, review_text = "", "", ""
        for i in range(len(pros_cons_review)):
            if pros_cons_review[i].text == "Pros:":
                pros = pros_cons_review[i].next_sibling.strip()
            elif pros_cons_review[i].text == "Cons:":
                cons = pros_cons_review[i].next_sibling.strip()
            elif pros_cons_review[i].text == "Overall Review:":
                review_text = pros_cons_review[i].next_sibling.strip()
        new_auth = str(author)
        subdata[item].append({
            'Title': title,
            'Rating': int(rating),
            'PublishDate': str(publish_date),
            'Author': new_auth,
            'AuthorID': str(author_id),
            'BoughtTimeTypeString': str(boughttime),
            'PurchaseMark': purchased,
            'Cons': str(cons),
            'Pros': str(pros),
            'Comments': str(review_text),

        })
        #print(subdata)

    return str(item), subdata
    

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
    print(url)
    print(item, review_count)
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


#itemno, dataset = newReviews(test_url)

my_urls = getPagesfromCategory(cases_url)
data = {}
dataentry = {}
all_links = []

for num in my_urls:
    category, urls = getCategoryAndUrls(num)
    for link in urls:
        all_links.append(link)
    #all_links.append(urls)
print(category + ": " + str(len(all_links)))
#print(all_links)


data = {}
dataentry = {}
for url in all_links:
    print(url)
    itemno, dataset = newReviews(url)
    dataentry.update(dataset)
    time.sleep(3)
"""
category, urls = getCategoryAndUrls(graphics_url)
category = "Desktop Graphics Cards"
print(type(category))
data = {}
dataentry = {}
for url in urls:
    print(url)
    itemno, dataset = newReviews(url)
    dataentry.update(dataset)
    time.sleep(3)
"""
data[str(category)] = dataentry

with open('data_cases.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
