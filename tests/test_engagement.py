from datetime import datetime, timedelta, timezone
from agentic.engagement import EngagementSkill


def test_should_respond_within_deadline():
    skill = EngagementSkill(response_deadline_minutes=15)
    comment_time = datetime.now(tz=timezone.utc) - timedelta(minutes=10)

    assert skill.should_respond_now(comment_time) is True


def test_should_not_respond_after_deadline():
    skill = EngagementSkill(response_deadline_minutes=15)
    comment_time = datetime.now(tz=timezone.utc) - timedelta(minutes=20)

    assert skill.should_respond_now(comment_time) is False
