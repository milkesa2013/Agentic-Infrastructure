from datetime import datetime, timedelta, timezone
from typing import Optional


class EngagementSkill:
    """Handles engagement rules like responding to comments within a time window."""

    def __init__(self, response_deadline_minutes: int = 15) -> None:
        self.response_deadline = timedelta(minutes=response_deadline_minutes)

    def should_respond_now(self, comment_time: datetime, current_time: Optional[datetime] = None) -> bool:
        """Return True if current time is within the response deadline from comment_time.

        Both datetimes should be timezone-aware (UTC is used if missing).
        """
        if current_time is None:
            current_time = datetime.now(tz=timezone.utc)

        if comment_time.tzinfo is None:
            comment_time = comment_time.replace(tzinfo=timezone.utc)

        return (current_time - comment_time) <= self.response_deadline
