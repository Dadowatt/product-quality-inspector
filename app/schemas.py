from pydantic import BaseModel


# ==========================
# Réponse du diagnostic
# ==========================

class InspectionResponse(BaseModel):
    status: str
    confidence: float
    anomaly_score: float