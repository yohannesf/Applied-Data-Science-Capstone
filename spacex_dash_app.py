# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                ],
                                                value='ALL',
                                                placeholder="Select a Launch Site here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def render_pie_chart(selected_launch_site):
    selected_launch_site_df = spacex_df
    if selected_launch_site == 'ALL':
        #return Pie Chart for All Sites
        return px.pie(selected_launch_site_df, values='class', names='Launch Site', title='Total Successful Launches By Site')
       
    else:
        # return a piechart for the selected site
        mask = selected_launch_site_df['Launch Site'] == selected_launch_site

      
        return px.pie(selected_launch_site_df[mask], names='class',
                     title=f'Total Successful Launches For Site {selected_launch_site}')
       

   

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              [Input(component_id='payload-slider', component_property='value')])

def render_scatter_chart(launch_site, payload_slider_value):

   # min_payload = payload_slider_value[0]
   # max_payload =  payload_slider_value[1]
    min_payload_mass = spacex_df['Payload Mass (kg)'] >= float(payload_slider_value[0])
    max_payload_mass = spacex_df['Payload Mass (kg)'] <=  float(payload_slider_value[1])
    
    selected_payload_mass_df = spacex_df[min_payload_mass][max_payload_mass]
    
    if launch_site == 'ALL':

        scatter_chart = px.scatter(selected_payload_mass_df, x='Payload Mass (kg)', y='class', color="Booster Version Category",
                         title=f'Correlation between Payload Mass and Launch Success for All Sites for Payload Mass(kg) Between {payload_slider_value[0]} and {payload_slider_value[1]}')
        return scatter_chart
    else:
        
        
        selected_launch_site = launch_site
        mask = selected_payload_mass_df['Launch Site'] == selected_launch_site
        scatter_chart = px.scatter(selected_payload_mass_df[mask], x='Payload Mass (kg)', y='class', color="Booster Version Category",
                         title=f'Correlation between Payload Mass and Launch Success for Site {selected_launch_site}')
        return scatter_chart

# Run the app
if __name__ == '__main__':
    app.run_server()
