"""
Event logging system
"""

import logging
from datetime import datetime
from pathlib import Path

# Create log directory if it does not exist
LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configure logger
logger = logging.getLogger("recommender_mvp")
logger.setLevel(logging.DEBUG)

# File handler
file_handler = logging.FileHandler(
    LOG_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
)
file_handler.setLevel(logging.DEBUG)

# Handler for console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Format
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def log_event(event_type: str, user_id: int, book_id: int, **kwargs):
    """Recommendation and feedback event log"""
    logger.info(
        f"Event: {event_type} | User: {user_id} | Book: {book_id} | "
        f"Extra: {kwargs}"
    )


def log_model_update(n_samples: int, avg_reward: float):
    """Template update log"""
    logger.info(
        f"Model updated with {n_samples} samples. Avg reward: {avg_reward:.3f}"
    )
