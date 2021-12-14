""" Main code done by Amelia, Henry, Darlyn, Nyko. """
import python_ta

import webscraper as ws
import graph as g


def get_max(word_list: list[str]) -> None:
    """ Find the peak popularity for each word in word_list
     and the day it reached that maximum and print that value.

    """

    data = ws.trends_data(word_list)
    maxes = []

    for word in word_list:
        current_max = 0
        max_date = ''
        for date in data[word].keys():
            if data[word][date] >= current_max:
                current_max = data[word][date]
                max_date = str(date)
        maxes.append((max_date, current_max))
        print("Latest peak popularity for " + word
              + " was: " + str(current_max) + ' on ' + max_date)


def get_min(word_list: list[str]) -> None:
    """ Find the minimum popularity for each word in word_list
     and the day it reached that minimum and print that value.

    """
    data = ws.trends_data(word_list)
    mins = []
    for word in word_list:
        current_min = 101
        min_date = ''
        for date in data[word].keys():
            if data[word][date] <= current_min:
                current_min = data[word][date]
                min_date = str(date)
        mins.append((min_date, current_min))
        print("Latest minimum popularity for " + word
              + " was: " + str(current_min) + ' on ' + min_date)


# Main loop
run = True
while run is True:
    inputs = input("Rules: \n"
                   "If you wish to enter more than one word, separate each word with a comma \n"
                   "If there is a space in your word, use a '_' instead of the space. \n"
                   "Enter your keywords: ")
    cleaned_once = inputs.replace(" ", "")
    cleaned_twice = inputs.replace("_", " ")
    keywords = cleaned_twice.split(',')

    # Display the graphs
    g.display_percentage_bar_graph(keywords)
    g.display_searches_over_time(keywords)

    # Display data
    print("Data:")
    get_max(keywords)
    get_min(keywords)

    # Stop
    power = input("Input new words?(y/n): ")
    if power == 'n':
        run = False

if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': ['webscraper', 'graph'],  # the names (strs) of imported modules
        'allowed-io': ['get_max',
                       'get_min'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'E9997']
    })

    import doctest

    doctest.testmod()
