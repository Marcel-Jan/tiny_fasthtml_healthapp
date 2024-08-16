from fasthtml.common import *
from datetime import datetime

app = FastHTML()

# Create a sqlite database for health data
# The table is called items for some reason.
app, rt, healthdata, HealthData = fast_app('/Volumes/backup/sqlite/tinyhealth.db',
                                            id=int,
                                            created_at=str, # I would like this to be a datetime
                                            weight=float,
                                            bmi=float,
                                            pk='id')

@app.get("/")
def home():
    """ home function

    Returns:
        FastHTML: Creates a form to enter weight and bmis
    """
    return Main(P("Welcome to Tiny MyHealthApp!"),
                Form(Input(id="weight", name="weight", type="float", placeholder="Weight"),
                     Input(id="bmi", name="bmi", type="float", placeholder="BMI"),
                     Button("Submit"),
                     action="/", method="post"))

@app.route("/", methods=['post'])
def post(weight:float, bmi:float):
    """ post function

    This inserts the weight and bmi into the database

    Args:
        weight (float): weight of the person (measurement unspecified)
        bmi (float): body mass index of the person

    Returns:
        str: Shows what was entered into the database
    """    
    healthdata.insert(HealthData(weight=weight,
                                 bmi=bmi,
                                 created_at=datetime.now().isoformat()))
    return f"Entered into the database: weight={weight}, bmi={bmi}"


serve()
