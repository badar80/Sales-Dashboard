import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

# Load data from CSV file
df = pd.read_csv('business.retailsales.csv')  # Replace with your actual file name

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Sales Dashboard"),

    dcc.Dropdown(
        id='dropdown-product',
        options=[{'label': product, 'value': product} for product in df['Product Type'].unique()],
        value=df['Product Type'].iloc[0]  # Default selected product type
    ),

    dcc.Graph(id='net-quantity-plot'),
    dcc.Graph(id='gross-sales-plot'),
    dcc.Graph(id='discounts-plot'),
    dcc.Graph(id='returns-plot'),
    dcc.Graph(id='total-net-sales-plot'),
])


# Define callback to update plots based on dropdown selection
@app.callback(
    [Output('net-quantity-plot', 'figure'),
     Output('gross-sales-plot', 'figure'),
     Output('discounts-plot', 'figure'),
     Output('returns-plot', 'figure'),
     Output('total-net-sales-plot', 'figure')],
    [Input('dropdown-product', 'value')]
)
def update_graph(selected_product):
    # Filter data for the selected product type
    filtered_df = df[df['Product Type'] == selected_product]

    # Create plots
    net_quantity_plot = {
        'data': [{'x': filtered_df['Net Quantity'], 'type': 'histogram', 'name': 'Net Quantity'}],
        'layout': {'title': 'Net Quantity Distribution'}
    }

    gross_sales_plot = {
        'data': [{'x': filtered_df['Gross Sales'], 'type': 'bar', 'name': 'Gross Sales'}],
        'layout': {'title': 'Gross Sales'}
    }

    discounts_plot = {
        'data': [{'x': filtered_df['Discounts'], 'type': 'bar', 'name': 'Discounts'}],
        'layout': {'title': 'Discounts'}
    }

    returns_plot = {
        'data': [{'x': filtered_df['Returns'], 'type': 'bar', 'name': 'Returns'}],
        'layout': {'title': 'Returns'}
    }

    total_net_sales_plot = {
        'data': [{'x': filtered_df['Total Net Sales'], 'type': 'bar', 'name': 'Total Net Sales'}],
        'layout': {'title': 'Total Net Sales'}
    }

    return net_quantity_plot, gross_sales_plot, discounts_plot, returns_plot, total_net_sales_plot


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
