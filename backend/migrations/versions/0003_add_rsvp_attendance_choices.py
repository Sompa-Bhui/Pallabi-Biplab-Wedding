"""Add updated RSVP attendance choices.

Revision ID: 0003_rsvp_attendance_choices
Revises: 0002_email_outbox_claim_token
Create Date: 2026-11-11
"""
from typing import Sequence, Union

from alembic import op

revision: str = "0003_rsvp_attendance_choices"
down_revision: Union[str, None] = "0002_email_outbox_claim_token"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


_ATTENDANCE_WITH_NEW_CHOICES = (
    "attendance IN ("
    "'Wedding Ceremony (13 December 2026)', "
    "'Reception & Dinner (14 December 2026)', "
    "'Both Events', 'Joyfully Attending', "
    "'Attending with Family', 'Unable to Attend')"
)

_ATTENDANCE_LEGACY_CHOICES = (
    "attendance IN ("
    "'Wedding Ceremony (13 December 2026)', "
    "'Reception & Dinner (14 December 2026)', "
    "'Both Events', 'Unable to Attend')"
)


def upgrade() -> None:
    with op.batch_alter_table("rsvps") as batch_op:
        batch_op.drop_constraint("ck_rsvps_attendance", type_="check")
        batch_op.create_check_constraint(
            "ck_rsvps_attendance",
            _ATTENDANCE_WITH_NEW_CHOICES,
        )


def downgrade() -> None:
    op.execute(
        "UPDATE rsvps "
        "SET attendance = 'Wedding Ceremony (13 December 2026)' "
        "WHERE attendance IN ('Joyfully Attending', 'Attending with Family')"
    )
    with op.batch_alter_table("rsvps") as batch_op:
        batch_op.drop_constraint("ck_rsvps_attendance", type_="check")
        batch_op.create_check_constraint(
            "ck_rsvps_attendance",
            _ATTENDANCE_LEGACY_CHOICES,
        )
