import requests
import re
from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urlparse, urlunparse

#making a bs4 keyword comparison function to see if
#two site urls are associated?
#the percentage of related keywords to be considered related
#links can be changed in this function.
def soup_comparison(soup1, soup2):

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
    if len(common) >= (words_to_compare * .05):
        return True

    return False


# takes in links and makes them beautifulsoup parsed for
# soup_comparison. Is called in place of soup_comparison
# for raw links.
def link_comparison(url1, url2):

    #parses the link into to requests
    response1 = requests.get(url1, timeout=20)
    response2 = requests.get(url2, timeout=20)

    soup1 = 0
    soup2 = 0

    #checks if the response is valid and does a soup parse on it
    if response1.status_code == 200:
        soup1 = BeautifulSoup(response1.text, "html.parser")

    if response2.status_code == 200:
        soup2 = BeautifulSoup(response2.text, "html.parser")

    #calls the soup_comparison() function on it. This checks if the
    #two links keywords are similar. the percentage of related keywords
    #to be considered related links can be changed in this function.
    temp = soup_comparison(soup1, soup2)

    return temp


#takes in a url, checks if it has page increments
#if not, it returns false, and if it does
#it runs it through the predictive url check function
#and if it's a valid url, it returns that and if not
#it returns
def predictive_url(url):

    key_words = {"page_num=", "page", "page-", "p="}

    path = urlparse(url).path
    query = urlparse(url).query
    #print(path)

    for section in ["path", "query"]:

        if section == "path":
            current_section = path
        else:
            current_section = query


        for word in key_words:

            #makes a regular expression to check for when there is a keyword
            #followed directly by any series of numbers
            pattern = re.escape(word) + r"(\d+)"
            match_object= re.search(pattern, current_section)
            #print(pattern)
            #print("Match? ")
            #print(match)

            if match_object:
                #gets the number over and before the current page number.
                next_url_page = int(match_object.group(1)) + 1
                prev_url_page = int(match_object.group(1)) - 1

                #changes the current page count of the path to be one more and one
                #less than the given page count.
                next_url_section = (current_section[:match_object.start(1)]
                                + str(next_url_page) + current_section[match_object.end(1):])
                prev_url_section = (current_section[:match_object.start(1)]
                                + str(prev_url_page) + current_section[match_object.end(1):])
                #print(next_url_path)
                #print(prev_url_path)

                #replaces the path value in urlparse with the newly made
                #path with the updated page count
                if section == "path":
                    next_url = urlunparse(urlparse(url)._replace(path=next_url_section))
                    prev_url = urlunparse(urlparse(url)._replace(path=prev_url_section))
                else:
                    next_url = urlunparse(urlparse(url)._replace(query=next_url_section))
                    prev_url = urlunparse(urlparse(url)._replace(query=prev_url_section))
                #print(next_url)
                #print(prev_url)

                return next_url, prev_url

    return False, False

#takes in the predicted url from the def predictive_url
#and checks if it's a valid url
def predictive_url_check(url):
    next_url, prev_url = predictive_url(url)

    #if the predictive_url() function didn't find any valid
    #page related keywords it will return False, False
    if next_url == False and prev_url == False:
        return False, False

    #gets the generated url(s) and checks for if they are valid
    #returned values get changed to False if they are not.
    response1 = requests.get(next_url, timeout=20)
    response2 = requests.get(prev_url, timeout=20)

    if response1.status_code != 200:
        next_url = False

    if response2.status_code != 200:
        prev_url = False

    #print(next_url, prev_url)

    return next_url, prev_url


#test run for the text comparison
#does the basic response and soup init
#then runs it through the link comparison
#function. True if related. False if not.
url1 = "https://www.scrapethissite.com/lessons/"
url2 = "https://www.scrapethissite.com/pages/"

#temp = link_comparison(url1, url2)
#print(temp)

#test run for a valid page. Should return the page 23 and 25
urltemp = "https://www.scrapethissite.com/pages/forms/?page_num=24"
predictive_url_check(urltemp)