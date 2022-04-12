import dash
from dash import dcc,html
from dash.dependencies import Input, Output, State



########### Define your variables ######
myheading1='Predicting Home Sale Prices in Ames, Iowa'
image1='ames_welcome.jpeg'
equation='eq.mathml'
tabtitle = 'Ames Housing'
sourceurl = 'http://jse.amstat.org/v19n3/decock.pdf'
githublink = 'https://github.com/amakarewycz/501-linear-reg-ames-housing'


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle



########### Set up the layout
app.layout = html.Div(children=[
    html.H1(myheading1),
    html.Div([
        html.Img(src=app.get_asset_url(image1), style={'width': '30%', 'height': 'auto'}, className='four columns'),
        html.Div([
                html.H3('Features of Home:'),
                html.Div('Year Built:'),
                dcc.Input(id='YearBuilt', value=2010, type='number', min=2006, max=2010, step=1),
                html.Div('Bathrooms:'),
                dcc.Input(id='Bathrooms', value=2, type='number', min=1, max=5, step=1),
                html.Div('Bedrooms:'),
                dcc.Input(id='BedroomAbvGr', value=4, type='number', min=1, max=5, step=1),
                html.Div('Total Square Feet:'),
                dcc.Input(id='TotalSF', value=2000, type='number', min=100, max=5000, step=1),
                html.Div('Single Family Home:'),
                dcc.Input(id='SingleFam', value=0, type='number', min=0, max=1, step=1),
                html.Div('Garage Area:'),
                dcc.Input(id='GarageArea', value=0, type='number', min=0, max=1481, step=1),

            ], className='four columns'),
            html.Div([
                html.Button(children='Submit', id='submit-val', n_clicks=0,
                                style={
                                'background-color': 'red',
                                'color': 'white',
                                'margin-left': '5px',
                                'verticalAlign': 'center',
                                'horizontalAlign': 'center'}
                                ),
                html.H3('Predicted Home Value:'),
                html.Div(id='Results')
            ], className='four columns')
        ], className='twelve columns',
    ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.H4('Regression Equation:'),
    html.Div('Predicted Price = (- $1,154.9K * Baseline) + ($0.6K * Year Built) + ($13.1K * Bathrooms) + (- $7.0K * Bedrooms) + ($0.044K * Total Square Feet) + ($ 22.6K * Single Family Home) + ( $0.049 * Garage Area)'),
#    html.Div([
#    html.Meta(name="viewport",content="width=device-width"),
#    html.Script(src="https://polyfill.io/v3/polyfill.min.js?features=es6"),
#    html.Script(src="ps://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js",id="MathJax-script"), #async=True)
#    html.P('''When \(a \ne 0\), there are two solutions to \(ax^2 + bx + c = 0\) and they are 
 # \[x = {-b \pm \sqrt{b^2-4ac} \over 2a}.\]''')
 #   ]),
    html.Br(),
    html.A('Google Spreadsheet', href='https://docs.google.com/spreadsheets/d/1WlUKALlFqEHA-A9kbyhXzxuHol1AZT-shTQ7uuzob1M/edit#gid=0'),
    html.Br(),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)


######### Define Callback
def ames_lr_function_old(clicks, YearBuilt,Bathrooms,BedroomAbvGr,TotalSF,SingleFam,GarageArea):
    if clicks==0:
        return "waiting for inputs"
    else:
        y = [-1154949.7078 + 593.8959*YearBuilt + 13064.0661*Bathrooms + -7004.9201*BedroomAbvGr + 44.3431*TotalSF+ 22586.4944*SingleFam+ 49.1537*GarageArea]
        formatted_y = "${:,.2f}".format(y[0])
        return formatted_y
    
@app.callback(
    Output(component_id='Results', component_property='children'),
    Input(component_id='submit-val', component_property='n_clicks'),
    State(component_id='YearBuilt', component_property='value'),
    State(component_id='Bathrooms', component_property='value'),
    State(component_id='BedroomAbvGr', component_property='value'),
    State(component_id='TotalSF', component_property='value'),
    State(component_id='SingleFam', component_property='value'),
    State(component_id='GarageArea', component_property='value')
)
def ames_lr_function(clicks,YearBuilt,Bathrooms,BedroomAbvGr,TotalSF,SingleFam,GarageArea):
    print(GarageArea)
    if clicks==0:
        return "waiting for inputs"
    
    if  (GarageArea is None) :
        return "Please provide adequate GarageArea"

    if  (YearBuilt is None) :
        return "Please provide adequate YearBuilt"

    if  (Bathrooms is None) :
        return "Please provide adequate Bathrooms"

    if  (BedroomAbvGr is None) :
        return "Please provide adequate Bedrooms"

    if  (SingleFam is None) :
        return "Please provide adequate SingleFam"

    if  (TotalSF is None) :
        return "Please provide adequate Total Square Feet"

    
    checksum=0
    for var in [YearBuilt,Bathrooms,BedroomAbvGr,TotalSF,SingleFam,GarageArea]:
        if isinstance(var,int)==False:
            checksum+=1
    if (YearBuilt<1900)|(YearBuilt>2020):
        checksum+=1
    if (Bathrooms<1) | (Bathrooms>5):
        checksum+=1
    if (BedroomAbvGr<1) | (BedroomAbvGr>5):
        checksum+=1
    if (TotalSF<100)|(TotalSF>5000):
        checksum+=1
    if (SingleFam!=0) & (SingleFam!=1):
        checksum+=1
    if (GarageArea<0) | (GarageArea>1481):
        checksum+=1
    if checksum>0:
        return "Please provide adequate inputs"
    else:
        y = [-1154949.7078 + 593.8959*YearBuilt + 13064.0661*Bathrooms + -7004.9201*BedroomAbvGr + 44.3431*TotalSF+ 22586.4944*SingleFam+ 49.1537*GarageArea]
#         y = unpickled_model.predict([[YearBuilt,Bathrooms,BedroomAbvGr,TotalSF,SingleFam,LargeNeighborhood]])
        formatted_y = "${:,.2f}".format(y[0])
        return formatted_y 

############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
