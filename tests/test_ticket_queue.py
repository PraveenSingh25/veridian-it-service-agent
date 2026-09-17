"""
Unit tests for Ticket Queue processing (Section 3: Active and Closed tickets).
"""
import unittest
import os
from engine.agent import VeridianITAgent
from engine.models import ActionType, TargetDepartment


class TestVeridianTicketQueue(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "data")
        cls.agent = VeridianITAgent(data_dir=data_dir)

    def test_tk_1043_active_laptop_replacement(self):
        """TK-1043: S. Iyer (Laptop replacement 3.2 yrs old, Approved pending fulfillment)"""
        res = self.agent.process_active_ticket("TK-1043")
        self.assertEqual(res.action_type, ActionType.ROUTE_TO_HUMAN)
        self.assertEqual(res.target_department, TargetDepartment.IT_HARDWARE)
        self.assertIn("KB-03", res.policy_citations)
        self.assertIn("POL-ASSET-01", res.policy_citations)
        self.assertIn("2-week", res.sla_estimate)

    def test_tk_1044_active_non_catalog_software(self):
        """TK-1044: A. Khan (Non-catalog software request, Pending Security review)"""
        res = self.agent.process_active_ticket("TK-1044")
        self.assertEqual(res.action_type, ActionType.REQUIRE_APPROVAL)
        self.assertEqual(res.target_department, TargetDepartment.IT_SECURITY)
        self.assertIn("KB-04", res.policy_citations)
        self.assertIn("3–5 business days", res.sla_estimate)

    def test_tk_1047_active_home_office_equipment(self):
        """TK-1047: K. Singh (Home office equipment request, Pending Finance)"""
        res = self.agent.process_active_ticket("TK-1047")
        self.assertEqual(res.action_type, ActionType.REQUIRE_APPROVAL)
        self.assertEqual(res.target_department, TargetDepartment.FINANCE)
        self.assertIn("KB-10", res.policy_citations)
        self.assertIn("Finance", res.requires_approval_from)

    def test_tk_1048_active_phishing_investigation(self):
        """TK-1048: T. Rao (Phishing email reported, Escalated to Security under investigation)"""
        res = self.agent.process_active_ticket("TK-1048")
        self.assertEqual(res.action_type, ActionType.ESCALATE_SECURITY)
        self.assertEqual(res.target_department, TargetDepartment.IT_SECURITY)
        self.assertIn("KB-09", res.policy_citations)
        self.assertIsNotNone(res.safety_warning)

    def test_closed_tickets_non_actionable(self):
        """Closed tickets (TK-1042, TK-1045, TK-1046, TK-1049, TK-1050, TK-1051) are historical precedents"""
        closed_ids = ["TK-1042", "TK-1045", "TK-1046", "TK-1049", "TK-1050", "TK-1051"]
        for cid in closed_ids:
            tk = self.agent.kb_store.get_ticket(cid)
            self.assertFalse(tk.is_active)
            self.assertFalse(tk.actionable)
            res = self.agent.process_active_ticket(tk)
            self.assertIn("already closed", res.user_message)


if __name__ == "__main__":
    unittest.main()
