from google.cloud import firestore
import os, datetime

PROJECT_NAME = "espa-d378b"
COLLECTION_NAME = u"temp_data"
SECRET_KEY_LOC = "secrets/espa-d378b-c9dfaae64401.json"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SECRET_KEY_LOC
db = firestore.Client(project=PROJECT_NAME)

collection = db.collection(COLLECTION_NAME)

a = input("Query (id/time/temp): ")

if (a == "id"):
    query_sensor_id = u"2843ad924d2001b5"
    docs = collection.where(u"sensor_id", u"==", query_sensor_id).stream()
elif (a == "time"):
    query_time = datetime.datetime.fromtimestamp(1631149683.0848386)
    docs = collection.where(u"time", u">=", query_time).stream()
elif (a == "temp"):
    query_temp = 78
    docs = collection.where(u"temp", u">=", query_temp).stream()

for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")