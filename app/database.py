import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON
import databases

DATABASE_URL = "postgresql://usuario:senha@localhost:5432/nutritional_value_recipes_dev"

database = databases.Database(DATABASE_URL)

metadata = sa.MetaData()

# Columns:
# Define tabela que conterá as receitas culinárias
recipes = sa.Table(
    "recipes",
    metadata,
    sa.Column(
        "id",
        sa.Integer,
        primary_key=True
    ),
    sa.Column(
        "name",
        sa.String(50)
    ),
    sa.Column(
        "descript",
        sa.String(4000)
    ),
    sa.Column(
        "ingredients",
        sa.JSON()
    )
)

# Define tabela que conterá o valor nutricional dos ingredientes
nutritional_value_recipes = sa.Table(
    "nutritional_value_recipes",
    metadata,
    sa.Column(
        "id",
        sa.Integer,
        primary_key=True
    ),
    sa.Column(
        "id_recipe",
        sa.Integer,
        sa.ForeignKey("recipes.id")
    ),
    sa.Column(
        "nutritionl_value_ingredients",
        sa.JSON()
    )
)

roles = sa.Table(
    "roles",
    metadata,
    sa.Column(
        "id",
        sa.Integer, primary_key=True
    ),
    sa.Column(
        "name",
        sa.String(25),
    )
)

users = sa.Table(
    "users",
    metadata,
    sa.Column(
        "id",
        sa.Integer, primary_key=True
    ),
    sa.Column(
        "username",
        sa.String(16),
    ),
    sa.Column(
        "hashed_password",
        sa.String(14),
    ),
    sa.Column(
        "full_name",
        sa.String(30)
    ),
    sa.Column(
        "email",
        sa.String(20)
    ),
    sa.Column(
        "disable",
        sa.Boolean,
    ),
    sa.Column(
        "role",
        sa.Integer,
        sa.ForeignKey("roles.id")
    ),
    sa.Column(
        "created_at",
        sa.TIMESTAMP(timezone=True),
        server_default=sa.func.now(),
    ),
    sa.Column(
        "updated_at",
        sa.TIMESTAMP(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )
)

def concat_hashed_pass(password):
    return f"h@sh3d.{password}"

# Crie índices para a tabela 'recipes'
sa.Index(
    'idx_recipes_id',
    recipes.c.id
)

engine = sa.create_engine(DATABASE_URL)

metadata.create_all(engine)
