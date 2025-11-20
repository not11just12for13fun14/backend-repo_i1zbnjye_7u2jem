"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# App-specific schemas

class Channel(BaseModel):
    """Realtime comm channel (e.g., Bluetooth chat room)"""
    name: str = Field(..., description="Channel name")
    topic: Optional[str] = Field(None, description="Channel topic")

class Message(BaseModel):
    """Messages sent within a channel"""
    channel_id: str = Field(..., description="Channel identifier")
    sender: str = Field(..., description="Display name of sender")
    text: Optional[str] = Field(None, description="Plain text message")
    voice_url: Optional[str] = Field(None, description="URL to voice clip if any")

class PaymentIntent(BaseModel):
    """Payment record for subscriptions or purchases"""
    user_email: str = Field(..., description="Purchaser email")
    plan: str = Field(..., description="Plan or product id")
    amount_cents: int = Field(..., ge=0, description="Amount in cents")
    currency: str = Field("USD", description="Currency code")
    status: str = Field("created", description="Status of intent")

class Project(BaseModel):
    """Music project sessions metadata"""
    title: str
    bpm: int = Field(120, ge=40, le=300)
    key: str = Field("C Major")
    tracks: List[str] = Field(default_factory=list)

class Device(BaseModel):
    """External MIDI/OTG device metadata"""
    name: str
    manufacturer: Optional[str] = None
    connection: str = Field(..., description="Connection type: midi, bluetooth, otg")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
