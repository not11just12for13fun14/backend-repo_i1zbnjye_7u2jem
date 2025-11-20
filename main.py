import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

from database import create_document, get_documents, db
from schemas import Channel, Message, PaymentIntent, Project, Device

app = FastAPI(title="SOLA Vatzka Max 65 API", description="Backend services for futuristic music studio prototype")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "SOLA Vatzka Max 65 backend running"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


# ---------- Schemas exposure (lightweight) ----------
class SchemaResponse(BaseModel):
    name: str
    fields: List[str]

@app.get("/schema", response_model=List[SchemaResponse])
def get_schema():
    models = [Channel, Message, PaymentIntent, Project, Device]
    out = []
    for m in models:
        out.append(SchemaResponse(name=m.__name__.lower(), fields=list(m.model_fields.keys())))
    return out


# ---------- Channels & Messaging (Bluetooth-like chat over web) ----------
@app.get("/channels")
def list_channels(limit: int = Query(20, ge=1, le=100)):
    docs = get_documents("channel", {}, limit)
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return docs

@app.post("/channels")
def create_channel(ch: Channel):
    _id = create_document("channel", ch)
    return {"id": _id}

@app.get("/messages")
def list_messages(channel_id: Optional[str] = None, limit: int = Query(50, ge=1, le=200)):
    filt = {"channel_id": channel_id} if channel_id else {}
    docs = get_documents("message", filt, limit)
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return docs

@app.post("/messages")
def create_message(msg: Message):
    _id = create_document("message", msg)
    return {"id": _id}


# ---------- Projects ----------
@app.get("/projects")
def list_projects(limit: int = Query(20, ge=1, le=100)):
    docs = get_documents("project", {}, limit)
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return docs

@app.post("/projects")
def create_project(project: Project):
    _id = create_document("project", project)
    return {"id": _id}


# ---------- Devices (MIDI/OTG/Bluetooth metadata only) ----------
@app.get("/devices")
def list_devices(limit: int = Query(50, ge=1, le=200)):
    docs = get_documents("device", {}, limit)
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return docs

@app.post("/devices")
def register_device(device: Device):
    _id = create_document("device", device)
    return {"id": _id}


# ---------- Payments (mock intent) ----------
class CreatePaymentRequest(BaseModel):
    user_email: str
    plan: str
    amount_cents: int
    currency: str = "USD"

@app.post("/payments/intent")
def create_payment_intent(data: CreatePaymentRequest):
    intent = PaymentIntent(
        user_email=data.user_email,
        plan=data.plan,
        amount_cents=data.amount_cents,
        currency=data.currency,
        status="created",
    )
    _id = create_document("paymentintent", intent)
    return {"id": _id, "status": "created"}


# ---------- AI Assistant (mocked) ----------
class AssistantMessage(BaseModel):
    prompt: str

@app.post("/assistant/sola")
def assistant_reply(msg: AssistantMessage):
    # Simple, optimistic mocked reply for demo purposes
    reply = (
        "SOLA Vatzka Max 65 online. I can route your MIDI to external devices, "
        "set BPM and key, and configure mixers and futuristic EQs. "
        "Tell me the vibe and I’ll scaffold a project for you."
    )
    return {"assistant": "solavatzkamax65", "prompt": msg.prompt, "reply": reply}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
