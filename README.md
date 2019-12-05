# Newegg Scraper

This project is designed to scrape the website newegg.com to gather reviews from their most popular product lines, as part of a research project for Professor Hongning at the University of Virginia.

## Usage:
To use, the scraper needs a sub-category from the newegg website and a name for the file, like so
```python
python3 scraper.py https://www.newegg.com/Processors-Desktops/SubCategory/ID-343/Page-1?name=Processors-Desktops&PageSize=96&Order=REVIEWS processor_data
```
The formatting of the link is the most important part of the formatting.  It is important to have the subcategory sorted by "Most Reviews", as opposed to the "Featured Items".  It will also make your life easier to have each page display 96 items opposed to the default of 36.  As you can see both of these parameters are just additions to the end of the link, so once you know which links you need you can just append these onto the end of any query.  **The most important part of the link is the "Page-1?" part at the end of the URL.**  The easiest way to make sure you have a properly formatted link is to:
1. Go to the subcategory you want
2. Change the sorting to "Most Reviews"
3. Change the display per page to "96"
4. Go to **Page 2** to ensure proper format of the link, then *manually* change the "2" to a "1".


I know that this can be a little clunky, but newegg is very picky about how they display their data.

## Other info
After the program has run (it will probably take between 15 minutes to an hour due to the 3 second sleep for every item) it will return *your_file_name*_timestamp.json, so make sure you're not including the file extention in the command arguments.  My initial data is in the *new_data.json* file and statistics about this info can be found in *statistics.txt*.  I used 5 initial subcategories, which happen to be Newegg's 5 most popular: 

-Desktop Graphics Cards
-Computer Cases
-AMD Motherboards
-Intel Motherboards
-Desktop Memory

A good reference for the most popular categories on Newegg can be found at https://www.newegg.com/d/Feedback/Reviews.

Most of the code is well documented, but for future reference if something breaks catestrophically, Newegg has most likely completely changed the formatted something on their end of the project, which happened to me in the middle of my work.  The codebase should hopefully be compartmentalized enough to minimize the number of changes necessary.  Most likely the page with review data has been altered, in which case you will have to change the tags that BeautifulSoup is searching for, most of the other formatting should still work.
