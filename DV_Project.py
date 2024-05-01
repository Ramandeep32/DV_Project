import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

def filter_data(df, format):
    return df[df['Unnamed: 0'] == format].iloc[0]
radar_data_virat = pd.read_csv("71 Centuries of Virat Kohli.csv")
radar_data_sachin = pd.read_csv("Sachin Tendulkar - 100 Centuries.csv")
radar_data_virat = radar_data_virat.rename(columns={"Venue":"Stadium", "Column1":"City", "Inn.":"Innings", "H/A":"Home/Away","Out/Not Out":"Dismissed"})
radar_data_virat = radar_data_virat.drop(["Dismissed","Batting Order","Innings","Strike Rate","Captain","Batting Order","Innings","Strike Rate","Home/Away","Result","Date","Format","City","Man of the Match"], axis=1)
radar_data_sachin = radar_data_sachin.rename(columns={"Player of the match":"Man of the Match", "Venue":"Stadium"})

radar_data_sachin = radar_data_sachin.drop(["S.No.","Dismissed","Captain","Position","Innings","Strike Rate","H/A","Result","City","Man of the Match"], axis=1)
radar_data_sachin = radar_data_sachin.reindex(columns=["Score","Against","Stadium"])

radar_team = radar_data_virat["Against"].value_counts().index.tolist()
for i in radar_data_sachin["Against"]:
    if i not in radar_team:
        radar_team.append(i)

Radar_Virat = []
for i in radar_team:
    if i in radar_data_virat["Against"].tolist():
        Radar_Virat.append(radar_data_virat["Against"].value_counts()[i])
    else:
        Radar_Virat.append(0)
Radar_Sachin = []
for i in radar_team:
    if i in radar_data_sachin["Against"].tolist():
        Radar_Sachin.append(radar_data_sachin["Against"].value_counts()[i])
    else:
        Radar_Sachin.append(0)


# Function to scrape and parse opponent statistics for a player
def scrape_player_opponents(player_id, format):
    # Determine URL based on format
    if format == "ODI":
        url = f"http://www.howstat.com/cricket/statistics/Players/PlayerOpponents_ODI.asp?PlayerID={player_id}#bat"
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table containing the desired data
        table = soup.find("table", {"class": "TableLined"})

        # Extract data from the table
        rows = table.find_all("tr")
        data = []
        for row in rows[1:]:  # Exclude first two header rows
            cols = row.find_all("td")
            cols = [col.get_text(strip=True) for col in cols]
            data.append(cols)

        # Create a DataFrame from the extracted data
        df = pd.DataFrame(data, columns=["Versus", "Mat", "Inns", "NO", "100s", "50s", "0s", "HS", "Runs", "Avg", "S/R", "Ca Fld", "Ca Kpr", "St"])

    elif format == "T20":
        url = f"http://www.howstat.com/cricket/statistics/Players/PlayerOpponents_T20.asp?PlayerID={player_id}#bat"
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table containing the desired data
        table = soup.find("table", {"class": "TableLined"})

        # Extract data from the table
        rows = table.find_all("tr")
        data = []
        for row in rows[1:]:  # Exclude first two header rows
            cols = row.find_all("td")
            cols = [col.get_text(strip=True) for col in cols]
            data.append(cols)

        # Create a DataFrame from the extracted data
        df = pd.DataFrame(data, columns=["Versus", "Mat", "Inns", "NO", "100s", "50s","4s","6s", "0s", "HS", "Runs", "Avg", "S/R", "Ca Fld", "Ca Kpr", "St"])
        df=df.drop(["4s","6s"],axis=1)

    elif format == "Test":
        url = f"http://www.howstat.com/cricket/statistics/Players/PlayerOpponents.asp?PlayerID={player_id}" 
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table containing the desired data
        table = soup.find("table", {"class": "TableLined"})

        # Extract data from the table
        rows = table.find_all("tr")
        data = []
        for row in rows[1:]:  # Exclude first two header rows
            cols = row.find_all("td")
            cols = [col.get_text(strip=True) for col in cols]
            data.append(cols)

        # Create a DataFrame from the extracted data
        df = pd.DataFrame(data, columns=["Versus", "Mat", "Inns", "NO", "100s", "50s", "0s", "HS", "Runs", "Avg", "S/R", "Ca Fld", "Ca Kpr", "St"])

    else:
        raise ValueError("Invalid format. Use 'ODI' or 'T20'.")

    # Send an HTTP GET request to the URL
    
    # Map country names to continents
    # df["Continent"] = df["Versus"].apply(get_continent)

    return df

def scrape_player_progress_summary(player_id, format):

    if format == "ODI":
        url = f"http://www.howstat.com/cricket/statistics/players/PlayerProgressSummary_ODI.asp?PlayerID={player_id}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", {"class": "TableLined"})
        rows = table.find_all("tr")
        data = []
        for row in rows[1:]:
            cols = row.find_all("td")
            cols = [col.get_text(strip=True) for col in cols]
            data.append(cols)
        df = pd.DataFrame(data, columns=["Match", "Innings", "Date", "Versus", "Ground", "Runs", "Aggr", "Avg", "Wkts", "Aggr", "Avg", "Ca", "Agg", "Ca", "St", "Agg", "Age"])
    elif format == "T20":
        url = f"http://www.howstat.com/cricket/statistics/players/PlayerProgressSummary_T20.asp?PlayerID={player_id}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", {"class": "TableLined"})
        rows = table.find_all("tr")
        data = []
        for row in rows[1:]:
            cols = row.find_all("td")
            cols = [col.get_text(strip=True) for col in cols]
            data.append(cols)
        df = pd.DataFrame(data, columns=["Match", "Innings", "Date", "Versus", "Ground", "Runs", "Aggr", "Avg", "Wkts", "Aggr", "Avg", "Ca", "Agg", "Ca", "St", "Agg", "Age"])
    elif format == "Test":
        url = f"http://www.howstat.com/cricket/statistics/players/PlayerProgressSummary.asp?PlayerID={player_id}" 
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", {"class": "TableLined"})
        rows = table.find_all("tr")
        data = []
        for row in rows[1:]:
            cols = row.find_all("td")
            cols = [col.get_text(strip=True) for col in cols]
            data.append(cols)
        df = pd.DataFrame(data, columns=["Match", "Innings", "Date", "Versus", "Ground","Inns", "Runs", "Aggr", "Avg", "Wkts", "Aggr", "Avg", "Ca", "Agg", "Ca", "St", "Agg", "Age"])
        df=df.drop("Inns",axis=1)
    else:
        raise ValueError("Invalid format. Use 'ODI' or 'T20'.")
    return df

def generate_figure_virat_polar(format):
    if format=="Test":
        data = {
        "Bowler / Country": [
            "J M Anderson* (England)",
            "N M Lyon* (Australia)",
            "M M Ali* (England)",
            "B A Stokes* (England)",
            "S C J Broad* (England)"
        ],
        "B": [0, 0, 1, 1, 0],
        "C": [4, 4, 3, 2, 3],
        "CB": [0, 0, 1, 2, 1],
        "LBW": [0, 3, 1, 2, 1],
        "Total": [7, 7, 6, 6, 5]  # Total dismissals
        }

    elif format == "ODI":
        data = {
        "Bowler / Country": [
            "T G Southee* (New Zealand)",
            "R Rampaul* (West Indies)",
            "J R Hazlewood* (Australia)",
            "N L T C Perera (Sri Lanka)",
            "Shakib Al Hasan* (Bangladesh)"
        ],
        "B": [1, 1, 1, 0, 1],
        "C": [5, 2, 3, 3, 3],
        "CB": [1, 3, 1, 1, 0],
        "LBW": [0, 0, 0, 1, 0],
        "St": [0, 0, 0, 0, 1],
        "Total": [7, 6, 5, 5, 5]  # Total dismissals
        }
    elif format == "T20":
        data = {
        "Bowler / Country": [
            "C J Jordan* (England)",
            "I S Sodhi* (New Zealand)",
            "A Zampa* (Australia)",
            "H K Bennett* (New Zealand)",
            "P K D Chase (Ireland)"
        ],
        "B": [0, 0, 1, 0, 0],
        "C": [3, 2, 2, 2, 2],
        "CB": [0, 1, 0, 0, 0],
        "LBW": [0, 1, 0, 0, 0],
        "Total": [3, 3, 3, 2, 2]  # Total dismissals
        }


    bowlers = data["Bowler / Country"]
    categories = len(bowlers)
    nbar_group = 4  # Number of bars in a group ("B", "C", "CB", "LBW")
    step = 360 / categories
    small_step = step / (nbar_group + 1)
    theta = [0.5 * (2 * k - 1) * step + small_step * (j + 1) for k in range(categories) for j in range(nbar_group)]
    r = [data[key][i] for i in range(categories) for key in ["B", "C", "CB", "LBW"]]
    marker_color = [0, 1, 2, 3] * categories  # Mapping B, C, CB, LBW to numerical values
    tickvals = [k * step for k in range(categories)]
    ticktext = bowlers

    # Mapping numerical values to dismissal types
    colorbar_annotations = {
        0: "B - Bowled",
        1: "C - Caught",
        2: "CB - Caught Behind",
        3: "LBW - Leg Before Wicket"
    }

    # Initial figure
    fig = go.Figure(go.Barpolar(r=r, theta=theta, marker_color=marker_color, marker_colorscale="Viridis",
                               ))
    fig.update_layout(width=650, polar=dict(angularaxis=dict(tickvals=tickvals, ticktext=ticktext)),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    ))

    fig.update_traces(showlegend=True,
                    legendgroup="group",
                    name='Statistics',
                    marker=dict(line=dict(width=0.3, color='black')))

    # Update color bar annotations
    fig.update_layout(coloraxis_colorbar=dict(
        title='Dismissal Type',
        tickvals=[0, 1, 2, 3],
        # ticktext=[colorbar_annotations[i] for i in range(4)]
    ))    
    return fig
    



def generate_figure_sachin_polar(format):
    if format=="Test":
        data = {
            "Bowler / Country": [
                "J M Anderson*(England)",
                "M Muralitharan(Sri Lanka)",
                "J N Gillespie(Australia)",
                "G D McGrath(Australia)",
                "W J Cronje(South Africa)",
                "A A Donald(South Africa)"
            ],
            "B": [2, 1, 0, 1, 0, 2],
            "C": [2, 4, 1, 1, 3, 1],
            "CB": [2, 0, 3, 1, 1, 1],
            "LBW": [3, 0, 2, 3, 1, 1],
            "Total": [9, 8, 6, 6, 5, 5]
        }
    elif format == "ODI":
        data = {
        "Bowler / Country": [
            "B Lee (Australia)",
            "S M Pollock (South Africa)",
            "W P U J C Vaas (Sri Lanka)",
            "G D McGrath (Australia)",
            "H H Streak (Zimbabwe)"
        ],
        "B": [2, 2, 2, 0, 1],
        "C": [4, 3, 4, 4, 4],
        "CB": [1, 3, 2, 3, 2],
        "LBW": [1, 1, 1, 0, 0],
        "Total": [9, 9, 9, 7, 7]
        }
    elif format == "T20":
        data = {
        "Bowler / Country": [
            "C K Langeveldt (South Africa)"
        ],
        "B": [1],
        "C": [0],
        "CB": [0],
        "LBW": [0],
        "Total": [1]
        }

    bowlers = data["Bowler / Country"]
    categories = len(bowlers)
    nbar_group = 4  # Number of bars in a group ("B", "C", "CB", "LBW")
    step = 360 / categories
    small_step = step / (nbar_group + 1)
    theta = [0.5 * (2 * k - 1) * step + small_step * (j + 1) for k in range(categories) for j in range(nbar_group)]
    r = [data[key][i] for i in range(categories) for key in ["B", "C", "CB", "LBW"]]
    marker_color = [0, 1, 2, 3] * categories  # Mapping B, C, CB, LBW to numerical values
    tickvals = [k * step for k in range(categories)]
    ticktext = bowlers

    # Mapping numerical values to dismissal types
    colorbar_annotations = {
        0: "B - Bowled",
        1: "C - Caught",
        2: "CB - Caught Behind",
        3: "LBW - Leg Before Wicket"
    }

    # Initial figure
    fig = go.Figure(go.Barpolar(r=r, theta=theta, marker_color=marker_color, marker_colorscale="Viridis", 
                                marker_colorbar_thickness=15
                                ))
    fig.update_layout(width=600, polar=dict(angularaxis=dict(tickvals=tickvals, ticktext=ticktext)),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    ))

    fig.update_traces(showlegend=True,
                    legendgroup="group",
                    name='Statistics',
                    marker=dict(line=dict(width=0.5, color='black')))

    # Update color bar annotations
    fig.update_layout(coloraxis_colorbar=dict(
        title='Dismissal Type',
        tickvals=[0, 1, 2, 3],
        # ticktext=[colorbar_annotations[i] for i in range(4)]
    ))
    return fig

def generate_pyramid_chart():
    innings = [-24, -53, -75, -93, -114, -136, -161, -175, -194, -205, -222, -242]
    positive_innings = [24, 53, 75, 93, 114, 136, 161, 175, 194, 205, 222, 242]
    virat_runs = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000]
    sachin_innings = [34, 70, 93, 112, 138, 170, 189, 210, 235, 259, 276, 300]
    sachin_runs = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000]

    # Reverse Sachin's innings and runs for pyramid effect
    # sachin_runs = sachin_runs[::]
    # virat_runs = virat_runs[::]
    # Create a new figure
    fig = go.Figure()

    # Add Sachin's innings and runs on the left side (mirrored)
    fig.add_trace(go.Bar(
        y=sachin_runs,
        x=sachin_innings,
        orientation="h",
        name="Sachin Tendulkar",
        marker=dict(color="red"),
        text=sachin_innings,
    ))

    # Add Virat's innings and runs on the right side
    fig.add_trace(go.Bar(
        y=virat_runs,
        x=innings,
        orientation="h",
        name="Virat Kohli",
        marker=dict(color="blue"),
        text=positive_innings,
    ))

    # Update the figure layout
    fig.update_layout(
        title="Runs scored vs Innings taken",
        yaxis=dict(title="Runs", range=[max(max(sachin_runs), max(virat_runs))+1000, 0]),
        xaxis=dict(range=[min(innings)-50, max(positive_innings)+100], dtick=300),  # Shift origin to the left top
        barmode="overlay",  # Bars will be grouped side by side
        bargap=0.1,  # Gap between bars
        hovermode="closest",
        showlegend=True,
        height=500,
        legend=dict(orientation='h', yanchor='top', y=1.1, xanchor='center', x=0.5)
    )

    return fig
test_data = pd.read_csv("comparison_test.csv")
odi_data = pd.read_csv("comparison_odi.csv")

def extract_data(data):
    bowler_names = data["Bowlers"].tolist()
    categories = data.columns[1:].tolist()  # Exclude the first column (Bowlers)
    sachin_values = data.iloc[:, 1:7].values.tolist()  # Assuming first 4 columns are for Sachin, next 4 for Virat
    virat_values = data.iloc[:, 7:13].values.tolist()  # Adjust the column indices accordingly
    return bowler_names, categories, sachin_values, virat_values

test_bowler_names, test_categories, test_sachin_values, test_virat_values = extract_data(test_data)
odi_bowler_names, odi_categories, odi_sachin_values, odi_virat_values = extract_data(odi_data)

player1_name = 'Sachin Tendulkar'
player2_name = 'Virat Kohli'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define layout
background_image = "background.png"
app.layout = html.Div(style={'backgroundImage': f'url("{background_image}")', 'backgroundSize': '70px 800px'}, children=[
    dcc.Tabs([
        dcc.Tab(label='Overview of statistics', children=[
            html.H1("Sachin Tendulkar vs Virat Kohli", style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'center', 'color': '#333', 'font-family': 'Arial, sans-serif'}),
            html.Div([
                html.Label("Select Format:", style={'color': 'green'}),
                dcc.RadioItems(
                    id='Bar-format-radio',
                    options=[
                        {'label': 'Test', 'value': 'Test'},
                        {'label': 'ODI', 'value': 'ODI'},
                        {'label': 'T20I', 'value': 'T20I'},
                        {'label': 'IPL', 'value': 'IPL'}
                    ],
                    value='Test',
                    labelStyle={'display': 'inline-block', 'margin-right': '10px'}
                )
            ], style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'center'}),
            html.Div([
                html.Div([
                    html.Img(src='sachin.png', style={'height': 'auto', 'width': '300px'}),
                ], style={'flex': '1', 'display': 'flex', 'justify-content': 'center'}),
                html.Div([
                    # dcc.Graph(id='bar-chart', style={'height': '600px', 'width': '650px'}),
                    dcc.Tabs(id='stats-tabs', value='batting-stats', children=[
                        dcc.Tab(label='Batting Stats', value='batting-stats', children=[
                            dcc.Graph(id='Batting_stats', style={'height': '600px', 'width': '650px'})
                        ]),
                        dcc.Tab(label='Bowling Stats', value='bowling-stats', children=[
                            dcc.Graph(id='bowling-stats', style={'height': '600px', 'width': '650px'})
                        ])
                    ])
                ], style={'flex': '1', 'display': 'flex', 'justify-content': 'center'}),
                html.Div([
                    html.Img(src='virat.png', style={'height': 'auto', 'width': '300px'}),
                ], style={'flex': '1', 'display': 'flex', 'justify-content': 'center'})
            ], style={'display': 'flex', 'justify-content': 'center'}),
            html.Div([
                html.Div([
                    html.P("Sachin Tendulkar, often referred to as the ""Master Blaster"" and ""Little Master,"" is a cricketing icon whose name is synonymous with excellence and records. Born on April 24, 1973, in Mumbai, India, Tendulkar's career spanned over two decades, during which he etched his name in the annals of cricket history. Renowned for his impeccable technique, exquisite stroke play, and insatiable hunger for runs, Tendulkar holds numerous batting records, including the most runs and centuries in both Test and One Day International (ODI) cricket. His unparalleled achievements have earned him adulation and respect from cricketing enthusiasts worldwide, making him one of the most revered figures in the sport",
                            style={'height': 'auto', 'width': '400px','margin': '5px','font-size': '14px'}),
                ], style={'border': '1px solid #ccc', 'padding': '5px'}),
                html.Div([
                        html.H3("Conclusion"),
                        html.Ul([
                            html.Li("Sachin Tendulkar emerges as the leading run-scorer in both Test and ODI formats, showcasing his unparalleled consistency and longevity in international cricket."),
                            html.Li("Conversely, Virat Kohli dominates in IPL and T20 formats, underscoring his exceptional prowess and adaptability in the shorter formats of the game."),
                            html.Li("It's notable that Sachin Tendulkar's versatility extended beyond batting, as he also contributed as a bowler, a dimension absent in Virat Kohli's statistical profile."),
                        ],style={'height': 'auto', 'width': '400px','font-size': '14px'})
                ], style={'border': '1px solid #ccc', 'padding': '5px'}),
                html.Div([
                    html.P(" Virat Kohli, the modern-day maestro of cricket, is a powerhouse batsman known for his aggressive style, unparalleled consistency, and indomitable spirit on the field. Born on November 5, 1988, in Delhi, India, Kohli rose through the ranks to become one of the most influential cricketers of his generation. With a penchant for chasing down targets and leading from the front, Kohli has amassed a staggering number of runs across all formats of the game, captivating audiences with his batting prowess and unwavering determination. As the torchbearer of Indian cricket, Kohli's leadership and passion have inspired millions, cementing his status as a true legend in the making.",
                            style={'height': 'auto', 'width': '400px','font-size': '14px'}),
                ], style={'border': '1px solid #ccc', 'padding': '5px'}),
            ], style={'display': 'flex', 'justify-content': 'center'})
        ]),
        dcc.Tab(label='Runs scored Vs innings', children=[
            html.H1("The Run Marathon", style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'center', 'color': '#333', 'font-family': 'Arial, sans-serif'}),
            dcc.RadioItems(
                id='line-format-radio',
                options=[
                    {'label': 'Test', 'value': 'Test'},
                    {'label': 'ODI', 'value': 'ODI'},
                    {'label': 'T20', 'value': 'T20'}
                ],
                value='ODI',
                labelStyle={'display': 'inline-block', 'margin-right': '10px'},  # Display radio items inline
                style={'text-align': 'center'}
            ),
            dcc.Graph(id='line-chart', style={'height': '600px'}),
            html.Div([
                    html.H3("Overall conclusion"),
                        html.Ul([
                            html.Li("In Tests, Sachin Tendulkar has notably scored more runs in the same number of innings as Virat Kohli. However, it's intriguing to note that Sachin achieved this feat at the age of 30, while Virat accomplished it at 35. This age difference suggests that Virat may face challenges in surpassing Sachin's records in Test cricket due to the limitations posed by age-related decline."),
                            html.Li("In ODIs, Virat Kohli has outperformed Sachin Tendulkar by scoring 2,000 more runs in the same number of innings. However, it's essential to consider the context that Sachin was only 31 when achieving this milestone, whereas Virat is currently trailing by approximately 5,000 runs. Although Virat has showcased exceptional consistency and form, surpassing Sachin's overall ODI run tally might be a daunting task, especially considering Sachin's prolonged career span of seven more years post this milestone."),
                            html.Li("In T20 cricket, there's a clear dominance of Sachin Tendulkar since he played only one T20 match during his career. This stark contrast indicates that while Sachin's T20 career was brief, Virat has had a more significant impact in this format due to his active participation and consistent performances."),
                        ],style={'height': 'auto', 'width': 'auto','font-size': '14px'})
                ], style={'border': '1px solid #ccc', 'padding': '5px'}),
            html.Div([
                    html.H1("Milestones Unveiled: The Journey to 12K Runs in Innings"),
                    dcc.Graph(id="pyramid-chart",figure=generate_pyramid_chart()),
                    # html.H4("Conclusion"),
                    html.P("Virat Kohli achieved each milestone with fewer innings than Sachin Tendulkar, reflecting Kohli's efficiency and ability to convert innings into significant runs at a faster rate. Sachin Tendulkar's innings to runs ratio appears slightly higher than Kohli's, indicating a slightly slower but equally effective accumulation of runs over a longer period.",
                        style={'height': 'auto', 'width': 'auto','font-size': '14px'}),
                ]),
        ]),
            dcc.Tab(label='Runs against opponents', children=[
                html.H1("Conquering Countries: A Journey Through Runs and Rivalries", style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'center', 'color': '#333', 'font-family': 'Arial, sans-serif'}),
                html.Div([
                dcc.RadioItems(
                    id='map-format-radio',
                    options=[
                        {'label': 'Test', 'value': 'Test'},
                        {'label': 'ODI', 'value': 'ODI'},
                        {'label': 'T20', 'value': 'T20'}
                    ],
                    value='ODI',
                    labelStyle={'display': 'inline-block', 'margin-right': '10px'},  # Display radio items inline
                    style={'text-align': 'center'}
                ),
                
                dcc.Graph(id='bubble-map-countrywise',style={'height': '600px'}),
                html.Div([
                    html.H1("Worldly Wickets: Exploring Runs Across Cricketing Frontiers", style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'center', 'color': '#333', 'font-family': 'Arial, sans-serif'}),
                dcc.Graph(id="bubble-map",style={'height': '600px'})
                ]),
                # html.Div([
                    html.H3("Overall conclusion"),
                        html.Ul([
                            html.Li("In Test matches, Sachin Tendulkar has consistently outperformed Virat Kohli against all opponents. Sachin's superior run-scoring record against each team highlights his enduring excellence and dominance in the longest format of the game. Sachin's consistent performances across various conditions demonstrate his unparalleled skill and longevity, establishing him as one of the greatest batsmen in cricket history."),
                            html.Li("In ODIs, Sachin Tendulkar outshines Virat Kohli in runs scored against several teams. Notably, Sachin leads in runs against Australia, England, Pakistan, and Sri Lanka. However, Virat demonstrates strength against teams like West Indies, Bangladesh, and Afghanistan. Sachin's experience reflects in his dominance across varied opponents, while Virat's consistent performance hints at his adaptability and prowess in contemporary cricket."),
                            html.Li("In T20 cricket, Virat has shown dominance, outscoring Sachin against every opponent"),
                        ],style={'height': 'auto', 'width': 'auto','font-size': '14px'}),
                # ], style={'border': '1px solid #ccc', 'padding': '5px'}),

                html.Div([
                html.H1("Century Chronicles"),
                dcc.Graph(id='radar-chart',style={'height': '600px'}),
                html.P("Sachin Tendulkar's century record stands at 100 in international cricket, spread across Test (51), ODI (49), and IPL (1). His remarkable consistency and longevity are evident, with Test cricket being his most prolific format. In contrast, Virat Kohli has amassed a total of 87 centuries, distributed across Test (29), ODI (48), and IPL (7). Despite a shorter career span, Kohli's century tally reflects his exceptional batting prowess across all formats, with ODIs being his stronghold. Both legends have left an indelible mark on cricket history with their remarkable century-scoring abilities.",
                        style={'height': 'auto', 'width': 'auto','font-size': '14px'}),
                ])
            ])
        ]),
            dcc.Tab(label='Performance against bowlers', children=[
                    html.Div([
                        html.Div([
                        html.H1("Wicket Wizards: Unraveling the Enigma of Dismissals"),
                        html.Label("Select Format:", style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'center'}),
                            dcc.RadioItems(
                                id='format-radio',
                                options=[
                                    {'label': 'Test', 'value': 'Test'},
                                    {'label': 'ODI', 'value': 'ODI'},
                                    {'label': 'T20', 'value': 'T20'}
                                ],
                                value='ODI',
                                labelStyle={'display': 'inline-block', 'margin-right': '10px'},  # Display radio items inline
                                style={'text-align': 'center'}
                            ),
                        ], style={'width': '100%', 'display': 'inline-block'}),
                        # html.Div([
                        #     html.Div([
                        #         html.H2("Virat Kohli",style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'center'}),
                        #         dcc.Graph(id='polar-plot-virat'),
                                
                        #     ]
                        #     , style={'width': '55%', 'display': 'inline-block','margin-left':'0px'}
                        #     ),
                        #     html.Div([
                        #         html.H2("Sachin Tendulkar",style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'center'}),
                        #         dcc.Graph(id='polar-plot-sachin')
                        #     ]
                        #     , style={'width': '55%', 'display': 'inline-block','margin-right':'0px'}
                        #     )
                        # ], style={'width': '100%', 'display': 'inline-block','justify-content': 'space-between'})
                        html.Div([
                            html.Div([
                                html.H2("Virat Kohli", style={'text-align': 'center', 'color': '#333', 'font-family': 'Arial, sans-serif'}),
                                dcc.Graph(id='polar-plot-virat'),
                            ], className='plot'),
                            html.Div([
                                html.H2("Sachin Tendulkar", style={'text-align': 'center', 'color': '#333', 'font-family': 'Arial, sans-serif'}),
                                dcc.Graph(id='polar-plot-sachin'),
                            ], className='plot')
                        ], style={'display': 'flex', 'max-width': '2500px', 'margin': '0 auto','margin-left':'0px'})
                    ], style={'margin': '0 auto'}),
                    html.Div([
                        html.H1("Bowler Showdown"),
                        dcc.RadioItems(
                            id='dataset-radio',
                            options=[
                                {'label': 'Test', 'value': 'test'},
                                {'label': 'ODI', 'value': 'odi'}
                            ],
                            value='test',  # Default value
                            labelStyle={'display': 'inline-block'},
                            style={'text-align': 'center'}
                        ),
                        html.Div([
                            dcc.Dropdown(
                                id='bowler-dropdown',
                                options=[],  # Will be updated based on selected dataset
                                value=[],
                                style={'margin-left':'240px','width': '50%','text-align': 'center'},  # Will be updated based on selected dataset
                            ),
                        ],style={'text-align': 'center'}),
                        dcc.Graph(id='radar-chart-bowler')
                    ])
                ]),
                dcc.Tab(label='Overall conclusion', children=[
            html.Div([
                html.Div([
                    html.Img(src='sachin.png', style={'height': 'auto', 'width': '300px'}),
                ], style={'flex': '1', 'display': 'flex', 'justify-content': 'center'}),
                html.Div([
                    # html.H3("Overall conclusion"),
                        html.Ul([
                            html.Li("Sachin Tendulkar's illustrious career boasts superior records in Test and ODI cricket, showcasing his unparalleled mastery and consistency in these formats. His dominance in Test cricket is evident through his monumental runs and centuries, setting benchmarks that epitomize batting excellence. In ODIs, Sachin's record-breaking feats remain unmatched, though Virat Kohli's prolific run-scoring suggests he could challenge these records given time. While Sachin's T20 career was limited, his legacy transcends formats, with Virat emerging as the epitome of T20 batting brilliance. Additionally, Sachin's occasional bowling contributions add another dimension to his all-around skills. In terms of captaincy, Virat's aggressive leadership style has yielded significant success, whereas Sachin's leadership tenure, though brief, showcased moments of strategic brilliance. Ultimately, both legends have left an indelible mark on cricket, enriching the sport with their extraordinary talent and inspiring generations of cricketers worldwide."),
                            html.Li("In conclusion, determining who is better between Sachin Tendulkar and Virat Kohli is a futile endeavor. Their greatness transcends statistical comparisons, as they graced the cricketing world in different eras, each leaving an indelible mark on the sport. Sachin's timeless elegance and Kohli's modern-day mastery are both emblematic of cricketing excellence. Their contributions have not only shaped the game but also inspired countless aspiring cricketers worldwide. To label one as superior would be an injustice to their respective legacies. Sachin and Virat are champions in their own right, and their enduring impact on the sport ensures that their names will forever be etched in cricketing folklore."),
                        ],style={'height': 'auto', 'width': 'auto','font-size': '14px'})
                ], style={'border': '1px solid #ccc', 'padding': '10px'}),
                html.Div([
                    html.Img(src='virat.png', style={'height': 'auto', 'width': '300px'}),
                ], style={'flex': '1', 'display': 'flex', 'justify-content': 'center'})
            ], style={'display': 'flex', 'justify-content': 'center'}),
            
        ]),
    ])
])

# Define callbacks for updating charts
# Define callbacks for updating charts
@app.callback(
    Output('Batting_stats', 'figure'),
    Input('Bar-format-radio', 'value')
)
def update_bar_chart(selected_format):
    # Filter the datasets for the selected format
    url_sachin = "https://www.cricbuzz.com/profiles/25/sachin-tendulkar"
    url_virat = "https://www.cricbuzz.com/profiles/1413/virat-kohli"
    df_sachin = pd.read_html(url_sachin)[0]
    df_virat = pd.read_html(url_virat)[0]
    sachin_test = filter_data(df_sachin, selected_format)
    virat_test = filter_data(df_virat, selected_format)

    # Get the column names excluding 'Unnamed: 0'
    attributes = sachin_test.index[2:]

    # Extract Sachin and Virat's runs
    sachin_runs = sachin_test[2:]
    virat_runs = virat_test[2:]

    # Calculate the total runs for each attribute
    total_runs = sachin_runs + virat_runs

    # Calculate the percentage of runs contributed by each player
    sachin_percentage = (sachin_runs / total_runs) * 100
    virat_percentage = (virat_runs / total_runs) * 100

    # Create the figure
    fig = go.Figure()

    # Add Sachin's runs
    fig.add_trace(go.Bar(
        y=attributes,
        x=sachin_percentage,
        name='Sachin Tendulkar',
        orientation='h',
        text=sachin_runs,
        hoverinfo='x+text',
        marker=dict(color='rgba(255, 128, 0, 0.7)')
    ))

    # Add Virat's runs
    fig.add_trace(go.Bar(
        y=attributes,
        x=virat_percentage,
        name='Virat Kohli',
        orientation='h',
        text=virat_runs,
        hoverinfo='x+text',
        marker=dict(color='rgba(0, 128, 255, 0.7)')
    ))

    # Update layout
    fig.update_layout(
        title=f'100% Stacked Bar Chart of {selected_format} Runs: Sachin Tendulkar vs Virat Kohli',
        xaxis=dict(title='Percentage'),
        yaxis=dict(title='Attributes'),
        barmode='stack',
        legend=dict(orientation='h', yanchor='top', y=1.1, xanchor='center', x=0.5)

    )

    return fig

@app.callback(
    Output('bowling-stats', 'figure'),
    Input('Bar-format-radio', 'value')
)
def update_bar_chart2(selected_format):
    url_sachin = "https://www.cricbuzz.com/profiles/25/sachin-tendulkar"
    url_virat = "https://www.cricbuzz.com/profiles/1413/virat-kohli"

    # Read the tables from the URLs
    df_sachin = pd.read_html(url_sachin)[1]
    df_virat = pd.read_html(url_virat)[1]

    # Filter Test data for Sachin and Virat
    sachin_test = filter_data(df_sachin, selected_format).drop(["BBI", "BBM"])
    virat_test = filter_data(df_virat, selected_format).drop(["BBI", "BBM"])

    # Convert all rows in both datasets to float
    sachin_test = sachin_test.apply(pd.to_numeric, errors='coerce')
    virat_test = virat_test.apply(pd.to_numeric, errors='coerce')

    # Handle NaN values if any
    sachin_test.fillna(0, inplace=True)
    virat_test.fillna(0, inplace=True)

    # Add both datasets
    total_matches = sachin_test.add(virat_test, fill_value=0)

    # Calculate percentage of matches played by each player
    sachin_percentage = (sachin_test / total_matches) * 100
    virat_percentage = (virat_test / total_matches) * 100

    fig = go.Figure()
    attributes = sachin_test.index

    # Add Sachin's runs
    fig.add_trace(go.Bar(
        y=attributes,
        x=sachin_percentage,
        name='Sachin Tendulkar',
        orientation='h',
        text=sachin_test,
        hoverinfo='x+text',
        marker=dict(color='rgba(255, 128, 0, 0.7)')
    ))

    # Add Virat's runs
    fig.add_trace(go.Bar(
        y=attributes,
        x=virat_percentage,
        name='Virat Kohli',
        orientation='h',
        text=virat_test,
        hoverinfo='x+text',
        marker=dict(color='rgba(0, 128, 255, 0.7)')
    ))

    # Update layout
    fig.update_layout(
        title=f'100% Stacked Bar Chart of Test Runs: Sachin Tendulkar vs Virat Kohli',
        xaxis=dict(title='Percentage'),
        yaxis=dict(title='Attributes'),
        barmode='stack',
        legend=dict(orientation='h', yanchor='top', y=1.1, xanchor='center', x=0.5)

    )

    return fig


@app.callback(
    Output('line-chart', 'figure'),
    Input('line-format-radio', 'value')
)
def update_line_chart(selected_format):
    # Scrape the data for Sachin Tendulkar (Player ID: 1735) in the selected format
    sachin_df = scrape_player_progress_summary(1735, format=selected_format)
    virat_df = scrape_player_progress_summary(3600, format=selected_format)

    # Extract the 0th and 6th columns for Sachin and Virat
    sachin_match_runs = sachin_df.iloc[:, [6]]
    sachin_match_runs = sachin_match_runs[1:]
    sachin_match_runs.columns = ['Sachin Runs']
    sachin_match_runs['Sachin Runs'] = sachin_match_runs['Sachin Runs'].astype(float)

    # Extract match and runs columns for Virat
    virat_match_runs = virat_df.iloc[:, [6]]
    virat_match_runs.columns = ['Virat Runs']
    virat_match_runs = virat_match_runs[1:]
    virat_match_runs['Virat Runs'] = virat_match_runs['Virat Runs'].astype(float)

    # Merge the two DataFrames based on the 'Match' column
    merged_df = sachin_match_runs.join(virat_match_runs, how='outer')



    # Create a line graph
    fig = go.Figure()
    # Add line trace for Sachin Tendulkar
    fig.add_trace(go.Scatter(x=merged_df.index, y=merged_df['Sachin Runs'], mode='lines', name='Sachin'))
    # Add line trace for Virat Kohli
    fig.add_trace(go.Scatter(x=merged_df.index, y=merged_df['Virat Runs'], mode='lines', name='Virat'))

    # Set the y-axis range to cover the maximum runs scored by both players
    fig.update_layout(title="Sachin Tendulkar vs Virat Kohli Runs Progress",
                      xaxis_title="Match",
                      yaxis_title="Runs")

    return fig

@app.callback(
    [Output('polar-plot-virat', 'figure'),
     Output('polar-plot-sachin', 'figure')],
    [Input('format-radio', 'value')]
)
def update_polar_plots(format):
    fig_virat = generate_figure_virat_polar(format)
    fig_sachin = generate_figure_sachin_polar(format)
    return fig_virat, fig_sachin


@app.callback(
    Output('bubble-map-countrywise', 'figure'),
    Input('map-format-radio', 'value')
)
def update_map(format):    
    # Scrape opponent statistics for Sachin Tendulkar (Player ID: 1735)

    sachin_df = scrape_player_opponents(1735, format=format)
    virat_df = scrape_player_opponents(3600, format=format)

    # Add a 'Player' column to each DataFrame
    sachin_df['Player'] = 'Runs_Sachin'
    virat_df['Player'] = 'Runs_Virat'

    # Combine both dataframes
    df = pd.concat([sachin_df, virat_df])

    # Convert 'Runs' column to numeric
    df['Runs'] = pd.to_numeric(df['Runs'], errors='coerce').fillna(0)

    # Reshape the data
    df = df.pivot_table(index='Versus', columns='Player', values='Runs', aggfunc='sum').reset_index()
    df.columns.name = None  # Remove the columns name

    # If Latitude and Longitude are available, you can merge them with the DataFrame
    latitude_longitude_data = {
        "Versus": ["Australia", "Bangladesh", "Bermuda", "England", "Ireland", "Kenya", "Namibia", "Netherlands",
                "New Zealand", "Pakistan", "South Africa", "Sri Lanka", "United Arab Emirates", "West Indies",
                "Zimbabwe", "Afghanistan", "Nepal"],
        "Latitude": [-25.2744, 23.685, 32.3078, 52.3555, 53.4129, -0.0236, -22.9576, 52.1326,
                    -40.9006, 30.3753, -30.5595, 7.8731, 23.4241, 21.694, -19.0154, 33.9391, 28.3949],
        "Longitude": [133.7751, 90.3563, -64.7505, -1.3465, -8.2439, 37.9062, 18.4904, 5.2913,
                    174.886, 69.3451, 22.9375, 80.7718, 53.8478, -78.3804, 29.1549, 67.7099, 84.124]
    }

    df = pd.merge(df, pd.DataFrame(latitude_longitude_data), on='Versus')
    df.fillna(0, inplace=True)
    df["More_Runs_Player"] = df.apply(lambda row: "Sachin" if row["Runs_Sachin"] >= row["Runs_Virat"] else "Virat", axis=1)
    df["More_Runs"] = df.apply(lambda row: max(row["Runs_Sachin"], row["Runs_Virat"]), axis=1)
    df['hover_text'] = df.apply(lambda row: f"Country: {row['Versus']}, Sachin: {row['Runs_Sachin']}, Virat: {row['Runs_Virat']}", axis=1)

    
    # Plotting bubble map
    fig = px.scatter_geo(df,
                         lat="Latitude",
                         lon="Longitude",
                         hover_name="hover_text",
                         size="More_Runs",
                         color=df['Runs_Sachin'] > df['Runs_Virat'],  # Sachin = True, Virat = False
                         color_discrete_map={True: 'orange', False: 'blue'},
                         projection="natural earth",
                         size_max=50,
                         title="Runs scored against a country")
    fig.for_each_trace(lambda trace: trace.update(name='Sachin' if trace.name == 'True' else 'Virat'))
    return fig

@app.callback(
    Output('radar-chart', 'figure'),
    [Input('radar-chart', 'id')]
)
def update_radar_chart(_):
    angles = np.linspace(0, 360, len(radar_team), endpoint=False)
    angles=np.concatenate((angles,[angles[0]]))
    # Create traces
    trace_sachin = go.Scatterpolar(
        r=Radar_Sachin + [Radar_Sachin[0]],
        theta=angles,
        fill='toself',
        name='Sachin',
        hoverinfo='name+text',
        text=['Against {}: 100s: {}'.format(opponent, val) for opponent, val in zip(radar_team, Radar_Sachin)]
    )
    trace_virat = go.Scatterpolar(
        r=Radar_Virat + [Radar_Virat[0]],
        theta=angles,
        fill='toself',
        name='Virat',
        hoverinfo='name+text',
        text=['Against {}: 100s: {}'.format(opponent, val) for opponent, val in zip(radar_team, Radar_Virat)]
    )

    layout = go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(max(Radar_Sachin), max(Radar_Virat)) + 1]
            ),
            angularaxis=dict(
                tickvals=np.linspace(0, 360, len(radar_team), endpoint=False),
                ticktext=radar_team
            )
        ),
        showlegend=True,
        title="Total number of 100s of Sachin Tendulkar vs Virat Kohli vs opponent team"
    )
    return go.Figure(data=[trace_sachin, trace_virat], layout=layout)

@app.callback(
    Output("bubble-map", "figure"),
    Input('map-format-radio', 'value')
)
def update_bubble_map(format):
    if format == "Test":
        sachin_Test = pd.DataFrame({"Country": ["Australia", "Bangladesh", "England", "India", "New Zealand", "Pakistan", "South Africa", "Sri Lanka", "West Indies", "Zimbabwe"], "Sachin Runs": [1809, 820, 1575, 7216, 842, 483, 1161, 1155, 620, 240]})
        virat_Test = pd.DataFrame({"Country": ["Australia", "Bangladesh", "England", "India", "New Zealand", "South Africa", "Sri Lanka", "West Indies"], "Virat Runs": [1352, 59, 1096, 4144, 252, 891, 394, 660]})
        merged_df = pd.merge(sachin_Test, virat_Test, on="Country", how="outer").fillna(0)
    elif format == "ODI":
        sachin_ODI = pd.DataFrame({"Country": ["Australia", "Bangladesh", "Canada", "England", "India", "Ireland", "Kenya", "Malaysia", "New Zealand", "Pakistan", "Singapore", "South Africa", "Sri Lanka", "U.A.E.", "West Indies", "Zimbabwe"], "Sachin Runs": [1491, 827, 313, 1051, 6976, 204, 171, 222, 821, 480, 253, 1453, 1531, 1778, 282, 573]})
        virat_ODI = pd.DataFrame({"Country": ["Australia", "Bangladesh", "England", "India", "New Zealand", "South Africa", "Sri Lanka", "West Indies", "Zimbabwe"], "Virat Runs": [1327, 1097, 1349, 6268, 596, 993, 1028, 825, 365]})
        merged_df = pd.merge(sachin_ODI, virat_ODI, on="Country", how="outer").fillna(0)
    elif format == "T20":
        virat_T20 = pd.DataFrame({"Country": ["Australia", "Bangladesh", "England", "India", "Ireland", "New Zealand", "South Africa", "Sri Lanka", "U.A.E.", "U.S.A.", "West Indies", "Zimbabwe"], "Virat Runs": [747, 472, 192, 1577, 9, 105, 55, 335, 344, 63, 112, 26]})
        sachin_T20 = pd.DataFrame({"Country": ["South Africa"], "Sachin Runs": [10]})
        merged_df = pd.merge(sachin_T20, virat_T20, on="Country", how="outer").fillna(0)

    latitude_longitude_data = {
        "Country": ["Australia", "Bangladesh", "Bermuda", "England", "Ireland", "Kenya", "Namibia", "Netherlands",
                    "New Zealand", "Pakistan", "South Africa", "Sri Lanka", "United Arab Emirates", "West Indies",
                    "Zimbabwe", "Afghanistan", "Nepal", "USA", "U.A.E.", "India", "Canada", "Malaysia", "Singapore"],
        "Latitude": [-25.2744, 23.685, 32.3078, 52.3555, 53.4129, -0.0236, -22.9576, 52.1326,
                    -40.9006, 30.3753, -30.5595, 7.8731, 23.4241, 21.694, -19.0154, 33.9391, 28.3949,
                    37.0902, 23.4241, 20.5937, 56.1304, 4.2105, 1.3521],
        "Longitude": [133.7751, 90.3563, -64.7505, -1.3465, -8.2439, 37.9062, 18.4904, 5.2913,
                    174.886, 69.3451, 22.9375, 80.7718, 53.8478, -78.3804, 29.1549, 67.7099, 84.124,
                    -95.7129, 53.8478, 78.9629, -106.3468, 101.9758, 103.8198]
    }

    latitude_longitude_data = pd.DataFrame(latitude_longitude_data)

    df = pd.merge(merged_df, latitude_longitude_data, how="inner")
    df["More_Runs_Player"] = df.apply(lambda row: "Sachin" if row["Sachin Runs"] >= row["Virat Runs"] else "Virat", axis=1)
    df["More_Runs"] = df.apply(lambda row: max(row["Sachin Runs"], row["Virat Runs"]), axis=1)
    df['hover_text'] = df.apply(lambda row: f"Country: {row['Country']}, Sachin: {row['Sachin Runs']}, Virat: {row['Virat Runs']}", axis=1)


    fig = px.scatter_geo(df,
                         lat="Latitude",
                         lon="Longitude",
                         hover_name="hover_text",
                         size="More_Runs",
                         color=df['Sachin Runs'] > df['Virat Runs'],  # Sachin = True, Virat = False
                         color_discrete_map={True: 'orange', False: 'blue'},
                         projection="natural earth",
                         size_max=50,
                         title="Runs scored in a country.")
    fig.for_each_trace(lambda trace: trace.update(name='Sachin' if trace.name == 'True' else 'Virat'))
    return fig

@app.callback(
    Output('bowler-dropdown', 'options'),
    Output('bowler-dropdown', 'value'),
    Input('dataset-radio', 'value')
)
def update_dropdown_options(selected_dataset):
    if selected_dataset == 'test':
        bowler_names = test_bowler_names
    else:
        bowler_names = odi_bowler_names
    return [{'label': bowler, 'value': bowler} for bowler in bowler_names], bowler_names[0]

# Define Dash callback to update radar chart based on selected bowler and dataset
@app.callback(
    Output('radar-chart-bowler', 'figure'),
    [Input('bowler-dropdown', 'value'),
     Input('dataset-radio', 'value')]
)
def update_radar_chart(selected_bowler, selected_dataset):
    if selected_dataset == 'test':
        bowler_names = test_bowler_names
        categories = test_categories
        sachin_values = test_sachin_values
        virat_values = test_virat_values
    else:
        bowler_names = odi_bowler_names
        categories = odi_categories
        sachin_values = odi_sachin_values
        virat_values = odi_virat_values

    # Find index of selected bowler
    bowler_index = bowler_names.index(selected_bowler)
    
    # Create radar chart
    fig = go.Figure()

    # Add traces for Sachin Tendulkar and Virat Kohli
    fig.add_trace(go.Scatterpolar(
        r=sachin_values[bowler_index],
        theta=categories,
        fill='toself',
        name=player1_name
    ))
    fig.add_trace(go.Scatterpolar(
        r=virat_values[bowler_index],
        theta=categories,
        fill='toself',
        name=player2_name
    ))

    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                type='log',  # Set radial axis to log scale
                tickvals=[],
                ticktext=[]
            )
        ),
        title=f'Performance Comparison: {player1_name} vs {player2_name} against {selected_bowler} in {selected_dataset.upper()}'
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)