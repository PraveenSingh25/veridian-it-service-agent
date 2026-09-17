"""
Knowledge Base and Ticket Store for Veridian Corp IT Support Agent.
Loads grounded policies, historical precedents, and employee requests.
"""
import json
import os
from typing import List, Dict, Optional
from engine.models import PolicyItem, EmployeeRequest, TicketRecord


class KBStore:
    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_dir, "data")
        
        self.data_dir = data_dir
        self.policies: Dict[str, PolicyItem] = {}
        self.requests: Dict[str, EmployeeRequest] = {}
        self.tickets: Dict[str, TicketRecord] = {}
        self._load_data()

    def _load_data(self):
        # Load policies
        pol_path = os.path.join(self.data_dir, "policies.json")
        with open(pol_path, "r", encoding="utf-8") as f:
            raw_policies = json.load(f)["policies"]
            for p in raw_policies:
                item = PolicyItem(**p)
                self.policies[item.id] = item

        # Load employee requests
        req_path = os.path.join(self.data_dir, "employee_requests.json")
        with open(req_path, "r", encoding="utf-8") as f:
            raw_requests = json.load(f)
            for r in raw_requests:
                item = EmployeeRequest(**r)
                self.requests[item.id] = item

        # Load ticket history
        tk_path = os.path.join(self.data_dir, "ticket_history.json")
        with open(tk_path, "r", encoding="utf-8") as f:
            raw_tickets = json.load(f)
            for t in raw_tickets:
                item = TicketRecord(**t)
                self.tickets[item.id] = item

    def get_policy(self, policy_id: str) -> Optional[PolicyItem]:
        return self.policies.get(policy_id)

    def get_all_policies(self) -> List[PolicyItem]:
        return list(self.policies.values())

    def get_request(self, request_id: str) -> Optional[EmployeeRequest]:
        return self.requests.get(request_id)

    def get_all_requests(self) -> List[EmployeeRequest]:
        return list(self.requests.values())

    def get_ticket(self, ticket_id: str) -> Optional[TicketRecord]:
        return self.tickets.get(ticket_id)

    def get_all_tickets(self) -> List[TicketRecord]:
        return list(self.tickets.values())

    def get_active_tickets(self) -> List[TicketRecord]:
        return [t for t in self.tickets.values() if t.is_active]

    def get_closed_tickets(self) -> List[TicketRecord]:
        return [t for t in self.tickets.values() if not t.is_active]

    def search_policies(self, query: str) -> List[PolicyItem]:
        """Strict keyword and token matching grounded in the policies."""
        q_tokens = set(query.lower().replace("-", " ").replace("_", " ").split())
        scored: List[tuple[int, PolicyItem]] = []
        for p in self.policies.values():
            score = 0
            for kw in p.keywords:
                if kw in query.lower():
                    score += 3
            # check tokens in full text
            full_lower = p.full_text.lower()
            for token in q_tokens:
                if len(token) > 3 and token in full_lower:
                    score += 1
            if score > 0:
                scored.append((score, p))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored]
