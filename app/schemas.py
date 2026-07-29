from pydantic import BaseModel


class InspectionResponse(BaseModel):
    status: str
    confidence: float
    detected_object: str