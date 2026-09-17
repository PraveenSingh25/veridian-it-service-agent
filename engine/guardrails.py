"""
Safety Guardrails and Grounding Verifier for Veridian Corp IT Support Agent.
Enforces anti-hallucination, strict grounding, and critical security warnings.
"""
import re
from typing import Optional, Tuple, List


class Guardrails:
    # Security trigger keywords
    PHISHING_KEYWORDS = ["phishing", "suspicious email", "fake email", "malware", "unauthorized access", "hack"]
    FORWARD_KEYWORDS = ["forward", "forwarding", "forwarded", "sent to team", "sent to colleague", "share with"]
    
    # Ambiguous phrases that lack any actionable details
    AMBIGUOUS_PATTERNS = [
        r"^hey\b",
        r"^help\b",
        r"^it('?s)? not working\b",
        r"^something is wrong\b",
        r"^please help\b",
        r"^not working\b",
        r"^broken\b"
    ]

    ALLOWED_POLICY_IDS = {
        "KB-01", "KB-02", "KB-03", "KB-04", "KB-05", 
        "KB-06", "KB-07", "KB-08", "KB-09", "KB-10", 
        "POL-ASSET-01"
    }

    ALLOWED_TICKET_IDS = {
        "TK-1042", "TK-1043", "TK-1044", "TK-1045", "TK-1046",
        "TK-1047", "TK-1048", "TK-1049", "TK-1050", "TK-1051"
    }

    @classmethod
    def check_security_hazard(cls, text: str) -> Tuple[bool, Optional[str]]:
        """
        Detects suspected phishing/malware and critically flags any forwarding to teammates.
        Grounding: KB-09: 'should not be forwarded to other employees'.
        """
        text_lower = text.lower()
        has_phishing = any(k in text_lower for k in cls.PHISHING_KEYWORDS)
        has_forwarding = any(k in text_lower for k in cls.FORWARD_KEYWORDS)

        if has_phishing and has_forwarding:
            warning = (
                "CRITICAL SECURITY ALERT (KB-09): DO NOT FORWARD SUSPECTED PHISHING EMAILS! "
                "Forwarding spreads malicious payloads and phishing risks across internal mailboxes. "
                "Immediately notify any teammates who received it to delete without clicking, "
                "and report the email exclusively to security@veridian-corp.example."
            )
            return True, warning
        elif has_phishing:
            warning = (
                "SECURITY ALERT (KB-09): Suspected security incident detected. "
                "Report immediately to security@veridian-corp.example. Do not forward to colleagues."
            )
            return True, warning
        return False, None

    @classmethod
    def is_underspecified(cls, text: str) -> bool:
        """
        Detects if a request is completely vague without actionable technical context.
        E.g., REQ-15: 'hey can you help, its not working'
        """
        clean = text.strip().lower()
        # Remove punctuation
        clean = re.sub(r"[^\w\s]", "", clean)
        tokens = clean.split()
        
        # If very short (< 7 words) and matches generic complaints without technical nouns
        technical_nouns = [
            "laptop", "screen", "vpn", "printer", "wifi", "wi-fi", "password", 
            "account", "email", "mailbox", "quota", "monitor", "software", 
            "app", "expense", "browser", "admin", "server", "access", "jam"
        ]
        has_tech_noun = any(tn in clean for tn in technical_nouns)
        
        if len(tokens) <= 7 and not has_tech_noun:
            return True
        return False

    @classmethod
    def validate_citations(cls, policy_citations: List[str], precedent_citations: List[str]) -> Tuple[bool, List[str]]:
        """Verifies that every cited policy or precedent exists in Veridian source data."""
        invalid = []
        for pol in policy_citations:
            if pol not in cls.ALLOWED_POLICY_IDS:
                invalid.append(f"Invalid policy citation: {pol}")
        for tk in precedent_citations:
            if tk not in cls.ALLOWED_TICKET_IDS:
                invalid.append(f"Invalid ticket citation: {tk}")
        return (len(invalid) == 0), invalid
