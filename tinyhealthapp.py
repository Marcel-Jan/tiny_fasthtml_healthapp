from fasthtml.common import *
from datetime import datetime

app = FastHTML()


app, rt, healthdata, HealthData = fast_app('/Volumes/backup/sqlite/tinyhealth.db', 
                                            id=int,
                                            created_at=str,
                                            weight=float,
                                            bmi=float,
                                            pk='id')

@app.get("/")
def home():
    return Main(P("Welcome to Tiny MyHealthApp!"),
                Form(Input(id="weight", name="weight", type="float", placeholder="Weight"),
                     Input(id="bmi", name="bmi", type="float", placeholder="BMI"),
                     Button("Submit"),
                     action="/", method="post"))

@app.route("/", methods=['post'])
def post(weight:float, bmi:float):
    healthdata.insert(HealthData(weight=weight,
                                 bmi=bmi,
                                 created_at=datetime.now().isoformat()))
    return f"Entered into the database: weight={weight}, bmi={bmi}"


serve()
