from google.cloud import firestore
import os

PROJECT_NAME = "espa-d378b"
COLLECTION_NAME = u"temp_data"
SECRET_KEY_LOC = "secrets/espa-d378b-c9dfaae64401.json"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SECRET_KEY_LOC
db = firestore.Client(project=PROJECT_NAME)

collection = db.collection(COLLECTION_NAME)

docs = collection.stream()

#print(docs)

#u_sure = input(f"Are you sure you want to delete all documents in {COLLECTION_NAME}? (y/N)")

for doc in docs:
    doc.reference.delete()
