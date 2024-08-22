""" A tiny health app to demonstrate the use of FastHTML
Starts a web server that allows you to enter weight and bmi data into a database.
This version runs without live coding with fast_app. But here I have more
control over table names.
"""
from fasthtml.common import *
from datetime import datetime

app = FastHTML()

db_local = 'data/tinyhealth.db'
db = database(db_local)
# Create a sqlite database for health data
healthdata = db.t.healthdata
if healthdata not in db.t:
    healthdata.create(id=int,
                      created_at=datetime,
                      weight=float,
                      bmi=float,
                      pk='id')
Healthdata = healthdata.dataclass()

@app.get("/")
def home():
    """ home function

    Returns:
        FastHTML: Creates a form to enter weight and bmis.
        It will go to the "saved" page to show the results.
    """
    return Main(P("Welcome to Tiny Health App!"),
                Form(Input(id="weight", name="weight", type="float", placeholder="Weight"),
                     Input(id="bmi", name="bmi", type="float", placeholder="BMI"),
                     Button("Submit"),
                     action="/saved", method="post"))

@app.route("/saved", methods=['post'])
def post(healthmeasurement:Healthdata):
    """ post function
    This inserts healthdata (the weight and bmi) into the database

    Args:
        dataclass: healthmeasurement. This is a dataclass that has the fields
        weight and bmi.
    Returns:
        FastHTML: Shows what was entered into the database.
        It will go back to the form page so you can enter more data.
    """
    healthmeasurement.created_at = datetime.now().isoformat()
    healthdata.insert(healthmeasurement)
    return Main(P(f"Entered into the database: {healthmeasurement}"),
                Form(Button("Back"),
                action="/", method="get")
                )

serve()
