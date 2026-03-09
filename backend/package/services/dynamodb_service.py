import boto3
from datetime import datetime

# Initialize DynamoDB resource
dynamodb = boto3.resource("dynamodb")

# Table name
TABLE_NAME = "complaints"

table = dynamodb.Table(TABLE_NAME)



def insert_complaint(item: dict):

    try:
        import random
        
        # Ensure beneficiary_id is always present
        beneficiary_id = item.get("beneficiary_id")
        if not beneficiary_id or beneficiary_id == "UNKNOWN":
            beneficiary_id = f"BEN-{random.randint(100000, 999999)}"
            print(f"Generated fallback beneficiary_id in insert_complaint: {beneficiary_id}")

        db_item = {
            "complaint_id": item["complaint_id"],
            "beneficiary_id": beneficiary_id,
            "description": item.get("description"),
            "audio_url": item.get("audio_url"),
            "report_url": item.get("report_url"),
            "transcription_job": item.get("transcription_job"),
            "status": item.get("status", "pending"),
            "created_at": item.get("created_at", datetime.utcnow().isoformat())
        }

        table.put_item(Item=db_item)
        
        # Log for verification
        print(f"✅ DynamoDB insert successful: {db_item['complaint_id']} with beneficiary_id: {db_item['beneficiary_id']}")

        return db_item

    except Exception as e:
        print(f" DynamoDB insert failed: {str(e)}")
        raise Exception(f"DynamoDB insert failed: {str(e)}")

        