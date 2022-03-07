"""empty message

Revision ID: bdee1480419e
Revises: b9533c871f62
Create Date: 2022-02-27 16:33:47.070038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bdee1480419e"
down_revision = "b9533c871f62"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
    INSERT 
        INTO public."role" ("name",description) 
    VALUES 
        ('admin','admin'),
        ('teacher','teacher'),
        ('student','student');
    """
    )


def downgrade():
    pass
