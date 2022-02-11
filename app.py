import dash
import base64
from dash.dependencies import Output, Input

#import dash_core_components as dcc
from dash import dcc
from dash import html
#import dash_html_components as html
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
import pandas as pd
import numpy as np

data=pd.read_csv("avocado.csv")
data['Date'] = pd.to_datetime(data["Date"], format="%m/%d/%Y")   
#return render_template('view.html', table=data)
#data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")
#data.sort_values("Date", inplace=True)
#data['Date'] = data.fit_transform(data['Date'].astype(str))
#data['Result'] = data.apply(lambda row: row[row == 1].index.tolist(), axis=1)
#data.loc[data.index.isin(['type','region'])]
#data = data[['type', 'region']]
data=data.query("type == 'conventional' and region == 'Albany'")
#data.loc[(data['type'] == '') & (data['region'] == '')]
#data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")
#data['Date'] = pd.to_datetime(data.Date).dt.strftime("%Y-%m-%d")
data.sort_values("Date", inplace=True)


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server
app.tittle= 'Fuseinidashbaord'


app.layout = html.Div(

    children=[
        html.Div(
            children=[
                
                html.H1(
                    children="Jibril Analytics", className="header-title"
                ),
                html.P(
                    children="Dashboard to showcase output"
                    " and the number of avocados sold in the US"
                    " between 2015 and 2018",
                    className="header-description",
                ),
            ],
            className="header",
            ),

        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Region",className='menu-title'),
                        dcc.Dropdown(
                        	id="region-filter", 
                        	options=[
                        	    {"label": region,"value": region} 
                        	    for region in np.sort(data.region)
                        	], 
                        	value= " ", 
                        	 
                        	className="dropdown"
                        ),
                    ]

                ),

                html.Div(
                    children=[
                        html.Div(children='Types',className='menu-title'),
                        dcc.Dropdown(
                        	id="type-filter", 
                        	options=[
                                {"label": avocado_type,"value": avocado_type} 
                                for avocado_type in data.type.unique()
                        	], 
                        	value= 'conventional', 
                        	clearable=False, 
                        	searchable=True, 
                        	className='dropdown',
                        ),
                    ],

                ),

                html.Div(
                    children=[
                        html.Div(
                        	children='year',
                        	className='menu-title'
                        	),
                        dcc.DatePickerRange(
                        	id='Year', 
                        	min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),

                        ),

                    ]
                    
                ),

            ],

            className='menu',

        ),
        html.Div(
            children=[

                html.Div(
                    children=dcc.Graph(
                    	id='Price-Graph', config={"displayModeBar": False},
                    ),
                    className ='card',
                ),
                        
                
                html.Div(
                    children=dcc.Graph(
                    	id='Volume-Graph', config={"displayModeBar": False},
                    ),
                    className='card',
                ),
            ],
            className ="wrapper",
        ),

    ]

)


@app.callback(
	[Output('Price-Graph', 'figure'),Output('Volume-Graph', 'figure')],

    [   Input('region-filter', 'value'),
        Input('type-filter', 'value'), 
        Input('Year', 'start_date'), 
        Input('Year', 'end_date')
    ],
)


def update_Graph(region,avocado_type, start_date, end_date):
    mask=(
        (data.region==region)
        &(data.type==avocado_type)
        &(data.Date>=start_date)
        &(data.Date<=end_date)
    )
    filtered_data = data.loc[mask, :]
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["AveragePrice"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
    Volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Total Volume"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Total Volume of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }



    return price_chart_figure, Volume_chart_figure

if __name__ == "__main__":
    app.run_server(debug=True)
   #volume_chart_figure = {
    #   "data": [
     #      {
    #            "x": filtered_data["Date"],
    #            "y": filtered_data["Total Volume"],
    #            "type": "lines",
    #            "hovertemplate": "$%{y:.2f}<extra></extra>",
    #        },
    #    ],
    #    "layout": {
    #        "title": {"text": "Total Volume of Avocados", "x": 0.05,"xanchor": "left"},
            
    #       "xaxis": {"fixedrange": True},
    #       "yaxis": {"tickprefix": "$", "fixedrange": True},
    #       "colorway": ["#17B897"],
    #   },
   #}

   
