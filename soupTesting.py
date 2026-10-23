import requests
from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urlparse

#making a bs4 keyword comparison function to see if
#two site urls are associated?
def link_comparison(soup1, soup2):

    words_to_compare = 20

    #filter words to be removed from any comparisons.
    #words can be added freely to the filter words list
    #but must be lowercase.
    filter_words = [ "the", "a", "to", "and", "or", "and", "but",
                     "in", "that", "this", "of", "with", "for",
                     "was", "were", "am", "is", "are", "it", "from",
                     "has", "|"]

    #These have all words in a long list
    soup1_contents = soup1.get_text().split()
    soup2_contents = soup2.get_text().split()
    #print(soup1_contents)

    #made to store all words in a list that has filter_words removed.
    soup1_contents_filtered = []
    soup2_contents_filtered = []

    #filtering soup contents
    #.lower() is for in case a common word starts a sentence
    #and is capitalized oddly.
    #also removes periods
    for text in soup1_contents:
        if text.lower() not in filter_words:
            soup1_contents_filtered.append(text.replace(".", ""))

    for text in soup2_contents:
        if text.lower() not in filter_words:
            soup2_contents_filtered.append(text.replace(".", ""))
    #print(soup1_contents_filtered)

    #counts the amount of times each word shows up
    soup1_count = Counter(soup1_contents_filtered)
    soup2_count = Counter(soup2_contents_filtered)
    #print(soup1_count)

    #gets the most common amount of words
    soup1_most_common = soup1_count.most_common(words_to_compare)
    soup2_most_common = soup2_count.most_common(words_to_compare)
    #print(soup1_most_common)

    #list for removing counts
    soup1_common_set = set()
    soup2_common_set = set()

    #loop removes the counts and only saves the most common
    #words for later comparison
    for text, count in soup1_most_common:
        soup1_common_set.add(text)

    for text, count in soup2_most_common:
        soup2_common_set.add(text)

    #testing
    #print(soup1_common_set)
    #print(soup2_common_set)

    #gets the words in common between the sets
    common = soup1_common_set & soup2_common_set

    #print(common)
    #print(len(common))

    #Checks if more than half of the most popular word are in common
    #returns True indicating the urls are related.
    if len(common) >= (words_to_compare * .2):
        return True

    return False

#takes in a url, checks if it has page increments
#if not, it returns false, and if it does
#it runs it through the predictive url check function
#and if it's a valid url, it returns that and if not
#it returns
###############################
#finish building
def predictive_url(url):

    key_words = {"page", "page-", "p=", "="}

    path = urlparse(url).path
    #print(path)

    for word in key_words:
        if word in path:
            #figure out how to increment the page
            #print("True")
            return True

    return False

#takes in the predicted url from the def predictive_url
#and checks if it's a valid url
##################################3
#finish building
def predictive_url_check(url):
    return


#test run for the text comparison
#does the basic response and soup init
#then runs it through the link comparison
#function. True if related. False if not.
url1 = "https://www.scrapethissite.com/lessons/"
url2 = "https://www.scrapethissite.com/pages/"

response1 = requests.get(url1, timeout = 20)
response2 = requests.get(url2, timeout = 20)

soup1 = 0
soup2 = 0

if response1.status_code == 200:
    soup1 = BeautifulSoup(response1.text, "html.parser")

if response2.status_code == 200:
    soup2 = BeautifulSoup(response2.text, "html.parser")

temp = link_comparison(soup1, soup2)
#print(temp)

#this is not a real url
urltemp = "https://www.scrapethissite.com/lessons/p=1"
predictive_url(urltemp)