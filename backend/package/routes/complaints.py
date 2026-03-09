from fastapi import APIRouter, HTTPException
from models.schemas import ComplaintCreate, Complaint
from services.dynamodb import ComplaintDB
from ai_models.complaint_analyzer import complaint_analyzer
from datetime import datetime

router = APIRouter()

@router.post("/complaints", response_model=dict)
async def submit_complaint(complaint: ComplaintCreate):
    """Submit a new complaint"""
    try:
        import random
        
        # Analyze complaint text
        analysis = complaint_analyzer.analyze(complaint.description)
        
        # Generate fallback beneficiary_id if missing
        beneficiary_id = (
            complaint.subject_beneficiary_id or 
            analysis.get('extracted_beneficiary_id') or 
            f"BEN-{random.randint(100000, 999999)}"
        )
        
        # Create complaint data
        complaint_data = {
            'complaint_type': complaint.complaint_type,
            'description': complaint.description,
            'subject_beneficiary_id': beneficiary_id,  # Always set this
            'location': complaint.location.dict(),
            'urgency_score': analysis['urgency_score'],
            'sentiment_score': analysis['sentiment_score'],
            'submitter_name': complaint.submitter_name,
            'submitter_phone': complaint.submitter_phone,
            'is_anonymous': complaint.is_anonymous
        }
        
        # Save to database
        complaint_id = ComplaintDB.create(complaint_data)
        
        # Log for verification
        print(f"✅ Complaint submitted: {complaint_id} with beneficiary_id: {beneficiary_id}")
        
        return {
            'complaint_id': complaint_id,
            'beneficiary_id': beneficiary_id,
            'status': 'submitted',
            'urgency_score': analysis['urgency_score'],
            'predicted_type': analysis['predicted_type'],
            'message': 'Complaint submitted successfully'
        }
    
    except Exception as e:
        print(f"❌ Complaint submission error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/complaints", response_model=list)
async def get_complaints():
    """Get all complaints"""
    try:
        complaints = ComplaintDB.get_all()
        
        # Ensure beneficiary_id is always present in response
        for complaint in complaints:
            # Map subject_beneficiary_id to beneficiary_id for consistency
            if 'subject_beneficiary_id' in complaint and 'beneficiary_id' not in complaint:
                complaint['beneficiary_id'] = complaint['subject_beneficiary_id']
            
            # Fallback if still missing
            if not complaint.get('beneficiary_id'):
                complaint['beneficiary_id'] = 'N/A'
            
            # Parse location if it's a JSON string
            if isinstance(complaint.get('location'), str):
                try:
                    import json
                    complaint['location'] = json.loads(complaint['location'])
                except:
                    pass
        
        print(f"✅ Retrieved {len(complaints)} complaints")
        return complaints
    except Exception as e:
        print(f" Get complaints error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/complaints/{complaint_id}")
async def get_complaint(complaint_id: str):
    """Get complaint by ID"""
    try:
        complaints = ComplaintDB.get_all()
        complaint = next((c for c in complaints if c['complaint_id'] == complaint_id), None)
        
        if not complaint:
            raise HTTPException(status_code=404, detail="Complaint not found")
        
        # Ensure beneficiary_id is present
        if 'subject_beneficiary_id' in complaint and 'beneficiary_id' not in complaint:
            complaint['beneficiary_id'] = complaint['subject_beneficiary_id']
        
        if not complaint.get('beneficiary_id'):
            complaint['beneficiary_id'] = 'N/A'
        
        # Parse location if it's a JSON string
        if isinstance(complaint.get('location'), str):
            try:
                import json
                complaint['location'] = json.loads(complaint['location'])
            except:
                pass
        
        return complaint
    except HTTPException:
        raise
    except Exception as e:
        print(f" Get complaint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
