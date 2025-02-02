## Importing dependencies

import dash
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import altair as alt
import vega_datasets
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
alt.data_transformers.disable_max_rows()

## Initating the app

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server

## Objects creation 

description_df = pd.read_excel("data/lab4_drug-description.xlsx", sheet_name = 'lab4_drug-description') # importing the data 

pivoted_data = pd.read_csv("data/2012-2018_lab4_data_drug-overdose-deaths-connecticut-wrangled-pivot.csv") # importing the data

base_drug = 'Heroin' # making the deafult selection

number_of_people, size_table = pivoted_data.shape

def make_demographics(drug_name = base_drug):
    """
    Contains the mds theme and creates two bar plots relating the age and the gender of the victims to the specific drug
    and returns two plots age and gender 

    Parameters
    ----------
    drug_name : Chosen from from the dropdown menu
        
    Returns
    -------
    Plots: age | gender
    

    Examples
    --------
    >>> make_demographics(drug_name = 'Heroin')
    """
    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300, 
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0, 
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 0, 
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)", 
                    # titles are by default vertical left of axis so we need to hack this 
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels 
                },
            }
                }

    # Register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)

    # Enable the newly registered theme
    alt.themes.enable('mds_special')
    
    # Creat plots
    sub_data = pivoted_data.query("Sex == 'Male' | Sex == 'Female'")
    if drug_name == 'Everything':
        query = sub_data
    else:
        query = sub_data.query(drug_name + ' == 1')
    chart = alt.Chart(query)
    age = chart.mark_bar(color = "#3f7d4e").encode(
        x = alt.X("Age:Q", title = "Age", bin=alt.Bin(maxbins=10), axis=alt.AxisConfig(labelAngle=-45)),
        y = 'count()'
    ).properties(title='Age distribution for ' + drug_name, width=290, height=200)
    gender = chart.mark_bar().encode(
        x = alt.X("Sex:N", title = "Sex", axis=alt.AxisConfig(labelAngle=-45)),
        y='count()',
        color = alt.Color('Sex:N', scale=alt.Scale(scheme='viridis'),legend=None)
    ).properties(title='Gender distribution for ' + drug_name, width=190, height=200)
    return (age | gender)


def make_race(drug_name = base_drug): 
    """
    Ceates bar plot relating the race of the victims to the specific drug
    and returns bar plot race 

    Parameters
    ----------
    drug_name : Chosen from from the dropdown menu
        
    Returns
    -------
    Plots: race
    

    Examples
    --------
    >>> ake_demographics(drug_name = 'Heroin')
    """
    if drug_name == 'Everything':
        query = pivoted_data
    else:
        query = pivoted_data.query(drug_name + ' == 1')
    race = alt.Chart(query).mark_bar().encode(
        x = alt.X("Race:N", title = "Race", axis=alt.AxisConfig(labelAngle=-45)),
        y='count()',
        color = alt.Color('Race:N', scale=alt.Scale(scheme='viridis'),legend=None)
    ).properties(title='Race distribution for ' + drug_name, width=400, height=180) 
    return race

overdose_title = html.H3("Accidental overdose victims by drugs type ",className="uppercase title",)
overdose_title_span = html.Span("A dashboard showing deaths by accidental overdose in Connecticut from 2012 to 2018")
overdose_combination_chart = html.Iframe(sandbox='allow-scripts',
                                            id='plot',
                                            height='650',
                                            width='800',
                                            style={'border-width': '0px'},
                                            srcDoc=open('code/532_graph_overdose-count-by-2-drugs.html').read()
                                            )
overdose_dropdown_1 =   dcc.Dropdown(
                            id="drug1_dropdown",
                            value=base_drug,
                            options=[{"label": i, "value": i} for i in description_df['Drug']],
                        )

overdose_dropdown_race = dcc.Dropdown(
                                        id='dd-chart-race',
                                        options=[
                                        {'label': 'Black', 'value': 'Black'},
                                        {'label': 'White', 'value': 'White'},
                                        {'label': 'Asian, Other', 'value': 'Asian, Other'},
                                        {'label': 'Hispanic, White', 'value': 'Hispanic, White'},
                                        {'label': 'No description', 'value': 'No description'},
                                        {'label': 'Asian Indian', 'value': 'Asian Indian'},
                                        {'label': 'Hispanic, Black', 'value': 'Hispanic, Black'},
                                        {'label': 'Unknown', 'value': 'Unknown'},
                                        {'label': 'Other', 'value': 'Other'},
                                        {'label': 'Chinese', 'value': 'Chinese'},
                                        {'label': 'Native American, Other', 'value': 'Native American, Other'},
                                        {'label': 'Everything', 'value': 'Everything'}

                                     ], value='Everything' )

overdose_dropdown_place = dcc.Dropdown(
                                         id='dd-chart-place',
                                         options=[
                                        {'label': 'Hospital', 'value': 'Hospital'},
                                        {'label': 'Residence', 'value': 'Residence'},
                                        {'label': 'Other', 'value': 'Other'},
                                        {'label': 'Nursing Home', 'value': 'Nursing Home'},
                                        {'label': 'No description', 'value': 'No description'},
                                        {'label': 'Convalescent Home', 'value': 'Convalescent Home'},
                                        {'label': 'Hospice', 'value': 'Hospice'},
                                        {'label': 'Everything', 'value': 'Everything'}
                 
                                    ],  value='Everything')

main_text = 'From 2012 to 2018, '+ str(number_of_people) +' deaths occurred due to accidental overdose in Connecticut. This dashboard was created with the intent to provide a visual representation of the crisis'


def set_image(drug = base_drug):
    """
    Ceates image link for the specific drug chosen from the dropdown menu
    
    Returns
    -------
    Image : img_link
    """
    img_link = description_df.loc[description_df['Drug'] == drug, 'Link'].iloc[0]
    return img_link

def set_description(drug = base_drug):
    """
    Ceates drug description for the specific drug chosen from the dropdown menu
    
    Returns
    -------
    Text : drug_description
    """
    drug_description = description_df.loc[description_df['Drug'] == drug, 'Description'].iloc[0] 
    return drug_description

def set_reference(drug = base_drug):
    """
    Ceates drug drug link for the specific drug chosen from the dropdown menu
    
    Returns
    -------
    Link: drug_link
    """
    drug_link = description_df.loc[description_df['Drug'] == drug, 'Reference'].iloc[0] 
    return drug_link

## Displacement Creation
overdose_displacement = html.Div([
                                    dbc.Row([   
                                        dbc.Col( width=2),
                                        dbc.Col([
                                            dbc.Jumbotron([
                                                html.H1("Overdash"),
                                                overdose_title, 
                                                overdose_title_span])], width = 8),
                                        dbc.Col(width=2)
                                    ]),
                                    dbc.Row([
                                        dbc.Col(width=2),
                                        dbc.Col([
                                            dbc.Row([html.P(main_text, id="problem_desc")]),
                                            dbc.Row()
                                            ], width = 8),
                                        dbc.Col(width=2)       
                                    ]),                                 
                                
                                    dbc.Row([
                                            dbc.Col(width = 3),
                                            dbc.Col([html.H3('The Killers'), overdose_combination_chart], width = 7),
                                            dbc.Col(width = 3)
                                    ]),
                                    dbc.Row([
                                        dbc.Col(width=2),
                                        dbc.Col([html.H3('The Victims')], width = 6),
                                        dbc.Col(width=2)
                                    ]),
                                    dbc.Row([
                                        dbc.Col(width=2),
                                        dbc.Col([html.P('This section shows the social demographic effected by the selected drug')], width = 6),
                                        dbc.Col(width=1)
                                    ]),
                                    dbc.Row([
                                        dbc.Col(width = 2),
                                        dbc.Col([overdose_dropdown_1,
                                                    html.Img(
                                                        id="drug_img",
                                                        src=set_image(),
                                                        height = '150',
                                                        width = '200'
                                                        ),
                                                    html.P(set_description(), id="drug_desc"),
                                                    html.A(   
                                                        'This info was retrieved from drugbank.ca',
                                                        id="drug_ref",
                                                        href=set_reference(),
                                                        target="_blank"
                                                        )
                                                    ], width = 3),
                                        dbc.Col([
                                            dbc.Row([html.Iframe(
                                                    sandbox='allow-scripts',
                                                    id='plot_demog',
                                                    height='400',
                                                    width='1500',
                                                    style={'border-width': '0'},
                                                    srcDoc = make_demographics().to_html()
                                                ),
                                            dbc.Row([
                                                    dbc.Col(width=2),
                                                    dbc.Col([html.Iframe(
                                                            sandbox='allow-scripts',
                                                            id='plot_race',
                                                            height='300',
                                                            width='800',
                                                            style={'border-width': '0'},
                                                            srcDoc =make_race().to_html()
                                                            )], width = 4),
                                                    dbc.Col(width=2)
                                                ])
                                            ])
                                        ], width = 6)
                                    ])
                                ])
                  

## layout of the app
app.layout = dbc.Container([overdose_displacement], fluid= True)

## callback section
@app.callback(
    dash.dependencies.Output('drug_img', 'src'),
    [dash.dependencies.Input('drug1_dropdown', 'value')])
def update_img(drug_name):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_img = set_image(drug_name)
    return updated_img

@app.callback(
    dash.dependencies.Output('drug_desc', 'children'),
    [dash.dependencies.Input('drug1_dropdown', 'value')])
def update_text(drug_name):
    '''
    Updates set_description function with the new drug_name entered by the user
    '''
    updated_text = set_description(drug_name)
    return updated_text

@app.callback(
    dash.dependencies.Output('plot_demog', 'srcDoc'),
    [dash.dependencies.Input('drug1_dropdown', 'value')])
def update_plot_demog(drug_name):
    '''
    Updates make_demographics function with the new drug_name entered by the user
    '''
    updated_plot = make_demographics(drug_name).to_html()
    return updated_plot

@app.callback(
    dash.dependencies.Output('plot_race', 'srcDoc'),
    [dash.dependencies.Input('drug1_dropdown', 'value')])
def update_plot_race(drug_name):
    '''
    Updates make_race function with the new drug_name entered by the user
    '''
    updated_plot = make_race(drug_name).to_html()
    return updated_plot

@app.callback(
    dash.dependencies.Output('drug_ref', 'href'),
    [dash.dependencies.Input('drug1_dropdown', 'value')])
def update_link(drug_name):
    '''
    Updates  set_reference function with the new drug_name entered by the user
    '''
    updated_link = set_reference(drug_name)
    return updated_link

if __name__ == '__main__':
    app.run_server(debug=True)
