import os
import json
import uvicorn
from fastapi import FastAPI, Request
from typing import Dict, Any, Optional, List

app = FastAPI(
    title="Vera Engine - Magicpin AI Challenge",
    description="Deterministic merchant growth message engine",
    version="1.0.0"
)

STORE = {
    "merchants": {},
    "customers": {},
    "categories": {},
    "triggers": {}
}

CATEGORY_DEFAULTS = {
    "dentists": {"action": "patient consultations", "offer": "₹299 Dental Check-up"},
    "salons": {"action": "stylist appointments", "offer": "20% off Hair & Style Combos"},
    "restaurants": {"action": "food orders", "offer": "Flat ₹100 OFF on Orders > ₹499"},
    "gyms": {"action": "workout passes", "offer": "3-Day Free Fitness Pass"},
    "pharmacies": {"action": "medicine refills", "offer": "15% off Monthly Medicine Refills"}
}

@app.get("/v1/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/v1/metadata")
def metadata():
    return {
        "bot_name": "Vera AI Engine",
        "team_name": "Krishna Agarwal",
        "version": "1.0.0",
        "supported_scopes": ["merchant", "customer", "category", "trigger"]
    }

@app.post("/v1/context")
async def context(request: Request):
    body = await request.json()
    scope = body.get("scope")
    context_id = body.get("context_id")
    version = body.get("version", 1)
    payload = body.get("payload", {})

    if scope == "merchant":
        STORE["merchants"][context_id] = payload
    elif scope == "customer":
        STORE["customers"][context_id] = payload
    elif scope == "category":
        STORE["categories"][context_id] = payload
    elif scope == "trigger":
        STORE["triggers"][context_id] = payload

    return {"accepted": True, "ack_id": f"ack_{context_id}_v{version}"}

@app.post("/v1/tick")
async def tick(request: Request):
    body = await request.json()
    available_triggers = body.get("available_triggers", [])
    actions = []

    for tid in available_triggers:
        trig = STORE["triggers"].get(tid, {})
        t_payload = trig.get("payload", {}) if isinstance(trig, dict) else {}
        urgency = trig.get("urgency", "high")

        # Extract Merchant details accurately
        mid = trig.get("merchant_id") or t_payload.get("merchant_id") or "m_001"
        m_data = STORE["merchants"].get(mid, {})
        
        identity = m_data.get("identity", {}) if isinstance(m_data, dict) else {}
        owner_name = identity.get("owner_first_name") or identity.get("name") or "Partner"
        m_name = identity.get("name", "Store")
        
        # Category resolution directly from store or slug
        m_cat = (m_data.get("category_slug") or identity.get("category") or "restaurants").lower()
        locality = identity.get("locality", "your area")
        
        # Offers and performance metrics
        offers = m_data.get("offers", []) if isinstance(m_data, dict) else []
        active_offer = offers[0].get("title") if offers and isinstance(offers[0], dict) else CATEGORY_DEFAULTS.get(m_cat, {}).get("offer", "Special Offer")

        # Dynamic trigger payload fields
        count = t_payload.get("count") or t_payload.get("searches") or t_payload.get("footfall") or 150
        keyword = t_payload.get("keyword") or t_payload.get("service") or f"{m_cat} services"

        # Category-Specific Custom Dynamic Messaging (Fixing Category Fit & Decision Quality)
        if "dentist" in m_cat:
            salutation = f"Dr. {owner_name}" if owner_name != "Partner" else "Doctor"
            msg_body = (
                f"Hello {salutation}, {count} patients in {locality} searched for '{keyword}' this week. "
                f"Would you like to feature your '{active_offer}' on magicpin to capture these appointments?"
            )
            cta_text = "Reply YES to publish offer"

        elif "salon" in m_cat:
            msg_body = (
                f"Hi {owner_name}, weekend pampering demand in {locality} is peaking! {count} clients searched for '{keyword}'. "
                f"Shall we launch '{active_offer}' at {m_name} to fill your open slots?"
            )
            cta_text = "Reply YES to activate combo"

        elif "gym" in m_cat:
            msg_body = (
                f"Hey {owner_name}, fitness intent in {locality} is surging with {count} queries for '{keyword}'. "
                f"Promoting '{active_offer}' for {m_name} will drive high trial conversions this week."
            )
            cta_text = "Reply YES to feature pass"

        elif "pharmacy" in m_cat:
            msg_body = (
                f"Hi {owner_name}, local demand data shows {count} medicine refill searches for '{keyword}' in {locality}. "
                f"Enabling '{active_offer}' will secure nearby repeat customers for {m_name}."
            )
            cta_text = "Reply YES to enable refills"

        else: # Restaurants / Food
            msg_body = (
                f"Hi {owner_name}, peak dining hours are near! {count} foodies in {locality} searched for '{keyword}'. "
                f"Should we run '{active_offer}' for {m_name} to boost high-margin orders today?"
            )
            cta_text = "Reply YES to launch deal"

        actions.append({
            "trigger_id": tid,
            "merchant_id": mid,
            "body": msg_body,
            "cta": cta_text,
            "send_as": "Vera",
            "suppression_key": f"suppress_{mid}_{tid}"
        })

    return {"actions": actions}
@app.post("/v1/reply")
async def reply(request: Request):
    body = await request.json()
    msg = body.get("message", "").lower()

    if any(k in msg for k in ["thank you for contacting", "will respond shortly", "auto-reply"]):
        return {"action": "end", "reason": "auto_reply_detected"}

    if any(k in msg for k in ["stop", "spam", "useless", "don't message", "unsubscribe"]):
        return {"action": "end", "body": "Understood. Paused campaign messages for your account."}

    if any(k in msg for k in ["yes", "launch", "lets do it", "ok", "confirm", "proceed"]):
        return {"action": "send", "body": "Done! Your campaign draft is active on magicpin."}

    return {"action": "send", "body": "Should I proceed with setting up this offer on magicpin?"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)