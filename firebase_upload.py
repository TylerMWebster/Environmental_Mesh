from google.cloud import firestore
import os, datetime
import pandas as pd

TIME_BTW_MEASUREMENTS = 600 # Ten minutes
TIME_COL = "time"
PROJECT_NAME = "espa-d378b"
COLLECTION_NAME = u"temp_data"
SECRET_KEY_LOC = "secrets/espa-d378b-c9dfaae64401.json"
FILENAME = "09_08_2021_14.csv"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SECRET_KEY_LOC
db = firestore.Client(project=PROJECT_NAME)

collection = db.collection(COLLECTION_NAME)

# Read csv data
df = pd.read_csv(f"data/{FILENAME}")

# Get list of sensor ids from data frame
sensor_ids = [id for id in df.columns if id != TIME_COL]

for timestamp in range(0, df[TIME_COL].size, TIME_BTW_MEASUREMENTS):
    upload_dict = {}
    for id in sensor_ids:
        upload_dict["sensor_id"] = str.strip(id)
        upload_dict["temp"] = df[id][timestamp]
        upload_dict["time"] = datetime.datetime.fromtimestamp(df[TIME_COL][timestamp])
        collection.add(upload_dict)
        print(f"{upload_dict['sensor_id']} - {upload_dict['temp']} - {upload_dict['time']}")
