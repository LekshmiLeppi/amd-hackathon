
from pydantic import BaseModel
from typing import List

class RuleResult(BaseModel):
    rule_id:str
    status:str
    confidence:float
    evidence:str

class ValidationResponse(BaseModel):
    document_name:str
    compliance_score:float
    findings:List[RuleResult]
