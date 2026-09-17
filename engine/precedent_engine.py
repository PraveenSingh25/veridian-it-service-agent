"""
Precedent Matching and Consistency Engine for Veridian Corp IT Support Agent.
Maintains historical alignment with past ticket decisions (TK-1042 to TK-1051).
"""
from typing import List, Optional, Tuple
from engine.models import TicketRecord
from engine.kb_store import KBStore


class PrecedentEngine:
    def __init__(self, kb_store: Optional[KBStore] = None):
        self.kb_store = kb_store or KBStore()

    def find_matching_precedents(self, text: str, policy_ids: List[str]) -> List[TicketRecord]:
        """
        Finds relevant historical tickets that serve as precedent for the incoming request.
        Uses policy mappings, issue summaries, and topic overlap.
        """
        all_tickets = self.kb_store.get_all_tickets()
        matched: List[Tuple[int, TicketRecord]] = []
        text_lower = text.lower()

        for tk in all_tickets:
            score = 0
            
            # Policy intersection match
            if tk.policy_mapping:
                for pid in policy_ids:
                    if pid in tk.policy_mapping:
                        score += 5

            # Keyword matches in issue summary
            summary_lower = tk.issue_summary.lower()
            if "laptop" in text_lower and "laptop" in summary_lower:
                score += 4
            if "vpn" in text_lower and "vpn" in summary_lower:
                score += 4
            if "password" in text_lower and "password" in summary_lower:
                score += 4
            if "lock" in text_lower and "password" in summary_lower:
                score += 3
            if ("software" in text_lower or "tool" in text_lower or "extension" in text_lower) and "software" in summary_lower:
                score += 4
            if "printer" in text_lower and "printer" in summary_lower:
                score += 4
            if "jam" in text_lower and "jam" in summary_lower:
                score += 4
            if ("wfh" in text_lower or "home" in text_lower or "monitor" in text_lower) and "home office" in summary_lower:
                score += 4
            if "phishing" in text_lower and "phishing" in summary_lower:
                score += 5
            if ("mailbox" in text_lower or "quota" in text_lower) and "mailbox" in summary_lower:
                score += 4
            if "admin" in text_lower and "admin" in summary_lower:
                score += 5
            if ("guest" in text_lower or "wifi" in text_lower or "wi-fi" in text_lower) and "wi-fi" in summary_lower:
                score += 4

            if score >= 4:
                matched.append((score, tk))

        matched.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in matched[:2]]
