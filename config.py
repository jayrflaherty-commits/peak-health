"""config.py — Peak Health newsletter configuration."""
import os
from dotenv import load_dotenv
load_dotenv(override=True)

NEWSLETTER_NAME        = "Peak Health"
NEWSLETTER_DIR         = "peak-health"
TAGLINE                = "Science-backed wellness for a longer, stronger life"
SEND_HOUR              = 7
SEND_MINUTE            = 45
TIMEZONE               = "America/New_York"
ANTHROPIC_API_KEY      = os.getenv("ANTHROPIC_API_KEY", "")
BEEHIIV_API_KEY        = os.getenv("PEAK_HEALTH_BEEHIIV_API_KEY", os.getenv("BEEHIIV_API_KEY", ""))
BEEHIIV_PUBLICATION_ID = os.getenv("PEAK_HEALTH_BEEHIIV_PUBLICATION_ID", "")
CLAUDE_MODEL           = "claude-sonnet-4-5"

def validate():
    missing = [k for k, v in {
        "ANTHROPIC_API_KEY": ANTHROPIC_API_KEY,
        "PEAK_HEALTH_BEEHIIV_API_KEY": BEEHIIV_API_KEY,
        "PEAK_HEALTH_BEEHIIV_PUBLICATION_ID": BEEHIIV_PUBLICATION_ID,
    }.items() if not v]
    if missing:
        raise EnvironmentError(f"Missing required env vars: {', '.join(missing)}")
