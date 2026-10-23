#Name: Stephanie Zhang
#Class: CSCI 6330 - Parallel
#Assignment: Final Project
#Description: main.py for running the web scraper final project for
#             parallel processing

#imports
from links import get_links, history_print
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed

#values to make user input-able after testing is done
depth = 3
max_workers=4
url = 'https://www.scrapethissite.com/pages/simple/'

#double ended queue for easy removing value from front and adding in
#back. Format is (current url, depth, parent url). First url has no parent
queue = deque([(url, 0, None)])
visited = set()
history = []

with ThreadPoolExecutor(max_workers=max_workers) as executor:

    while queue:
        depth_length = len(queue)
        current_depth_list = [] #list to store all links in the current
                                #depth. This is so the multi-thread
                                #parallels correctly.

        #For the entire current depth, as long as the item has not already
        #been visited, it is added to the list with all urls in the depth.
        for i in range(depth_length):
            current_url, current_depth, parent_url = queue.popleft()

            if current_depth >= depth:
                continue
            if current_url not in visited:
                visited.add(current_url)#updates visited list so duplicate pages aren't visited again. possibly looping
                #history of sites processed in order to print out for debugging and visualization
                history.append({"url": current_url, "depth": current_depth, "parent": parent_url})
                #for sequential processing for the thread manager
                current_depth_list.append((current_url, current_depth, parent_url))
        #print(visited)
        #print(current_depth_list)
        if not current_depth_list:
            continue

        #Loops through all items in the current depth, if the current depth
        #is less than the max depth entered and submits the function the
        #thread executor will need to run into a log.
        thread_log = {}
        for current_url, current_depth, parent_url in current_depth_list:

            if current_depth > depth:
                continue

            temp = executor.submit(get_links, current_url)
            thread_log[temp] = (current_url, current_depth)
        #print(thread_log)

        #Loop for the thread executor to process async
        #has a html dump in bs4 format for now. Reminder to precess or store it
        #later in the project
        for temp in as_completed(thread_log):
            current_url, current_depth = thread_log[temp]

            #soup_html is for future parsing or downloading
            #of site contents
            #thread runs
            try:
                domain_links, soup_html = temp.result()
            except Exception as e:
                continue
            #loops through the internal links just generated and adds them to the
            #queue with the current url as the parent and depth incremented.
            for link in domain_links:
                link_url = link["url"]

                if link_url not in visited:
                    queue.append((link_url, current_depth+1, current_url))


#print(history)
#print("\n")
history_print(history)