from firebase_credentials import cred
from firebase_admin import firestore
from aiogram.types import Message, InputMedia, file, user
import firebase_admin

app = firebase_admin.initialize_app(cred)
db = firestore.client()

def write_row(user_id:str, message:Message, file_url:str):

    file_id = message.video.file_id

    if file_id is None:
        return
    
    _write_user(user_id, file_id)
    _write_file(file_id, file_url)

def _write_user(user_id:int, file_id:int):

    data = {
        u'file_ids' : [file_id]
    }

    ref = db.collection(u'users').document(str(user_id))
    doc = ref.get()

    if doc.exists == False:
        ref.set(data)
        return

    doc_dict = doc.to_dict()

    media_ids = doc_dict[u'file_ids']
    media_ids.append(file_id)
    data['file_ids'] = media_ids

    ref.update(data)

def _write_file(file_id:int, file_url:str):
    ref = db.collection(u'files').document(str(file_id))
    doc = ref.get()

    if doc.exists == True:
        return
    
    data = {
        'file_id' : file_id,
        'file_url' : file_url
    }

    ref.set(data)
