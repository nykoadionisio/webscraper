""" Main Module

This module calls functions from Webscraper Module and Graph Module on user input

This file is Copyright (c) 2021 Amelia, Henry, Darlyn, Nyko.
"""
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


def clean_input(input: str) -> list[str]:
    """Returns a list of each word separated by commas in input

    >>> clean_input('cat, dog')
    ['cat', 'dog']
    """
    input = input.replace(" ", "")
    input = input.replace("_", " ")
    input = input.split(',')

    return input


# Main loop
run = True
while run:

    inputs = input("Instructions: \n"
                   "If you wish to enter more than one word, separate each word with a comma \n"
                   "If there is a space in your word, use a '_' instead of the space. \n"
                   "Enter your keywords: ")
    keywords = clean_input(inputs)

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
