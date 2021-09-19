import dash
import dash_core_components as dcc
from dash import html
import pandas as pd
from plot_pies import plot_by_district_col
from plot_map import plot_map

districts_keys = pd.read_csv("districts.csv")

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                     html.Div(className='four columns div-user-controls',
                              children=[
                                  html.H2('Las Palmas Tourism'),
                                  html.P('Explore the socioeconomic characteristics'),
                                  html.P('of Las Palmas visitors.'),
                                  html.Div(
                                      children=[
                                          html.Label(['Select district'],
                                                     style={'font-weight': 'bold', "text-align": "center",
                                                            "font-family": "Open Sans Light",
                                                            "font-size": "16px"
                                                            }),
                                          dcc.Dropdown(
                                              id="districts_dropdown",
                                              options=[{"label": name, "value": key} for name, key in
                                                       districts_keys.values],
                                              value=3500101,
                                              clearable=False
                                          )
                                      ],
                                      style={"width": "300px",
                                             "position": "absolute",
                                             "top": "30%",
                                             "backgroundColor": "#95adc4",
                                             "font-family": "Open Sans Light",
                                             "font-size": "16px"
                                             }
                                  ),

                                  html.Div(
                                      children=[
                                          html.Label(['Select year/s'],
                                                     style={'font-weight': 'bold', "text-align": "center",
                                                            "font-family": "Open Sans Light",
                                                            "font-size": "16px"
                                                            }),
                                          dcc.Checklist(
                                              id="years_checklist",
                                              options=[
                                                  {'label': '2018', 'value': 2018},
                                                  {'label': '2019', 'value': 2019},
                                                  {'label': '2020', 'value': 2020}
                                              ],
                                              value=[2019]
                                          )
                                      ],
                                      style={"width": "300px",
                                             "position": "absolute",
                                             "top": "40%",
                                             "backgroundColor": "#95adc4",
                                             "font-family": "Open Sans Light",
                                             "font-size": "16px"
                                             }
                                  ),

                                  html.Div(
                                      children=[
                                          html.Label(['Select month/s'],
                                                     style={'font-weight': 'bold', "text-align": "center",
                                                            "font-family": "Open Sans Light",
                                                            "font-size": "16px"
                                                            }),
                                          dcc.Dropdown(
                                              id="months_checklist",
                                              options=[
                                                  {'label': 'January', 'value': 1},
                                                  {'label': 'February', 'value': 2},
                                                  {'label': 'March', 'value': 3},
                                                  {'label': 'April', 'value': 4},
                                                  {'label': 'May', 'value': 5},
                                                  {'label': 'June', 'value': 6},
                                                  {'label': 'July', 'value': 7},
                                                  {'label': 'August', 'value': 8},
                                                  {'label': 'September', 'value': 9},
                                                  {'label': 'October', 'value': 10},
                                                  {'label': 'November', 'value': 11},
                                                  {'label': 'December', 'value': 12}
                                              ],
                                              value=[7, 8],
                                              multi=True,
                                              clearable=False
                                          )
                                      ],
                                      style={"width": "300px",
                                             "position": "absolute",
                                             "top": "50%",
                                             "backgroundColor": "#95adc4",
                                             "font-family": "Open Sans Light",
                                             "font-size": "16px"
                                             }
                                  ),

                                  html.Div(
                                      children=[
                                          html.Label(['Select visitors type'],
                                                     style={'font-weight': 'bold', "text-align": "center",
                                                            "font-family": "Open Sans Light",
                                                            "font-size": "16px"
                                                            }),
                                          dcc.Checklist(
                                              id="visitors_checklist",
                                              options=[
                                                  {'label': 'Tourist', 'value': "Turista"},
                                                  {'label': 'Excursionist', 'value': "Excursionista"},
                                              ],
                                              value=["Turista", "Excursionista"]
                                          )
                                      ],
                                      style={"width": "300px",
                                             "position": "absolute",
                                             "top": "60%",
                                             "backgroundColor": "#95adc4",
                                             "font-family": "Open Sans Light",
                                             "font-size": "16px"
                                             }
                                  ),

                                  html.Div(
                                      children=[
                                          html.Label(['Select day type'],
                                                     style={'font-weight': 'bold', "text-align": "center",
                                                            "font-family": "Open Sans Light",
                                                            "font-size": "16px"
                                                            }),
                                          dcc.Checklist(
                                              id="day_type_checklist",
                                              options=[
                                                  {'label': 'Weekday', 'value': "Laborable"},
                                                  {'label': 'Weekend', 'value': "Fin Semana"},
                                              ],
                                              value=["Laborable", "Fin Semana"]
                                          )
                                      ],
                                      style={"width": "300px",
                                             "position": "absolute",
                                             "top": "70%",
                                             "backgroundColor": "#95adc4",
                                             "font-family": "Open Sans Light",
                                             "font-size": "16px"}
                                  ),
                                  html.Div(className='eight columns div-for-charts bg-grey',
                                           children=[
                                               dcc.Graph(id='map_plot'),
                                               dcc.Graph(id='pie_plots')
                                           ],
                                           style={"width": "1500px",
                                                  "height": "1000px",
                                                  "position": "absolute",
                                                  "top": "0%",
                                                  "left": "20%",
                                                  "overflow": "scroll"}
                                           )
                              ])
                 ]
                 )
    ]
)


@app.callback(
    dash.dependencies.Output('map_plot', 'figure'),
    [dash.dependencies.Input('years_checklist', 'value'),
     dash.dependencies.Input('months_checklist', 'value'),
     dash.dependencies.Input('visitors_checklist', 'value'),
     dash.dependencies.Input('day_type_checklist', 'value')]
)
def update_map(years, months, visitor_type, day_type):
    map_plotted = plot_map(years, months, visitor_type, day_type)
    map_plotted.show()
    return map_plotted


@app.callback(
    dash.dependencies.Output('pie_plots', 'figure'),
    [dash.dependencies.Input('districts_dropdown', 'value'),
     dash.dependencies.Input('years_checklist', 'value'),
     dash.dependencies.Input('months_checklist', 'value'),
     dash.dependencies.Input('visitors_checklist', 'value'),
     dash.dependencies.Input('day_type_checklist', 'value')]
)
def update_pie_plots(district, years, months, visitor_type, day_type):
    return plot_by_district_col(district, years, months, visitor_type, day_type)


if __name__ == '__main__':
    app.run_server(debug=True, port=3004)
