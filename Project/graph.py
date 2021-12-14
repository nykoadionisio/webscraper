"""Graph Module

This module contains functions that displays data from the Webscraper Module
in the form of charts, using the Plotly library.

This file is Copyright (c) 2021 Amelia, Henry, Darlyn, Nyko.
 """
import python_ta

import plotly.express as px
import plotly.graph_objects as go
import webscraper as ws


def format_dict_to_parallel_lists(data: dict) -> tuple[list, list]:
    """ Converts a dictionary to a tuple of two parallel lists

    >>> d = {'Hello': 1, 'World!': 2}
    >>> format_dict_to_parallel_lists(d)
    (['Hello', 'World!'], [1, 2])
    """
    lst1 = []
    lst2 = []
    for key in data:
        lst1.append(key)
        lst2.append(data[key])

    return lst1, lst2


def display_percentage_bar_graph(keywords: list[str]) -> None:
    """ Displays a bar graph displaying the frequency percentage of each keyword in keywords

       Preconditions:
        - keywords != []
    """
    data = ws.find_percentage(keywords)
    x, y = format_dict_to_parallel_lists(data)

    fig = go.Figure([go.Bar(x=x, y=y)])
    fig.update_layout(title='Keyword Frequency Percentages',
                      xaxis_title='Keyword',
                      yaxis_title='Percentage'
                      )
    fig.update_yaxes(range=[0, 100])

    fig.show()


def display_searches_over_time(keywords: list[str]) -> None:
    """ Displays a time-series graph displaying the interest of each keyword in keywords
        in terms of google searches

    Preconditions:
        - keywords != []
    """
    data = ws.trends_data(keywords)
    data = data.reset_index()

    fig = px.line(data,
                  x='date',
                  y=list(keywords),
                  title='Keyword Search Interest Over Time',
                  labels={
                      'date': 'Date',
                      'value': 'Interest',
                      'variable': 'Keyword'
                  })
    fig.show()


if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': ['webscraper', 'plotly.graph_objects',
                          'plotly.express'],  # the names (strs) of imported modules
        'allowed-io': [],     # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'E9997']
    })

    import doctest

    doctest.testmod()
