import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

df_IL_2017 = pd.read_csv('IL_2017.csv')

df_IL_2017.rename(columns={'Partner Name':'Partner_Name','Statement #':'Statement_ID',
                           'Sold Quarter':'Sold_Quarter','Rptd. Customer':'Rptd_Customer', 
                           'Res. Customer':'Res_Customer','Rptd. Item':'Rptd_Item',
                           'Res. Item #':'Res_Item','Rptd. Distributor':'Rptd_Distributor',
                           'Royalty Type':'Royalty_Type'},inplace=True)

df_IL_2017[['Rptd_Customer','Res_Customer']].fillna('Blank', inplace=True)

def cust_status(status):
    Rptd_Customer, Res_Customer, Comments = status
        
    if Rptd_Customer == 'Blank'and Res_Customer == 'Blank':
        return 'Resolved'
    elif Rptd_Customer != 'Blank'and Res_Customer == 'Blank' and Comments == 'Blank':
        return 'Not resolved'
    elif Rptd_Customer != 'Blank'and Res_Customer == 'Blank' and Comments != 'Blank':
        return 'Resolved'
    else:
        return 'Resolved'

df_IL_2017['Res_Cust_Status'] = df_IL_2017[['Rptd_Customer','Res_Customer','Comments']].apply(cust_status, axis=1)



app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=df_IL_2017[df_IL_2017['Res_Cust_Status'] == i]['Sold_Quarter'],
                    y=df_IL_2017[df_IL_2017['Res_Cust_Status'] == i]['Qty'],
                    text=df_IL_2017[df_IL_2017['Res_Cust_Status'] == i]['Partner_Name'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df_IL_2017.Res_Cust_Status.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'Sold Quarter'},
                yaxis={'title': 'Quantity'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])


if __name__ == '__main__':
    app.run_server()