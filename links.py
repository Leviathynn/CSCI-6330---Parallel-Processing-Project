#Description: Function .py to avoid clutter in main
#contains get_links to get the data and associated links to
#a given url and history_print to print sites retrieved in
#a tree format

#imports
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


#Linked List initialization so linked lists can be used
#Node for nodes of the linked list
class Node:

    def __init__(self, url, parent, depth):
        self.url = url
        self.parent = parent
        self.depth = depth
        self.next = None

#LinkedList class
#contains a base initialization, append, insert, printLList and
#printTest for debugging
class LinkedList:

    def __init__(self):
        self.head = None

    #append adds a node to the end of the linked list
    def append(self, url, parent, depth):
        new_Node = Node(url, parent, depth)

        #makes the new node the head if there is no head
        if self.head is None:
            self.head = new_Node

        #if there is a head, the temp variable will go to the
        #end of the list and add the node
        else:
            temp = self.head

            while temp.next:
                temp = temp.next
            temp.next = new_Node

    #insert adds a node right behind where it's parent node is
    #it is made like this for printing formatting
    def insert(self, url, parent, depth):
        new_Node =  Node(url, parent, depth)

        #makes the new node the head if there is no head
        if self.head is None:
            self.head = new_Node

        #if not the head, it checks if the current node's parent
        #is the same as a nodes url and shifts the list back and
        #inserts itself right after it's parent node.
        else:
            temp = self.head

            while temp:
                if temp.url == new_Node.parent:
                    pushed_Node = temp.next
                    new_Node.next = pushed_Node
                    temp.next = new_Node
                    break

                elif temp.next is None:
                    temp.next = new_Node
                    break

                temp = temp.next

    #prints the linked list in a format where the depth is stated
    #and the child nodes are indented and visually associated with
    #their parent urls.
    def printLList(self):
        temp = self.head

        while temp:
            #the whitespace is to visually associate thr depth with
            #how much it has been indented
            whitespace = "   " * temp.depth
            print(f"{whitespace}- Depth:{temp.depth} URL:{temp.url}")
            temp = temp.next

    #Simple print out of all of the content in the linked list in
    #order for debugging and testing the list is working correctly
    def printTest(self):
        temp = self.head

        while temp:
            print(f"{temp.url}, {temp.parent}, {temp.depth}")
            temp = temp.next




#function gets url and returns list of domain links (internal only)
#as to not accidentally test the wrong site. Function is to be used
#in the for multiple threads
def get_links(url):
    response = requests.get(url, timeout = 20)

    #response status code 200 means the site has responded correctly
    #soup is to change th format from the raw dump that requests
    #gets into a tree for beautifulsoup functions and easier filtering
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)
        #print(len(links)#checks number of links

        all_links = []
        for link in links:
            #print(link)
            href = link["href"]
            text = link.get_text(strip=True)

            #urljoin gets the base url and combines it with href
            #to make the final url that is linked.
            full_url = urljoin(url, href)
            #print(full_url)

            #adds all links to a list as a dictionary
            all_links.append({
                "text": text,
                "url": full_url
            })
        #filter links by only internal links
        #mainly to not accidentally test on the wrong site.
        #This section may be removed and a list with all_links
        #urls made for multi-domain traversal.
        domain_links = []
        domain = urlparse(url).netloc
        for link in all_links:
            if urlparse(link["url"]).netloc == domain:
                domain_links.append(link)
        #for link in domain_links:
            #print(link["url"])
        #print(domain_links)
        return domain_links, soup

    else:
        print(f"Error: {response.status_code} for url: {url}")



def history_print(history):
    #test print to print all of the links flat out with depth
    # for link in history:
    #     whitespace = "     " * link["depth"]
    #
    #     if link["parent"] is None:
    #         print("Entered URL:")
    #         print(link['url'])
    #     else:
    #         print(f"{whitespace}- Depth:{link['depth']} URL:{link['url']}")


    history_lList = LinkedList()
    #print(history)
    for item in history:
        #print(item['depth'])

        if item['depth'] == 0:
            history_lList.append(
                item['url'],
                item['parent'],
                item['depth'])
            continue

        history_lList.insert(
            item['url'],
            item['parent'],
            item['depth'])
        #history_lList.printTest()

    print(history_lList.printLList())
    #print(history_lList.printTest())
