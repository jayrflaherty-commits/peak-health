"""content_generator.py — Peak Health content generation via Claude."""
from __future__ import annotations
import json, sys
from datetime import date
from pathlib import Path
import anthropic

_FILE_DIR = Path(__file__).parent
BASE_DIR = _FILE_DIR.parent if (_FILE_DIR.parent / "shared").exists() else _FILE_DIR
sys.path.insert(0, str(BASE_DIR))
from shared.topic_tracker import get_recent_topics, format_topics_for_prompt, log_topic
import config

SYSTEM_PROMPT = """You are the editor of "Peak Health," a daily wellness and longevity newsletter for adults 45–70. Your voice is evidence-based but warm — like a trusted doctor friend who explains things clearly and never fear-mongers.

NEWSLETTER FORMULA:
1. "Today's Health Insight" — one science-backed tip, study, or finding (3-4 sentences)
2. "Quick Health Wins" — 3 actionable micro-habits or facts readers can use today
3. "By the Numbers" — one compelling health statistic with context
4. "Ask the Research" — answer one common health question with a science-backed answer
5. A calm, encouraging sign-off

TONE: Optimistic, empowering, grounded in evidence. Never alarmist. Cite general research trends rather than specific papers. Focus on actionable takeaways for adults over 45.

Topics to rotate through: nutrition, sleep, strength training, cognitive health, longevity research, supplements (evidence-based only), heart health, gut health, mental health, preventative screenings, hydration, stress management.

Output JSON only."""

CONTENT_SCHEMA = """{
  "subject_line": "35-50 chars, specific and benefit-driven",
  "preview_text": "80-100 chars",
  "title": "Web title",
  "topic_slug": "kebab-case e.g. sleep-deep-sleep-longevity",
  "hook": "2 sentences. Start with a surprising fact or counterintuitive finding.",
  "todays_insight": {
    "topic": "Topic area e.g. Sleep, Nutrition, Exercise",
    "finding": "3-4 sentences explaining the insight clearly and practically"
  },
  "quick_wins": [
    "Actionable tip 1 (1 sentence)",
    "Actionable tip 2 (1 sentence)",
    "Actionable tip 3 (1 sentence)"
  ],
  "by_the_numbers": {
    "stat": "The statistic",
    "context": "2 sentences explaining what it means for readers"
  },
  "ask_the_research": {
    "question": "A question readers often have",
    "answer": "2-3 sentences with a clear, evidence-based answer"
  },
  "sponsor_placeholder": "2-3 sentences native ad for a health supplement, telehealth service, or fitness program",
  "cta_text": "Button label e.g. 'Learn more →'",
  "signoff": "1 encouraging sentence + tomorrow's topic teaser"
}"""


def generate_content(for_date: date | None = None) -> dict:
    if for_date is None:
        for_date = date.today()
    recent = get_recent_topics(config.NEWSLETTER_DIR, days=365)
    no_repeat = format_topics_for_prompt(recent)
    date_str = for_date.strftime("%A, %B %d, %Y")

    user_prompt = f"""Generate a Peak Health newsletter for {date_str}.

{no_repeat}

Pick a topic that is timely and seasonally relevant for {for_date.strftime("%B")}.
Return valid JSON matching this schema:
{CONTENT_SCHEMA}"""

    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    msg = client.messages.create(model=config.CLAUDE_MODEL, max_tokens=2000,
                                  system=SYSTEM_PROMPT,
                                  messages=[{"role": "user", "content": user_prompt}])
    raw = msg.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    content = json.loads(raw)
    log_topic(config.NEWSLETTER_DIR, content.get("topic_slug", f"health-{for_date.isoformat()}"),
              content.get("subject_line", ""), for_date)
    return content


def format_content_for_template(content: dict) -> dict:
    insight = content.get("todays_insight", {})
    nums = content.get("by_the_numbers", {})
    research = content.get("ask_the_research", {})

    main_story = (
        f"<strong>Today's topic: {insight.get('topic','')}</strong><br><br>"
        f"{insight.get('finding','')}"
    )

    quick_wins = content.get("quick_wins", [])
    by_numbers = f"📊 {nums.get('stat','')} — {nums.get('context','')}" if nums else ""
    ask = f"❓ Q: {research.get('question','')} A: {research.get('answer','')}" if research else ""

    quick_hits = quick_wins[:]
    if by_numbers:
        quick_hits.append(by_numbers)
    if ask:
        quick_hits.append(ask)

    return {
        "hook": content.get("hook", ""),
        "main_story": main_story,
        "quick_hits": quick_hits[:5],
        "sponsor_placeholder": content.get("sponsor_placeholder", ""),
        "money_move": f"Today's action: {quick_wins[0] if quick_wins else 'See inside.'}",
        "cta_text": content.get("cta_text", "Read more →"),
        "cta_url": "#",
        "signoff": content.get("signoff", ""),
        "title": content.get("title", "Peak Health"),
    }
