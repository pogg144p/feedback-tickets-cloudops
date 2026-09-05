# test_transformer.py
# ─────────────────────────────────────────────────────────────
# Automated Unit Tests for Transformer Lambda
#
# These tests run in GitHub Actions before ANY code is deployed.
# If someone breaks the categorization logic, CI will fail
# and stop the deployment automatically.
# ─────────────────────────────────────────────────────────────

import sys
import os

# Add transformer directory to Python path so we can import its functions
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../lambdas/transformer')))

from handler import categorize, assign_priority


def test_categorize_bug():
    """Verify that error/bug keywords are recognized as 'bug' category."""
    assert categorize("The login button is broken and crashes") == "bug"
    assert categorize("I am unable to submit my feedback form") == "bug"


def test_categorize_feature():
    """Verify that feature request keywords are recognized as 'feature' category."""
    assert categorize("I would like to request dark mode support") == "feature"
    assert categorize("Wish we had an export to CSV feature") == "feature"


def test_categorize_complaint():
    """Verify that complaint keywords are recognized as 'complaint' category."""
    assert categorize("The page loading is very slow and terrible") == "complaint"


def test_categorize_general():
    """Verify fallback for text with no matching keywords."""
    assert categorize("Hello there") == "general"


def test_assign_priority_high_explicit():
    """Verify that high severity tickets always get high priority."""
    assert assign_priority("Nothing special", severity="high") == "high"


def test_assign_priority_urgent_keywords():
    """Verify urgent keyword triggers high priority even if severity is low."""
    assert assign_priority("Emergency! The database is down and urgent", severity="low") == "high"


def test_assign_priority_low_default():
    """Verify normal tickets default to low priority."""
    assert assign_priority("Just a general question", severity="low") == "low"
