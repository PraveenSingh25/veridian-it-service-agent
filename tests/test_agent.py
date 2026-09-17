"""
Unit and regression tests for employee requests (REQ-01 to REQ-15).
Ensures strict policy grounding, safety warnings, and proper routing.
"""
import unittest
import os
from engine.agent import VeridianITAgent
from engine.models import ActionType, TargetDepartment
from engine.guardrails import Guardrails


class TestVeridianAgentRequests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "data")
        cls.agent = VeridianITAgent(data_dir=data_dir)

    def test_req_01_laptop_dead_aditi(self):
        """REQ-01: Aditi Sharma (Laptop completely dead, 3.5 yrs old)"""
        req = self.agent.kb_store.get_request("REQ-01")
        res = self.agent.process_employee_request(req)
        
        self.assertEqual(res.action_type, ActionType.ROUTE_TO_HUMAN)
        self.assertEqual(res.target_department, TargetDepartment.IT_HARDWARE)
        self.assertIn("KB-03", res.policy_citations)
        self.assertIn("POL-ASSET-01", res.policy_citations)
        self.assertIn("TK-1043", res.precedent_citations)
        self.assertIsNotNone(res.conflict_reconciliation)
        self.assertIn("4-year", res.conflict_reconciliation)
        self.assertIn("3 years", res.conflict_reconciliation)

    def test_req_02_guest_wifi_vikram(self):
        """REQ-02: Vikram Chawla (Guest Wi-Fi for tomorrow)"""
        req = self.agent.kb_store.get_request("REQ-02")
        res = self.agent.process_employee_request(req)
        
        self.assertEqual(res.action_type, ActionType.DIRECT_RESOLVE)
        self.assertEqual(res.target_department, TargetDepartment.EMPLOYEE_SELF_SERVICE)
        self.assertIn("KB-07", res.policy_citations)
        self.assertIn("TK-1051", res.precedent_citations)
        self.assertIn("front-desk kiosk", res.user_message)
        self.assertIn("24 hours", res.user_message)

    def test_req_03_password_lockout_karan(self):
        """REQ-03: Karan Mehta (Locked out, 6 failed attempts)"""
        req = self.agent.kb_store.get_request("REQ-03")
        res = self.agent.process_employee_request(req)
        
        self.assertEqual(res.action_type, ActionType.ROUTE_TO_HUMAN)
        self.assertEqual(res.target_department, TargetDepartment.IT_SERVICE_DESK)
        self.assertIn("KB-01", res.policy_citations)
        self.assertIn("TK-1049", res.precedent_citations)
        self.assertIn("manual", res.user_message.lower())

    def test_req_04_software_catalog_ritu(self):
        """REQ-04: Ritu Bhatia (Non-catalog data analysis tool)"""
        req = self.agent.kb_store.get_request("REQ-04")
        res = self.agent.process_employee_request(req)
        
        self.assertEqual(res.action_type, ActionType.REQUIRE_APPROVAL)
        self.assertEqual(res.target_department, TargetDepartment.IT_SECURITY)
        self.assertIn("KB-04", res.policy_citations)
        self.assertIn("TK-1044", res.precedent_citations)
        self.assertIn("3–5 business days", res.sla_estimate)

    def test_req_05_vpn_expired_sanjay(self):
        """REQ-05: Sanjay Oberoi (VPN credentials expired)"""
        req = self.agent.kb_store.get_request("REQ-05")
        res = self.agent.process_employee_request(req)
        
        self.assertEqual(res.action_type, ActionType.DIRECT_RESOLVE)
        self.assertEqual(res.target_department, TargetDepartment.EMPLOYEE_SELF_SERVICE)
        self.assertIn("KB-02", res.policy_citations)
        self.assertIn("TK-1042", res.precedent_citations)
        self.assertIn("90 days", res.user_message)

    def test_req_06_printer_jam_meera(self):
        """REQ-06: Meera Iyer (Printer 3rd floor paper jam error)"""
        req = self.agent.kb_store.get_request("REQ-06")
        res = self.agent.process_employee_request(req)
        
        self.assertEqual(res.action_type, ActionType.ROUTE_TO_HUMAN)
        self.assertEqual(res.target_department, TargetDepartment.IT_SERVICE_DESK)
        self.assertIn("KB-05", res.policy_citations)
        self.assertIn("TK-1046", res.precedent_citations)
        self.assertIn("spooler", res.user_message.lower())

    def test_req_07_wfh_equipment_farhan(self):
        """REQ-07: Farhan Ali (WFH 4 days/week monitor)"""
        req = self.agent.kb_store.get_request("REQ-07")
        res = self.agent.process_employee_request(req)
        
        self.assertEqual(res.action_type, ActionType.REQUIRE_APPROVAL)
        self.assertEqual(res.target_department, TargetDepartment.FINANCE)
        self.assertIn("KB-10", res.policy_citations)
        self.assertIn("TK-1047", res.precedent_citations)
        self.assertIn("Finance", res.requires_approval_from)

    def test_req_08_phishing_forwarding_ananya(self):
        """REQ-08: Ananya Reddy (Phishing email forwarded to teammates)"""
        req = self.agent.kb_store.get_request("REQ-08")
        res = self.agent.process_employee_request(req)
        
        self.assertEqual(res.action_type, ActionType.ESCALATE_SECURITY)
        self.assertEqual(res.target_department, TargetDepartment.IT_SECURITY)
        self.assertIn("KB-09", res.policy_citations)
        self.assertIn("TK-1048", res.precedent_citations)
        self.assertIsNotNone(res.safety_warning)
        self.assertIn("DO NOT FORWARD", res.safety_warning)
        self.assertIn("security@veridian-corp.example", res.user_message)

    def test_req_09_mailbox_full_rohit(self):
        """REQ-09: Rohit Desai (Mailbox full, cannot send email)"""
        req = self.agent.kb_store.get_request("REQ-09")
        res = self.agent.process_employee_request(req)
        
        self.assertEqual(res.action_type, ActionType.DIRECT_RESOLVE)
        self.assertIn("KB-06", res.policy_citations)
        self.assertIn("TK-1045", res.precedent_citations)
        self.assertIn("25GB", res.user_message)
        self.assertIn("50GB", res.user_message)

    def test_req_10_admin_access_kavya(self):
        """REQ-10: Kavya Pillai (Admin access to finance reporting server)"""
        req = self.agent.kb_store.get_request("REQ-10")
        res = self.agent.process_employee_request(req)
        
        self.assertEqual(res.action_type, ActionType.REQUIRE_APPROVAL)
        self.assertEqual(res.target_department, TargetDepartment.IT_SECURITY)
        self.assertIn("TK-1050", res.precedent_citations)
        self.assertIn("justification", res.user_message.lower())

    def test_req_11_contractor_vpn_nikhil(self):
        """REQ-11: Nikhil Bansal (Contractor joining team next week)"""
        req = self.agent.kb_store.get_request("REQ-11")
        res = self.agent.process_employee_request(req)
        
        self.assertEqual(res.action_type, ActionType.REQUIRE_APPROVAL)
        self.assertIn("KB-02", res.policy_citations)
        self.assertIn("manager approval", res.user_message.lower())
        self.assertIn("access request form", res.user_message.lower())

    def test_req_12_expense_tool_sneha(self):
        """REQ-12: Sneha Kulkarni (Expense tool invalid credentials)"""
        req = self.agent.kb_store.get_request("REQ-12")
        res = self.agent.process_employee_request(req)
        
        self.assertEqual(res.action_type, ActionType.ROUTE_TO_HUMAN)
        self.assertIn("KB-08", res.policy_citations)
        self.assertIn("Finance", res.user_message)

    def test_req_13_laptop_screen_flicker_aman(self):
        """REQ-13: Aman Gupta (Laptop screen flickering, 2 years old)"""
        req = self.agent.kb_store.get_request("REQ-13")
        res = self.agent.process_employee_request(req)
        
        self.assertEqual(res.action_type, ActionType.ROUTE_TO_HUMAN)
        self.assertEqual(res.target_department, TargetDepartment.IT_HARDWARE)
        self.assertIn("KB-03", res.policy_citations)
        self.assertIn("repair", res.user_message.lower())

    def test_req_14_browser_extension_tanya(self):
        """REQ-14: Tanya Chopra (Browser extension approval)"""
        req = self.agent.kb_store.get_request("REQ-14")
        res = self.agent.process_employee_request(req)
        
        self.assertEqual(res.action_type, ActionType.REQUIRE_APPROVAL)
        self.assertEqual(res.target_department, TargetDepartment.IT_SECURITY)
        self.assertIn("KB-04", res.policy_citations)
        self.assertIn("TK-1044", res.precedent_citations)

    def test_req_15_vague_input_rahul(self):
        """REQ-15: Rahul Menon ('hey can you help, its not working')"""
        req = self.agent.kb_store.get_request("REQ-15")
        res = self.agent.process_employee_request(req)
        
        self.assertEqual(res.action_type, ActionType.REQUEST_CLARIFICATION)
        self.assertEqual(len(res.policy_citations), 0)
        self.assertIn("clarification", res.internal_notes.lower())

    def test_grounding_citation_integrity(self):
        """Validate that citations across all requests exist in knowledge base"""
        for req in self.agent.kb_store.get_all_requests():
            res = self.agent.process_employee_request(req)
            is_valid, errors = Guardrails.validate_citations(res.policy_citations, res.precedent_citations)
            self.assertTrue(is_valid, f"Invalid citations found for {req.id}: {errors}")


if __name__ == "__main__":
    unittest.main()
