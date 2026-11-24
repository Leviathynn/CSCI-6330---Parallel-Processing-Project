#Description: main.py for running the web scraper final project for
#             parallel processing. database.py must be run at least
#             once to make the database used in this program. This
#             calls threadPool.py and processPool.py to get the links
#             for checking web pages.

from processPool import processPoolRun
from threadPool import threadPoolRun
from links import history_print

def main():
    #user changeable inputs
    #worker_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,
    #               21,22,23,24,25,26,27,28,29,30,31,32]
    worker_list = [6]
    depth = 4
    loops = 1
    url = 'https://www.scrapethissite.com/pages/simple/'

    #loop and print for main
    time_list = []
    history_threads = []
    #for every worker amount in the list of workers to calculate
    #do runs according to "loops" and store the times in to_append_process
    #and to_append_threads.
    for max_workers in worker_list:

        to_append_process = []
        to_append_threads = []
        for run in range(loops):
            time_elapsed_process, history = processPoolRun(url, depth, max_workers)
            time_elapsed_thread, history_threads = threadPoolRun(url, depth, max_workers)
            to_append_process.append(round(time_elapsed_process, 4))
            to_append_threads.append(round(time_elapsed_thread, 4))
            #history_print(history_threads)

        print("Processpoolexecutor    ", "Processes: ", max_workers,
              "     Times(seconds): ", to_append_process)
        print("Threadpoolexecutor     ", "Threads:   ", max_workers,
              "     Times(seconds): ", to_append_threads)
        time_list.append(to_append_process)

    history_print(history_threads)


if __name__ == "__main__":
    main()