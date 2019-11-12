#!/usr/bin/python3
import json
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time

browser = webdriver.Firefox()
browser.get('https://www.newegg.com/zotac-geforce-gtx-1060-zt-p10620a-10m/p/N82E16814500454')
reviews = []

