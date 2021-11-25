import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

# TODO handle this
firebase_config_path = 'firebase_config.json'

class Firebase():
    def __init__(self) -> None:
        pass

    def getClient(firebase_config_path):
        cred = credentials.Certificate(firebase_config_path)
        firebase_admin.initialize_app(cred)
        return firestore.client()
        
    
    async def upload_to_firestore(rows: list, target_date: datetime.date, firestore_client):
        target_date_str = target_date.strftime("%Y%m%d")
        #Group 500 each
        split_count = 0
        row_list = []
        while len(rows) > 500:
            split_count += 1
            row_list.append(rows[:500])
            rows = rows[500:]
        row_list.append(rows)

        doc_ref = firestore_client.collection("stock").document("price").collection(target_date_str)

        batch = firestore_client.batch()

        for group in row_list:
            for r in group:
                res = r.to_dict()
                batch.set(doc_ref.document(res['isu']), res)
            batch.commit()