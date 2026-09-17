"""
Data models and schemas for the Veridian IT Support Service Agent.
Strictly grounded in Veridian Corp policies and historical ticket records.
"""
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ActionType(str, Enum):
    DIRECT_RESOLVE = "DIRECT_RESOLVE"          # Self-service or immediate procedural resolution
    ROUTE_TO_HUMAN = "ROUTE_TO_HUMAN"          # Dispatched to human IT support technician
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"      # Requires Manager, Security, or Finance approval
    ESCALATE_SECURITY = "ESCALATE_SECURITY"    # Critical security incident (phishing/malware)
    REQUEST_CLARIFICATION = "REQUEST_CLARIFICATION"  # Under-specified / ambiguous input


class TargetDepartment(str, Enum):
    EMPLOYEE_SELF_SERVICE = "Employee Self-Service"
    IT_SERVICE_DESK = "IT Service Desk"
    IT_HARDWARE = "IT Hardware Support"
    IT_SECURITY = "IT Security"
    FINANCE = "Finance & Assets"
    NETWORK_INFRASTRUCTURE = "Network Infrastructure"


class PolicyItem(BaseModel):
    id: str
    title: str
    category: str
    department: str
    summary: str
    full_text: str
    approval_required: bool = False
    approval_conditions: Optional[str] = None
    approval_department: Optional[str] = None
    approval_workflow: Optional[List[str]] = None
    self_service_available: bool = False
    sla: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    issued_by: Optional[str] = None
    standard_cycle_years: Optional[float] = None
    minimum_service_years: Optional[float] = None


class EmployeeRequest(BaseModel):
    id: str
    employee: str
    email: str
    date_opened: str
    request: str
    initial_action_so_far: str
    relevant_kb: List[str] = Field(default_factory=list)
    expected_action: Optional[str] = None
    expected_department: Optional[str] = None
    precedent_ticket: Optional[str] = None


class TicketRecord(BaseModel):
    id: str
    employee: str
    issue_summary: str
    status: str
    is_active: bool
    actionable: bool
    policy_mapping: Optional[str] = None
    recommended_routing: Optional[str] = None
    precedent_takeaway: Optional[str] = None


class TriageResult(BaseModel):
    request_id: Optional[str] = None
    employee: Optional[str] = None
    action_type: ActionType
    target_department: TargetDepartment
    policy_citations: List[str] = Field(default_factory=list)
    precedent_citations: List[str] = Field(default_factory=list)
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    user_message: str
    internal_notes: str
    safety_warning: Optional[str] = None
    sla_estimate: Optional[str] = None
    conflict_reconciliation: Optional[str] = None
    grounded_facts: List[str] = Field(default_factory=list)
    requires_approval_from: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
