# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
# Read the airline data into pandas dataframe
spacex_df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv ")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
# Create a dash application
app = dash.Dash(__name__)
# Create an app layout
app.layout = html.Div(
  children=[html.H1('SpaceX Launch Records Dashboard',
               style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
              # TASK 1: Add a dropdown list to enable Launch Site selection
              # The default select value is for ALL sites
                
                dcc.Dropdown(id='site-dropdown',
                    options=[{'label':'All Sites', 'value':'ALL'},
                    {'label':'CCAFS LC-40','value':'CCAFS LC-40'},{'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                    {'label':'KSC LC-39A','value':'KSC LC-39A'},{'label':'VAFB SLC-4E','value':'VAFB SLC-4E'}],
                             placeholder="Select a Launch Site",
                             searchable=True ),
                    
                html.Br(),
                 html.Div(dcc.Graph(id='pie'))
  ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `pie' as output
# Function decorator to specify function input and output
@app.callback(
  Output(component_id='pie', component_property='figure'),
  [Input(component_id='site-dropdown', component_property='value')]
)            
def get_pie_chart(entered_site):
  filtered_df = spacex_df
  if entered_site == 'ALL':
    fig = px.pie(spacex_df, values='class', names='Launch Sites',title='Success for all Sites')
    return fig
  else:
      # return the outcomes piechart for a selected site
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    filtered_df1=filtered_df.groupby() ['Launch Site', 'class'].size().reset_index(name='class count')
    fig = px.pie(filtered_df1,values='class count', names='class',
     title="Total Success Launches for site"+entered_site)
    return fig


# Run the app
if __name__ == '__main__':
  app.run_server()
 


