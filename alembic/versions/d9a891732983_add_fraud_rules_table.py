from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "d9a891732983"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "fraud_rules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("field", sa.String(), nullable=False),
        sa.Column("operator", sa.String(), nullable=False),
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("active", sa.Boolean(), default=True),
    )


def downgrade() -> None:
    op.drop_table("fraud_rules")
