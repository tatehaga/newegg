#!/usr/bin/python3
import json
import urllib.request
from bs4 import BeautifulSoup
import re
import time
import sys

"""
This application is split into three major pieces of functionality:
getPagesfromCategory, getCategoryAndUrls, and newReviews.

getPagesfromCategory takes a Newegg subcategory link, and generates 
list of all pages in that subcategory until a page with some "n" 
number of reviews is reached, in this case n=2

getCategoryAndUrls takes an individual page with multiple items on it
(the output of getPagesfromCategory) and returns the subcategory of
items as well as a list of links to each item on the page

newReviews takes the url to any given item and returns the item id and a dictionary
object with the information about the object, including all its reviews
Note: During development, Newegg changed the way you viewed reviews from being a part of
the static html to a dynamic javascript loading, so for most pages, you only are able
to access the first 8 or so reviews on a page, sorry.  Also, for some reason there are lots
of items on Newegg that have reviews but these reviews aren't available.  I don't quite understand why.

Example url:
"https://www.newegg.com/Processors-Desktops/SubCategory/ID-343/Page-1?name=Processors-Desktops&PageSize=96&Order=REVIEWS"
"""


if len(sys.argv) != 3:
    print("Invalid command, run command as scraper.py *link to sub-category* *output_file with no file extention*")
    sys.exit()

subcategory_url = sys.argv[1]
output = sys.argv[2]



def getPagesfromCategory(category_url):
    urls = []
    end = False
    count = 1
    # split url over page number, should be page one according to specs
    split_link = category_url.rsplit('1',1)
    with urllib.request.urlopen(category_url) as read_file:
        soup = BeautifulSoup(read_file, "html.parser")
    review_counts = soup.find_all("span", {"class":"item-rating-num"})
    while not end:
        split_link = category_url.rsplit('1',1)
        new_link = split_link[0] + str(count) + split_link[1]
        with urllib.request.urlopen(new_link) as read_file:
            soup = BeautifulSoup(read_file, "html.parser")
        review_counts = soup.find_all("span", {"class":"item-rating-num"})
        for i in range(len(review_counts)):
            if int(review_counts[i].contents[0][1:-1].replace(',','')) <= 2:
                end = True
        urls.append(new_link)
        count+=1
    return urls

        
        
            
    
    
    

def getCategoryAndUrls(category_url):
    urls = []
    # open file
    with urllib.request.urlopen(category_url) as read_file:
        soup = BeautifulSoup(read_file, "html.parser")
    # find category in html object
    category = soup.find("h1", {"class":"page-title-text"}).contents
    item_listing = soup.find_all("a", {"class":"item-title"})
    #put all links in the item list
    for item in item_listing:
        urls.append(item.get('href'))
    return category[0], urls


def newReviews(url):
    subdata = {}
    # get item number from url, a bit clunky but the simplest way after newegg changes
    item = url.rsplit('/', 1)[1]
    with urllib.request.urlopen(url) as read_file:
        soup = BeautifulSoup(read_file, "html.parser")
    # find comments and put into comments list object
    comments = soup.find_all("div", {"class":"comments-cell has-side-left is-active"})
    # make entry for items with no reviews
    subdata[item] = []
    for comment in comments:
        # try and get title from comment, not necessary hense the try/except, maybe not best form
        try:
            title = str(comment.find("span", {"class":"comments-title-content"}).contents[0])
        except:
            title = ""
        # get rating, publish date, author - all required but author could be anonymous
        rating = int(comment.find("span").contents[0])
        publish_date = comment.find("span", {"class":"comments-text comments-time comments-time-right"}).get('content')
        author = comment.find("div", {"class":"comments-name"}).contents[0]
        # set author if anonymous due to funky formatting by newegg and the name otherwise
        if author != "Anonymous":
            author = str(author.contents[0])
        else:
            author == "Anonymous"
        # find the identifying author id, only exists if author is not anonymous
        try:
            author_id = str(comment.find("a").get('href').rsplit('/',1)[1])
        except:
            author_id = ""
        # find when the author purchased the item, not a required field            
        try:
            boughttime = str(comment.find("div", {"class":"comments-text"}).contents[0])
        except:
            boughttime = ""
        # try to find if the owner is verified, owned is a necessary variable, fails if
        # the purchase is verified
        try:
            owned = comment.find("div", {"class":"comments-text comments-verified-owner"})
            purchased = True
        except:
            purchased = False
        # gather list object of pros, cons, and review comments, can be all, some, or none of the above
        pros_cons_review = comment.find_all("strong")
        pros, cons, review_text = "", "", ""
        # iterate through the pros, cons, and comments find which exst and add those to the end dictionary object
        for i in range(len(pros_cons_review)):
            if pros_cons_review[i].text == "Pros:":
                pros = pros_cons_review[i].next_sibling.strip()
            elif pros_cons_review[i].text == "Cons:":
                cons = pros_cons_review[i].next_sibling.strip()
            elif pros_cons_review[i].text == "Overall Review:":
                review_text = pros_cons_review[i].next_sibling.strip()
        
        # author was a *really* weird field, gave me lots of trouble, this fixes it
        new_auth = str(author)

        # format data for addition to the json file
        if new_auth == "Anonymous":
            author_id = ""
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

    return str(item), subdata
    

# begin main function

my_urls = getPagesfromCategory(subcategory_url)
all_links = []

for num in my_urls:
    category, urls = getCategoryAndUrls(num)
    for link in urls:
        all_links.append(link)

data = {}
dataentry = {}
for url in all_links:
    print(url)
    itemno, dataset = newReviews(url)
    dataentry.update(dataset)
    ############################
    # 3 second sleep is ABSOLUTELY NECESSARY, any faster and you WILL get a short IP ban
    ############################
    time.sleep(3)

data[str(category)] = dataentry
output_with_timestamp = str(output) + str(time.time()) + ".json"
with open(output_with_timestamp, 'w') as outfile:
    json.dump(data, outfile, indent=4)
