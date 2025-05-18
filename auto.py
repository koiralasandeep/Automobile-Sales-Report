import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import ssl

# disable certificate
ssl._create_default_https_context = ssl._create_unverified_context

# Loading the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initializing the Dash app
app = dash.Dash(__name__)

# Setting the title of the dashboard
app.title = "Automobile Statistics Dashboard"

# List of years
year_list = [i for i in range(1980, 2024)]

# Creating the layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}),

    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Yearly Statistics',
            placeholder='Select a report type'
        )
    ]),

    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=2023,  # Default value, change as needed
            placeholder='Select year',
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlignLast': 'center'}
        )
    ]),

    html.Div(id='output-container', className='chart-grid')
])

# Callback to update the disabled state of the select-year dropdown
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    return selected_statistics != 'Yearly Statistics'

# Callback to update the output container based on dropdown selections
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(selected_statistics, selected_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Average Automobile Sales fluctuation over Recession Period
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales over Recession Period")
        )

        # Plot 2: Average Vehicles Sold by Vehicle Type during recession
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', title="Average Vehicles Sold by Vehicle Type")
        )

        return [
            html.Div(className='chart-item', children=[R_chart1]),
            html.Div(className='chart-item', children=[R_chart2])
        ]

    elif selected_statistics == 'Yearly Statistics':
        # Filter data for selected year
        yearly_data = data[data['Year'] == selected_year]

        # Plot 1: Yearly Automobile Sales
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, x='Year', y='Automobile_Sales', title='Yearly Automobile Sales')
        )

        # Plot 2: Total Monthly Automobile Sales
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas, x='Month', y='Automobile_Sales', title='Total Monthly Automobile Sales')
        )

        return [
            html.Div(className='chart-item', children=[Y_chart1]),
            html.Div(className='chart-item', children=[Y_chart2])
        ]

    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
