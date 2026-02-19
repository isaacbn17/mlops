from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    subject: str = Field(default="", description="Email subject line")
    email_to: str = Field(default="", description="Recipient email address")
    email_from: str = Field(default="", description="Sender email address")
    message: str = Field(default="", description="Raw email message (may include MIME)")

class PredictResponse(BaseModel):
    label: str = Field(description="Predicted class label, e.g., 'spam' or 'ham'")
    score: float = Field(ge=0.0, le=1.0, description="Confidence score in [0,1]")

