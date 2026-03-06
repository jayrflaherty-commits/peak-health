"""affiliates.py — Affiliate links for Peak Health newsletter."""
from __future__ import annotations
from datetime import date
from typing import Optional

AMAZON_ASSOCIATE_TAG = "retirehub09-20"

AFFILIATE_LINKS = {
    "telehealth": {
        "name": "Hims/Hers — online health care",
        "description": "Talk to a licensed doctor from home — no waiting room, no hassle",
        "cta": "See your options →",
        "url": "https://YOUR_HIMS_HERS_AFFILIATE_LINK_HERE",
        # Hims/Hers via Impact | Commission: $20–40/signup
    },
    "supplements": {
        "name": "iHerb — professional supplements",
        "description": "Over 30,000 health products, lab-tested, shipped fast — 5% off your first order",
        "cta": "Shop iHerb →",
        "url": "https://YOUR_IHERB_AFFILIATE_LINK_HERE",
        # iHerb via CJ Affiliate | Commission: 5–10% of sale
    },
    "weight_loss": {
        "name": "Noom — science-based weight management",
        "description": "Lose weight with psychology, not dieting — clinically proven, 14-day trial",
        "cta": "Take the quiz →",
        "url": "https://YOUR_NOOM_AFFILIATE_LINK_HERE",
        # Noom via CJ | Commission: $30–60/signup
    },
    "blood_testing": {
        "name": "InsideTracker — know your biomarkers",
        "description": "Blood and DNA analysis that tells you exactly how to optimize your health",
        "cta": "Get tested →",
        "url": "https://YOUR_INSIDETRACKER_AFFILIATE_LINK_HERE",
        # InsideTracker direct or via CJ | Commission: $30–50/sale
    },
    "fitness": {
        "name": "Amazon health & fitness picks",
        "description": "Our editor's top picks for home fitness — resistance bands, weights, and more",
        "cta": "See picks →",
        "url": f"https://www.amazon.com/s?k=home+fitness+equipment+seniors&tag={AMAZON_ASSOCIATE_TAG}",
    },
}

CATEGORY_ORDER = list(AFFILIATE_LINKS.keys())

def get_daily_affiliate(for_date: date | None = None) -> dict:
    if for_date is None:
        for_date = date.today()
    key = CATEGORY_ORDER[for_date.toordinal() % len(CATEGORY_ORDER)]
    affiliate = AFFILIATE_LINKS[key].copy()
    affiliate["category"] = key
    return affiliate

def get_amazon_link(asin: str) -> str:
    return f"https://www.amazon.com/dp/{asin}?tag={AMAZON_ASSOCIATE_TAG}"
