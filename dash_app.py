"""
Pink Morsel Sales Visualiser
A Dash web application to visualise sales data and answer the business question:
Were sales higher before or after the Pink Morsel price increase on January 15th, 2021?
"""

# Import Dash components for creating the web application
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Import data manipulation and visualisation libraries
import pandas as pd
import plotly.express as px

# Load the processed sales data from the CSV file
df = pd.read_csv('data/processed_sales_data.csv')

# Convert the Date column from string to datetime format for proper sorting
df['Date'] = pd.to_datetime(df['Date'])

# Create the Dash application instance
# __name__ is used to help Dash locate assets and other resources
app = dash.Dash(__name__)

# Define the layout of the web application
# html.Div creates a container element, similar to a div in HTML
app.layout = html.Div([
    # Main container div with styling
    html.Div([
        # Header card containing title and business question
        html.Div([
            html.H1("Pink Morsel Sales Visualiser"),
            html.P("Were sales higher before or after the Pink Morsel price increase on January 15th, 2021?",
                   className="question-text")
        ], className="header-card"),

        # Controls card with region filter radio buttons
        html.Div([
            html.Label("Filter by Region:", className="control-label"),
            dcc.RadioItems(
                id='region-selector',  # Unique identifier for the callback
                options=[
                    {'label': 'All Regions', 'value': 'all'},
                    {'label': 'North', 'value': 'north'},
                    {'label': 'East', 'value': 'east'},
                    {'label': 'South', 'value': 'south'},
                    {'label': 'West', 'value': 'west'}
                ],
                value='all',  # Default selection
                className='dash-radio-items'
            )
        ], className="controls-card"),

        # Graph card containing the line chart
        html.Div([
            dcc.Graph(id='sales-line-chart')  # Interactive Plotly chart
        ], className="chart-card"),

        # Footer
        html.Div([
            html.P("Soul Foods Analytics Dashboard")
        ], className="footer")
    ], className="container")
])

# Define a callback function to update the chart based on region selection
# This callback runs whenever the region radio button selection changes
@app.callback(
    Output('sales-line-chart', 'figure'),  # Component to update (the chart)
    Input('region-selector', 'value')       # Component that triggers the update
)
def update_chart(selected_region):
    """
    Update the line chart based on the selected region.
    
    Args:
        selected_region: The region selected from the radio buttons
                        ('all', 'north', 'east', 'south', 'west')
    
    Returns:
        fig: A Plotly figure object containing the filtered line chart
    """
    # Filter data based on selected region
    if selected_region == 'all':
        # When 'all' is selected, use the entire dataset
        filtered_df = df.copy()
        chart_title = 'Total Daily Sales Over Time (All Regions)'
    else:
        # Filter to only include the selected region
        filtered_df = df[df['Region'] == selected_region].copy()
        chart_title = f'Total Daily Sales Over Time ({selected_region.capitalize()} Region)'
    
    # Group the filtered data by date and sum the sales for each day
    daily_sales = filtered_df.groupby('Date')['Sales'].sum().reset_index()
    
    # Sort the data by date in chronological order
    daily_sales = daily_sales.sort_values('Date')
    
    # Create a line chart using Plotly Express
    fig = px.line(
        daily_sales,
        x='Date',
        y='Sales',
        title=chart_title
    )
    
    # Update the chart layout with axis labels and styling
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Total Sales ($)',
        template='plotly_white',
        title_font_size=18,
        title_x=0.5,  # Centre the title
        hovermode='x unified'  # Show all values on hover at the same x position
    )
    
    # Update line styling
    fig.update_traces(
        line=dict(color='#667eea', width=3),
        marker=dict(size=6)
    )
    
    return fig

# Run the application when this file is executed directly
# __name__ == '__main__' ensures the app only runs when we execute this file,
# not when it's imported as a module
if __name__ == '__main__':
    # Start the Dash development server
    # debug=False disables debug mode for production safety
    app.run(debug=False)
