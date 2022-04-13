import dash
from dash import dcc,html
from dash.dependencies import Input, Output, State



########### Define your variables ######
myheading1='Predicting Price of an Avocado'
image1='ames_welcome.jpeg'
equation='eq.mathml'
tabtitle = 'Avocados'
sourceurl = 'https://www.kaggle.com/datasets/neuromusic/avocado-prices'
githublink = 'https://github.com/amakarewycz/501-linear-reg-ames-housing'


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

#<img src="https://partycity6.scene7.com/is/image/PartyCity/_pdp_sq_?$_500x500_$&amp;$product=PartyCity/P890643" alt="Avocado Sombrero Costume for Dogs Image #1" class="loaded" data-was-processed="true">


########### Set up the layout
app.layout = html.Div(children=[
    html.H1(myheading1),
    html.Div([
        html.Img(src="https://partycity6.scene7.com/is/image/PartyCity/_pdp_sq_?$_500x500_$&$product=PartyCity/P890643", style={'width': '30%', 'height': 'auto'}, className='four columns'),
        html.Div([
                html.H3('Features of Avocado Purchase:'),
                html.Div('Year:'),
                dcc.Input(id='Year', value=2018, type='number', min=2015, max=2018, step=1),
                html.Div('Month:'),
                dcc.Input(id='Month', value=2, type='number', min=1, max=12, step=1),
                html.Div('Type:'),
                dcc.Dropdown( ['Organic','Conventional'], 'Organic',id='Type'),
                html.Div('Region:'),
                dcc.Dropdown( ['San Francisco','Albany','Spokane'], 'San Francisco',id='Region'),

            ], className='four columns'),
            html.Div([
                html.Button(children='Submit', id='submit-val', n_clicks=0,
                                style={
                                'background-color': 'green',
                                'color': 'white',
                                'margin-left': '5px',
                                'verticalAlign': 'center',
                                'horizontalAlign': 'center'}
                                ),
                html.H3('Predicted Avocado Price:'),
                html.Div(id='Results')
            ], className='four columns')
        ], className='twelve columns',
    ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.H4('Regression Equation:'),
    html.Div('Predicted Price = -138.26 + 0.0693*Year + 0.0257*Month + 0.28*TypeOrganic + -0.28*TypeConventional+ 0.147*RegionSanFrancisco+ 0.0002*RegionAlbany + -0.1472*RegionSpokane'),
    html.Br(),
    html.A('Google Spreadsheet', href='https://docs.google.com/spreadsheets/d/1mudmrJsmSq5UE93rLkgvOYfRxC19s9hYlCjFavoVbeU/edit#gid=0'),
    html.Br(),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)


######### Define Callback
    
@app.callback(
    Output(component_id='Results', component_property='children'),
    Input(component_id='submit-val', component_property='n_clicks'),
    State(component_id='Year', component_property='value'),
    State(component_id='Month', component_property='value'),
    State(component_id='Type', component_property='value'),
    State(component_id='Region', component_property='value'),
)
def onehotencode(clicks,Year,Month,Type,Region):
    RegionSanFrancisco=0

    RegionSpokane=0

    RegionAlbany=0

    TypeOrganic = 1 if Type == "Organic" else 0
    TypeConventional = not TypeOrganic
    if Region == "San Franciso":
        RegionSanFrancisco = 1
        RegionSpokane = 0
        RegionAlbany = 0
    if Region == "Albany":
        RegionSanFrancisco = 0
        RegionSpokane = 0
        RegionAlbany = 1
    if Region == "Spokane":
        RegionSanFrancisco = 0
        RegionSpokane = 1
        RegionAlbany = 0
    return ames_lr_function(clicks,Year,Month,TypeOrganic,TypeConventional,RegionSanFrancisco,RegionAlbany,RegionSpokane)


def ames_lr_function(clicks,Year,Month,TypeOrganic,TypeConventional,RegionSanFrancisco,RegionAlbany,RegionSpokane):

    if clicks==0:
        return "waiting for inputs"
    
    if  (Year is None) :
        return "Please provide adequate Year"

    if  (Month is None) :
        return "Please provide adequate Month"

    if  (TypeOrganic is None) :
        return "Please provide adequate TypeOrganic"

    if  (TypeConventional is None) :
        return "Please provide adequate TypeConventional"

    if  (RegionSanFrancisco is None) :
        return "Please provide adequate RegionSanFrancisco"

    if  (RegionAlbany is None) :
        return "Please provide adequate RegionAlbany"

    if  (RegionSpokane is None) :
        return "Please provide adequate RegionSpokane"

    
    checksum=0
    for var in [Year,Month,TypeOrganic,TypeConventional,RegionSanFrancisco,RegionAlbany,RegionSpokane]:
        if isinstance(var,int)==False:
            checksum+=1
    if (Year<2015)|(Year>2018):
        checksum+=1
    if (Month<1) | (Month>12):
        checksum+=1
    if checksum>0:
        return "Please provide adequate inputs"
    else:
        y = [-138.26 + 0.0693*Year + 0.0257*Month + 0.28*TypeOrganic + -0.28*TypeConventional+ 0.147*RegionSanFrancisco+ 0.0002*RegionAlbany +-0.1472*RegionSpokane]
#         y = unpickled_model.predict([[YearBuilt,Bathrooms,BedroomAbvGr,TotalSF,SingleFam,LargeNeighborhood]])
        formatted_y = "${:,.2f}".format(y[0])
        return formatted_y 
############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
