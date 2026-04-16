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

# Group the data by date and sum the sales for each day
# This gives us total daily sales across all regions
daily_sales = df.groupby('Date')['Sales'].sum().reset_index()

# Sort the data by date in chronological order
daily_sales = daily_sales.sort_values('Date')

# Create the Dash application instance
# __name__ is used to help Dash locate assets and other resources
app = dash.Dash(__name__)

# Define the layout of the web application
# html.Div creates a container element, similar to a div in HTML
app.layout = html.Div([
    # Main header for the page
    html.H1("Pink Morsel Sales Visualiser", style={'textAlign': 'center'}),
    
    # Subheading that poses the key business question
    # The style centres the text and sets a grey colour
    html.H3("Were sales higher before or after the Pink Morsel price increase on January 15th, 2021?",
            style={'textAlign': 'center', 'color': '#666'}),
    
    # dcc.Graph creates an interactive Plotly chart component
    # The id allows us to reference this chart in callbacks
    dcc.Graph(id='sales-line-chart')
])

# Define a callback function to update the chart
# A callback is triggered when a component's property changes
@app.callback(
    Output('sales-line-chart', 'figure'),  # What to update (the chart's figure)
    Input('sales-line-chart', 'id')         # What triggers the update (chart id change)
)
def update_chart(_):
    """
    Create and return a line chart showing daily sales over time.
    
    Args:
        _: Unused input parameter (callback requires an input)
    
    Returns:
        fig: A Plotly figure object containing the line chart
    """
    # Create a line chart using Plotly Express
    # x-axis: Date of the sale
    # y-axis: Total sales amount
    fig = px.line(
        daily_sales,
        x='Date',
        y='Sales',
        title='Total Daily Sales Over Time'
    )
    
    # Update the chart layout with axis labels and styling
    fig.update_layout(
        xaxis_title='Date',       # Label for the x-axis
        yaxis_title='Total Sales ($)',  # Label for the y-axis with currency
        template='plotly_white'   # Use a clean white background template
    )
    
    return fig

# Run the application when this file is executed directly
# __name__ == '__main__' ensures the app only runs when we execute this file,
# not when it's imported as a module
if __name__ == '__main__':
    # Start the Dash development server
    # debug=False disables debug mode for production safety
    app.run(debug=False)
