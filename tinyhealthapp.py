""" A tiny health app to demonstrate the use of FastHTML
Starts a web server that allows you to enter weight and bmi data into a database.
"""
from fasthtml.common import *
from datetime import datetime

app = FastHTML()

db_local = 'data/tinyhealth.db'
# Create a sqlite database for health data
# The table is called items for some reason.
app, rt, healthdata, HealthData = fast_app( db_file=db_local,
                                            id=int,
                                            created_at=datetime,
                                            weight=float,
                                            bmi=float,
                                            pk='id')

@app.get("/")
def home():
    """ home function

    Returns:
        FastHTML: Creates a form to enter weight and bmis.
        It will go to the "saved" page to show the results.
    """
    return Main(P("Welcome to Tiny MyHealthApp!"),
                Form(Input(id="weight", name="weight", type="float", placeholder="Weight"),
                     Input(id="bmi", name="bmi", type="float", placeholder="BMI"),
                     Button("Submit"),
                     action="/saved", method="post"))

@app.route("/saved", methods=['post'])
def post(weight:float, bmi:float):
    """ post function
    This inserts the weight and bmi into the database

    Args:
        weight (float): weight of the person (measurement unspecified)
        bmi (float): body mass index of the person

    Returns:
        FastHTML: Shows what was entered into the database.
        It will go back to the form page so you can enter more data.
    """
    healthdata.insert(HealthData(weight=weight,
                                 bmi=bmi,
                                 created_at=datetime.now().isoformat()))
    return Main(P(f"Entered into the database: weight={weight}, bmi={bmi}"),
                Form(Button("Back"),
                action="/", method="get")
                )

serve()
