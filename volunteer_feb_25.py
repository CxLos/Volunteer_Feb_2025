# =================================== IMPORTS ================================= #
import csv, sqlite3
import numpy as np 
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
import plotly.figure_factory as ff
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
from folium.plugins import MousePosition
import plotly.express as px
import datetime
import folium
import os
import sys
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.development.base_component import Component
# 'data/~$bmhc_data_2024_cleaned.xlsx'
# print('System Version:', sys.version)
# -------------------------------------- DATA ------------------------------------------- #

current_dir = os.getcwd()
current_file = os.path.basename(__file__)
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = 'data/Volunteer_Responses.xlsx'
file_path = os.path.join(script_dir, data_path)
data = pd.read_excel(file_path)
df = data.copy()

# Trim leading and trailing whitespaces from column names
df.columns = df.columns.str.strip()

# Trim whitespace from values in all columns
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Define a discrete color sequence
# color_sequence = px.colors.qualitative.Plotly

# Filtered df where 'Date of Activity:' is in December
df['Date of Activity'] = pd.to_datetime(df['Date of Activity'], errors='coerce')
df = df[df['Date of Activity'].dt.month == 2]

# print(df.head(10))
# print('Total Marketing Events: ', len(df))
print('Column Names: \n', df.columns.to_list())
# print('DF Shape:', df.shape)
# print('Dtypes: \n', df.dtypes)
# print('Info:', df.info())
# print("Amount of duplicate rows:", df.duplicated().sum())

# print('Current Directory:', current_dir)
# print('Script Directory:', script_dir)
# print('Path to data:',file_path)

# ================================= Columns ================================= #

Columns = [
'Timestamp', 'Date of Activity', 'Activity status:', 'Person Submitting Form', 'Project Name:', 'Role:', 'Describe the software used:', 'What is the annual subscription cost for this software (if known):', 'Are there any associated licensing fees?', 'If yes, specify the cost and details:', 'Estimated savings from using this software (e.g. developer costs avoided):', 'What is the name of the project related to this contribution?', 
'Briefly Describe the contributions:', 
'Estimated direct costs for this project (if applicable):', 
'Estimated labor hours contributed (if applicable):', 
'Describe the work performed by students or volunteers:', 'Number of students/volunteers involved:', 
'Total hours contributed this month:', 
'Entity affiliated with (school, organization):',
'Estimated dollar value of the work (e.g., hourly rate × hours worked):', 
'Any additional details or clarifications regarding the contribution?', 'Activity duration (minutes):', 
'Purpose of the activity (please only list one):', 
'Brief description of activity:'
    ] 



# =============================== Missing Values ============================ #

# missing = df.isnull().sum()
# print('Columns with missing values before fillna: \n', missing[missing > 0])

# ============================== Data Preprocessing ========================== #

# Check for duplicate columns
# duplicate_columns = df.columns[df.columns.duplicated()].tolist()
# print(f"Duplicate columns found: {duplicate_columns}")
# if duplicate_columns:
#     print(f"Duplicate columns found: {duplicate_columns}")

# ========================= Total Developments ========================== #

# Total number of engagements:
total_developments = len(df)

# -------------------------- Development Hours -------------------------- #

# Sum of 'Activity Duration (minutes):' dataframe converted to hours:
dev_hours = df['Activity duration (minutes):'].sum()/60
dev_hours = round(dev_hours)

# =================== Total Existing Partner Meetings =================== #

df_existing_partner_meetings = df['Number of Existing Partner Meetings:'].sum()
print('Total Existing Partner Meetings:', df_existing_partner_meetings)

# =================== Total New Partner Meetings =================== #

df_new_partner_meetings = df['Number of New Partnership Meetings:'].sum()
print('Total New Partner Meetings:', df_new_partner_meetings)

# =================== Total Number of New Partners =================== #

df_new_partners = df['Number of New Partners:'].sum()
print('Total New Partners:', df_new_partners)

# =================== Total Outreach Calls =================== #

df_outreach_calls = df['Number of Outreach Calls:'].sum()
print('Total Outreach Calls:', df_outreach_calls)

# =================== Total Outreach Emails =================== #

df_outreach_emails = df['Number of Outreach Emails:'].sum()
print('Total Outreach Emails:', df_outreach_emails)

# =================== Total Grants Searched =================== #

df_grants_searched = df['Number of Grants Searched:'].sum()
print('Total Grants Searched:', df_grants_searched)

# =================== Total Grants Applied =================== #

df_grants_applied = df['Number of Grants Applied:'].sum()
print('Total Grants Applied:', df_grants_applied)

# =========== Total Other Funding Opportunitites Searched ============ #

df_funding_searched = df['Number of Other Funding Opportunities Searched:'].sum()
print("Total Funding Sea", df_funding_searched)

# =========== Total Other Funding Opportunities Applied ============ #

df_funding_applied = df['Number of Other Funding Opportunities Applied:'].sum()
print("Total Funding Applied", df_funding_applied)

# =================== Total Community Events Attended =================== #

df_community_events = df['Number of Community Events Attended:'].sum()
print('Total Community Events Attended:', df_community_events)

# =================== Total CRM Updates =================== #

df_crm_updates = df['Number of CRM Updates:'].sum()
print('Total CRM Updates:', df_crm_updates)

# --------------------- Activity Status --------------------- #

# "Activity Status" dataframe:
df_activity_status = df.groupby('Activity Status').size().reset_index(name='Count')

status_bar=px.bar(
    df_activity_status,
    x='Activity Status',
    y='Count',
    color='Activity Status',
    text='Count',
).update_layout(
    height=460, 
    width=780,
    title=dict(
        text='Activity Status',
        x=0.5, 
        font=dict(
            size=25,
            family='Calibri',
            color='black',
            )
    ),
    font=dict(
        family='Calibri',
        size=18,
        color='black'
    ),
    xaxis=dict(
        tickangle=0,  # Rotate x-axis labels for better readability
        tickfont=dict(size=18),  # Adjust font size for the tick labels
        title=dict(
            # text=None,
            text="Status",
            font=dict(size=20),  # Font size for the title
        ),
        # showticklabels=False  # Hide x-tick labels
        showticklabels=True  # Hide x-tick labels
    ),
    yaxis=dict(
        title=dict(
            text='Count',
            font=dict(size=20),  # Font size for the title
        ),
    ),
    legend=dict(
        # title='Support',
        title_text='',
        orientation="v",  # Vertical legend
        x=1.05,  # Position legend to the right
        y=1,  # Position legend at the top
        xanchor="left",  # Anchor legend to the left
        yanchor="top",  # Anchor legend to the top
        # visible=False
        visible=True
    ),
    hovermode='closest', # Display only one hover label per trace
    bargap=0.08,  # Reduce the space between bars
    bargroupgap=0,  # Reduce space between individual bars in groups
).update_traces(
    textposition='auto',
    hovertemplate='<b>Status:</b> %{label}<br><b>Count</b>: %{y}<extra></extra>'
)

# Person Pie Chart
status_pie=px.pie(
    df_activity_status,
    names="Activity Status",
    values='Count'  # Specify the values parameter
).update_layout(
    title='Activity Status',
    title_x=0.5,
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    )
).update_traces(
    rotation=0,
    textposition='auto',
    textinfo='value+percent',
    hovertemplate='<b>%{label} Status</b>: %{value}<extra></extra>',
)

# ========================= Select Activity ========================== #

# Unique values:
# print(df['Select Activity:'].unique())

# Replace values in 'Select Activity:' column
df['Select Activity:'] = (
    df['Select Activity:']
    .str.strip()
    .replace(
        {"Outreach": "Outreach", 
        "Partnership": "Partnership", 
        "Grants": "Grants",
        "Funding": "Funding",
        "Community": "Community",
        "CRM": "CRM"}
    )
)

# Group by 'Select Activity:' column
df_activity = df.groupby('Select Activity:').size().reset_index(name='Count')

# Bar Chart
activity_bar=px.bar(
    df_activity,
    x='Select Activity:',
    y='Count',
    color='Select Activity:',
    text='Count',
).update_layout(
    height=460,
    width=780,
    title=dict(
        text='Activity Type',
        x=0.5,
        font=dict(

            size=25,
            family='Calibri',
            color='black',
            )
    ),
    font=dict(
        family='Calibri',
        size=18,
        color='black'
    ),
    xaxis=dict(
        tickangle=-15,  # Rotate x-axis labels for better readability
        tickfont=dict(size=18),  # Adjust font size for the tick labels
        title=dict(
            # text=None,
            text="Activity",
            font=dict(size=20),  # Font size for the title
        ),
        showticklabels=False  # Hide x-tick labels
        # showticklabels=True  # Hide x-tick labels
    ),
    yaxis=dict(
        title=dict(
            text='Count',
            font=dict(size=20),  # Font size for the title
        ),
    ),
    legend=dict(
        # title='Support',
        title_text='',  # Title of the legend   
        orientation="v",  # Vertical legend
        x=1.05,  # Position legend to the right
        y=1,  # Position legend at the top
        xanchor="left",  # Anchor legend to the left
        yanchor="top",  # Anchor legend to the top
        # visible=False
        visible=True
    ),
    hovermode='closest', # Display only one hover label per trace
    bargap=0.08,  # Reduce the space between bars
    bargroupgap=0,  # Reduce space between individual bars in groups
).update_traces(
    textposition='auto',
    hovertemplate='<b>Activity:</b> %{label}<br><b>Count</b>: %{y}<extra></extra>'
)

# Activity Pie Chart
activity_pie=px.pie(
    df_activity,
    names="Select Activity:",
    values='Count'  # Specify the values parameter
).update_layout(
    title='Activity Type Distribution',
    title_x=0.5,
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    )
).update_traces(
    rotation=0,
    textposition='auto',
    textinfo='value+percent',
    hovertemplate='<b>%{label} Activity</b>: %{value}<extra></extra>',
)

# ------------------------ Person Submitting Form -------------------- #

#  Unique values:



# df['Person submitting this form:'] = (
#     df['Person submitting this form:']
#     .str.strip()
#     .replace(
#         {"Larry Wallace Jr": "Larry Wallace Jr.", 
#         "Antonio Montggery": "Antonio Montgomery"}
#     )
# )

df_person = df.groupby('Person submitting this form:').size().reset_index(name='Count')
# print(person_group.value_counts())

person_bar=px.bar(
    df_person,
    x='Person submitting this form:',
    y='Count',
    color='Person submitting this form:',
    text='Count',
).update_layout(
    height=460, 
    width=780,
    title=dict(
        text='People Submitting Forms',
        x=0.5, 
        font=dict(
            size=25,
            family='Calibri',
            color='black',
            )
    ),
    font=dict(
        family='Calibri',
        size=18,
        color='black'
    ),
    xaxis=dict(
        tickangle=-15,  # Rotate x-axis labels for better readability
        tickfont=dict(size=18),  # Adjust font size for the tick labels
        title=dict(
            # text=None,
            text="Name",
            font=dict(size=20),  # Font size for the title
        ),
        showticklabels=False  # Hide x-tick labels
        # showticklabels=True  # Hide x-tick labels
    ),
    yaxis=dict(
        title=dict(
            text='Count',
            font=dict(size=20),  # Font size for the title
        ),
    ),
    legend=dict(
        # title='Support',
        title_text='',
        orientation="v",  # Vertical legend
        x=1.05,  # Position legend to the right
        y=1,  # Position legend at the top
        xanchor="left",  # Anchor legend to the left
        yanchor="top",  # Anchor legend to the top
        # visible=False
        visible=True
    ),
    hovermode='closest', # Display only one hover label per trace
    bargap=0.08,  # Reduce the space between bars
    bargroupgap=0,  # Reduce space between individual bars in groups
).update_traces(
    textposition='auto',
    hovertemplate='<b>Name:</b> %{label}<br><b>Count</b>: %{y}<extra></extra>'
)

# Person Pie Chart
person_pie=px.pie(
    df_person,
    names="Person submitting this form:",
    values='Count'  # Specify the values parameter
).update_layout(
    title='Ratio of People Filling Out Forms',
    title_x=0.5,
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    )
).update_traces(
    rotation=0,
    textposition='auto',
    textinfo='value+percent',
    hovertemplate='<b>%{label} Status</b>: %{value}<extra></extra>',
)

# # ========================== DataFrame Table ========================== #

# Engagement Table
dev_table = go.Figure(data=[go.Table(
    # columnwidth=[50, 50, 50],  # Adjust the width of the columns
    header=dict(
        values=list(df.columns),
        fill_color='paleturquoise',
        align='center',
        height=30,  # Adjust the height of the header cells
        # line=dict(color='black', width=1),  # Add border to header cells
        font=dict(size=12)  # Adjust font size
    ),
    cells=dict(
        values=[df[col] for col in df.columns],
        fill_color='lavender',
        align='left',
        height=25,  # Adjust the height of the cells
        # line=dict(color='black', width=1),  # Add border to cells
        font=dict(size=12)  # Adjust font size
    )
)])

dev_table.update_layout(
    margin=dict(l=50, r=50, t=30, b=40),  # Remove margins
    height=700,
    # width=1500,  # Set a smaller width to make columns thinner
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
    plot_bgcolor='rgba(0,0,0,0)'  # Transparent plot area
)

# ============================== Dash Application ========================== #

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    children=[ 
        html.Div(
            className='divv', 
            children=[ 
                html.H1('Business Development Report', className='title'),
                html.H1('February 2025', className='title2'),
                html.Div(
                    className='btn-box', 
                    children=[
                        html.A(
                            'Repo',
                            href='https://github.com/CxLos/Bus_Dev_Feb_2025',
                            className='btn'
                        )
                    ]
                )
            ]
        ),
        
        # # Data Table
        # html.Div(
        #     className='row0',
        #     children=[
        #         html.Div(
        #             className='table',
        #             children=[
        #                 html.H1(
        #                     className='table-title',
        #                     children='Business Development Data Table'
        #                 )
        #             ]
        #         ),
        #         html.Div(
        #             className='table2', 
        #             children=[
        #                 dcc.Graph(
        #                     className='data',
        #                     figure=dev_table
        #                 )
        #             ]
        #         )
        #     ]
        # ),

        html.Div(
            className='row1',
            children=[
                html.Div(
                    className='graph11',
                    children=[
                        html.Div(className='high1', 
                                 children=['Total Developments']),
                        html.Div(
                            className='circle1',
                            children=[
                                html.Div(
                                    className='hilite',
                                    children=[html.H1(className='high2', 
                                                      children=[total_developments])]
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='graph22',
                    children=[
                        html.Div(className='high3', children=['Development Hours']),
                        html.Div(
                            className='circle2',
                            children=[
                                html.Div(
                                    className='hilite',
                                    children=[html.H1(className='high4', children=[dev_hours])]
                                )
                            ]
                        ) 
                    ]
                )
            ]
        ),

        html.Div(
            className='row1',
            children=[
                html.Div(
                    className='graph11',
                    children=[
                        html.Div(className='high1', 
                                 children=['Existing Partner Meetings']),
                        html.Div(
                            className='circle1',
                            children=[
                                html.Div(
                                    className='hilite',
                                    children=[html.H1(className='high2', 
                                                      children=[df_existing_partner_meetings])]
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='graph22',
                    children=[
                        html.Div(className='high3', children=['New Partner Meetings']),
                        html.Div(
                            className='circle2',
                            children=[
                                html.Div(
                                    className='hilite',
                                    children=[html.H1(className='high4', 
                                                      children=[df_new_partner_meetings])]
                                )
                            ]
                        ) 
                    ]
                )
            ]
        ),

        html.Div(
            className='row1',
            children=[
                html.Div(
                    className='graph11',
                    children=[
                        html.Div(className='high1', 
                                 children=['New Partners']),
                        html.Div(
                            className='circle1',
                            children=[
                                html.Div(
                                    className='hilite',
                                    children=[html.H1(className='high2', 
                                                      children=[df_new_partners])]
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='graph22',
                    children=[
                        html.Div(className='high3', children=['Blank']),
                        html.Div(
                            className='circle2',
                            children=[
                                html.Div(
                                    className='hilite',
                                    children=[html.H1(className='high4', children=[])]
                                )
                            ]
                        ) 
                    ]
                )
            ]
        ),

        html.Div(
            className='row1',
            children=[
                html.Div(
                    className='graph11',
                    children=[
                        html.Div(className='high1', 
                                 children=['Outreach Calls']),
                        html.Div(
                            className='circle1',
                            children=[
                                html.Div(
                                    className='hilite',
                                    children=[html.H1(className='high2', 
                                                      children=[df_outreach_calls])]
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='graph22',
                    children=[
                        html.Div(className='high3', children=['Outreach Emails']),
                        html.Div(
                            className='circle2',
                            children=[
                                html.Div(
                                    className='hilite',
                                    children=[html.H1(className='high4', children=[df_outreach_emails])]
                                )
                            ]
                        ) 
                    ]
                )
            ]
        ),

        html.Div(
            className='row1',
            children=[
                html.Div(
                    className='graph11',
                    children=[
                        html.Div(className='high1', 
                                 children=['Grants Searched']),
                        html.Div(
                            className='circle1',
                            children=[
                                html.Div(
                                    className='hilite',
                                    children=[html.H1(className='high2', 
                                                      children=[df_grants_searched])]
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='graph22',
                    children=[
                        html.Div(className='high3', children=['Grants Applied']),
                        html.Div(
                            className='circle2',
                            children=[
                                html.Div(
                                    className='hilite',
                                    children=[html.H1(className='high4', children=[df_grants_applied])]
                                )
                            ]
                        ) 
                    ]
                )
            ]
        ),

        html.Div(
            className='row1',
            children=[
                html.Div(
                    className='graph11',
                    children=[
                        html.Div(className='high1', 
                                 children=['Funding Opportunities Searched']),
                        html.Div(
                            className='circle1',
                            children=[
                                html.Div(
                                    className='hilite',
                                    children=[html.H1(className='high2', 
                                                      children=[df_funding_searched])]
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='graph22',
                    children=[
                        html.Div(className='high3', children=['Funding Opportunitites Applied']),
                        html.Div(
                            className='circle2',
                            children=[
                                html.Div(
                                    className='hilite',
                                    children=[html.H1(className='high4', children=[df_funding_applied])]
                                )
                            ]
                        ) 
                    ]
                )
            ]
        ),

        html.Div(
            className='row1',
            children=[
                html.Div(
                    className='graph11',
                    children=[
                        html.Div(className='high1', 
                                 children=['Commuminity Events Attended']),
                        html.Div(
                            className='circle1',
                            children=[
                                html.Div(
                                    className='hilite',
                                    children=[html.H1(className='high2', 
                                                      children=[df_community_events])]
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='graph22',
                    children=[
                        html.Div(className='high3', children=['CRM Updates']),
                        html.Div(
                            className='circle2',
                            children=[
                                html.Div(
                                    className='hilite',
                                    children=[html.H1(className='high4', children=[df_crm_updates])]
                                )
                            ]
                        ) 
                    ]
                )
            ]
        ),

        html.Div(
            className='row3',
            children=[
                html.Div(
                    className='graph1',
                    children=[
                        dcc.Graph(
                            figure=status_bar
                        )
                    ]
                ),
                html.Div(
                    className='graph2',
                    children=[
                        dcc.Graph(
                            figure=status_pie
                        )
                    ]
                )
            ]
        ),   

        html.Div(
            className='row3',
            children=[
                html.Div(
                    className='graph1',
                    children=[
                        dcc.Graph(
                            figure=activity_bar
                        )
                    ]
                ),
                html.Div(
                    className='graph2',
                    children=[
                        dcc.Graph(
                            figure=activity_pie
                        )
                    ]
                )
            ]
        ),   

        html.Div(
            className='row3',
            children=[
                html.Div(
                    className='graph1',
                    children=[
                        dcc.Graph(
                            figure=person_bar
                        )
                    ]
                ),
                html.Div(
                    className='graph2',
                    children=[
                        dcc.Graph(
                            figure=person_pie
                        )
                    ]
                )
            ]
        ),   
])

print(f"Serving Flask app '{current_file}'! 🚀")

if __name__ == '__main__':
    app.run_server(debug=True)
                #    False)
# =================================== Updated Database ================================= #

# updated_path = 'data/bus_dev_feb_2025.xlsx'
# data_path = os.path.join(script_dir, updated_path)
# df.to_excel(data_path, index=False)
# print(f"DataFrame saved to {data_path}")

# updated_path1 = 'data/service_tracker_q4_2024_cleaned.csv'
# data_path1 = os.path.join(script_dir, updated_path1)
# df.to_csv(data_path1, index=False)
# print(f"DataFrame saved to {data_path1}")

# -------------------------------------------- KILL PORT ---------------------------------------------------

# netstat -ano | findstr :8050
# taskkill /PID 24772 /F
# npx kill-port 8050

# ---------------------------------------------- Host Application -------------------------------------------

# 1. pip freeze > requirements.txt
# 2. add this to procfile: 'web: gunicorn impact_11_2024:server'
# 3. heroku login
# 4. heroku create
# 5. git push heroku main

# Create venv 
# virtualenv venv 
# source venv/bin/activate # uses the virtualenv

# Update PIP Setup Tools:
# pip install --upgrade pip setuptools

# Install all dependencies in the requirements file:
# pip install -r requirements.txt

# Check dependency tree:
# pipdeptree
# pip show package-name

# Remove
# pypiwin32
# pywin32
# jupytercore

# ----------------------------------------------------

# Name must start with a letter, end with a letter or digit and can only contain lowercase letters, digits, and dashes.

# Heroku Setup:
# heroku login
# heroku create mc-impact-11-2024
# heroku git:remote -a mc-impact-11-2024
# git push heroku main

# Clear Heroku Cache:
# heroku plugins:install heroku-repo
# heroku repo:purge_cache -a mc-impact-11-2024

# Set buildpack for heroku
# heroku buildpacks:set heroku/python

# Heatmap Colorscale colors -----------------------------------------------------------------------------

#   ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
            #  'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
            #  'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
            #  'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
            #  'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
            #  'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
            #  'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
            #  'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',
            #  'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
            #  'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',
            #  'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar',
            #  'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
            #  'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid',
            #  'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',
            #  'ylorrd'].

# rm -rf ~$bmhc_data_2024_cleaned.xlsx
# rm -rf ~$bmhc_data_2024.xlsx
# rm -rf ~$bmhc_q4_2024_cleaned2.xlsx