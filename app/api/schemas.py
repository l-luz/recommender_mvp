"""
Pydantic schemas for API request/response validation
"""

from pydantic import BaseModel, Field, HttpUrl
from enum import Enum
from typing import Optional, List
from datetime import datetime


class ActionType(str, Enum):
    """Types of user actions"""

    LIKE = "like"
    DISLIKE = "dislike"
    CLEAR = "clear"


# ==================== Feedback Schemas ====================


class FeedbackRequest(BaseModel):
    """Input form for recording feedback"""

    user_id: int = Field(..., gt=0, description="User ID")
    book_id: int = Field(..., gt=0, description="Book ID")
    action_type: ActionType = Field(..., description="Type of feedback")
    slate_id: Optional[str] = Field(None, description="Recommendation list ID")
    pos: Optional[int] = Field(
        None, ge=0, le=20, description="Position in slate (1-indexed)"
    )
    ctx_features: Optional[str] = Field(
        None, description="Context features (JSON string)"
    )
    timestamp: Optional[int] = Field(None, description="Epoch ms")


class FeedbackResponse(BaseModel):
    """Response template for feedback"""

    success: bool
    message: str
    event_id: Optional[int] = None


# ==================== Book Schemas ====================


class BookBase(BaseModel):
    """Base book info"""

    id: int
    title: str
    authors: Optional[str] = None
    avg_rating: Optional[float] = None
    image: Optional[str] = None


class BookDetail(BookBase):
    """Detailed book info"""

    categories: Optional[str] = None
    description: Optional[str] = None
    publisher: Optional[str] = None
    published_date: Optional[str] = None
    ratings_count: Optional[int] = None
    price: Optional[float] = None
    info_link: Optional[HttpUrl] = None


class BookList(BaseModel):
    """Response for list of books"""

    user_id: int
    total: int
    books: list[BookDetail]


#
# ==================== User Schemas ====================
#
class LoginRequest(BaseModel):
    """Input form for user login"""

    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class UserBase(BaseModel):
    """Base user info"""

    id: int
    username: str
    preferred_genres: Optional[List[str]] = None


# ==================== Event/History Schemas ====================


class EventBase(BaseModel):
    """Base event info"""

    id: int
    user_id: int
    book_id: int
    action_type: str
    reward: Optional[float] = None
    timestamp: datetime


class HistorySummary(UserBase):
    """User history summary"""

    total_events: int
    likes: int
    dislikes: int
    unique_books_interacted: int


#
# ==================== Slate/Recommendation Schemas ====================
#


class BookRecommendation(BaseModel):
    """Return model for book recommendation"""

    book_id: int
    title: str
    authors: Optional[str] = None
    description: Optional[str] = None
    categories: Optional[str] = None
    score: Optional[float] = None
    image: Optional[str] = None


class SlateRequest(BaseModel):
    """Request form for getting recommendations"""

    user_id: int = Field(..., gt=0, description="User ID")
    n_items: int = Field(4, ge=1, le=20, description="Number of recommendations")


class SlateResponse(BaseModel):
    """Response form for recommendations"""

    user_id: int
    slate_id: str
    total: int
    recommendations: list[BookRecommendation]


class CategoryList(BaseModel):
    """Response for list of categories"""

    categories: list[str]
