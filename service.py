import logging

from google.cloud import firestore

from config.database import db
from model import StudentInfo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def save_to_firestore(doc_id: str, std_num: str, std: StudentInfo = None):
    if not doc_id and std:
        db.collection("registrations").add(
            std.to_dict()
            | {"stdNo": int(std_num), "createdAt": firestore.SERVER_TIMESTAMP}
        )
    else:
        doc_ref = db.collection("registrations").document(doc_id)
        doc_ref.update({"stdNo": int(std_num), "createdAt": firestore.SERVER_TIMESTAMP})
    logger.info(f"Updated student number for {doc_id} to {std_num}")
