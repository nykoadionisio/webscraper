import webscraper as ws
import plotly.graph_objects as go
import plotly.express as px

webinfo = ws.all_webinfo


def update_webinfo(keywords: list[str]):
    """ Updates webinfo variable

    """
    for website in ws.websites:
        ws.site_information(website, keywords)


def format_dict_to_parallel_lists(data: dict[str, float]) -> tuple[list[str], list[float]]:
    """ Converts a dictionary to two parallel lists

    """
    lst1 = []
    lst2 = []
    for key in data:
        lst1.append(key)
        lst2.append(data[key])

    return lst1, lst2


def display_percentage_bar_graph(keywords: list[str]):
    """ Displays a bar graph displaying the frequency percentage of each keyword in keywords

    """
    update_webinfo(keywords)
    data = ws.find_percentage(ws.find_related(webinfo, keywords), keywords)
    x, y = format_dict_to_parallel_lists(data)

    fig = go.Figure([go.Bar(x=x, y=y)])
    fig.update_layout(title='Keyword Frequency Percentages',
                      xaxis_title='Keyword',
                      yaxis_title='Percentage'
                      )
    fig.update_yaxes(range=[0, 100])

    fig.show()


def display_searches_over_time(keywords: list[str]):
    """ Displays a time-series graph displaying the interest of each keyword in keywords
        in terms of google searches

    """
    data = ws.trends_data(keywords)
    data = data.reset_index()

    fig = px.line(data,
                  x='date',
                  y=[keyword for keyword in keywords],
                  title='Keyword Search Interest Over Time',
                  labels={
                      'date': 'Date',
                      'value': 'Interest',
                      'variable': 'Keyword'
                  })
    fig.show()
