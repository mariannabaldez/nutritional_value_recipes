import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON
import databases

DATABASE_URL = None

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
    )
)

# Define tabela que conterá os ingredientes usados nas receitas
ingredients = sa.Table(
    "ingredients",
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
        "name",
        sa.String(50)
    ),
    sa.Column(
        "measure",
        sa.String(50)
    ),
    sa.Column(
        "quantity",
        sa.Integer
    )
)

# Define tabela que conterá o valor nutricional dos ingredientes
nutritional_value_ingredients = sa.Table(
    "nutritional_value_ingredients",
    metadata,
    sa.Column(
        "id",
        sa.Integer,
        primary_key=True
    ),
    sa.Column(
        "id_ingredient",
        sa.Integer,
        sa.ForeignKey("ingredients.id")
    ),
    sa.Column(
        "calories",
        sa.Integer
    ),
    sa.Column(
        "protein",
        sa.Float
    ),
    sa.Column(
        "carbo",
        sa.Float
    ),
    sa.Column(
        "saturated_fat",
        sa.Float
    ),
    sa.Column(
        "polyunsaturated_fat",
        sa.Float
    ),
    sa.Column(
        "monounsaturated_fat",
        sa.Float
    ),
    sa.Column(
        "fiber",
        sa.Integer
    ),
    sa.Column(
        "sugar",
        sa.Integer
    ),
    sa.Column(
        "sodium",
        sa.Float
    ),
    sa.Column(
        "potassium",
        sa.Float
    ),
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
        "calories",
        sa.Integer
    ),
    sa.Column(
        "protein",
        sa.Float
    ),
    sa.Column(
        "carbo",
        sa.Float
    ),
    sa.Column(
        "saturated_fat",
        sa.Float
    ),
    sa.Column(
        "polyunsaturated_fat",
        sa.Float
    ),
    sa.Column(
        "monounsaturated_fat",
        sa.Float
    ),
    sa.Column(
        "fiber",
        sa.Integer
    ),
    sa.Column(
        "sugar",
        sa.Integer
    ),
    sa.Column(
        "sodium",
        sa.Float
    ),
    sa.Column(
        "potassium",
        sa.Float
    ),
)

# Índices:
# Crie índices para a tabela 'recipes'
sa.Index(
    'idx_recipess_name',
    recipes.c.name
)

# Crie índices para a tabela 'ingredients'
sa.Index(
    'idx_ingredients_id_ingredient',
    ingredients.c.id_recipe
)

# Crie índices para a tabela 'nutritional_value_ingredients'
sa.Index(
    'idx_nutritional_value_ingredients_id_ingredient',
    nutritional_value_ingredients.c.id_ingredient
)

# Crie índices para a tabela 'nutritional_value_ingredients'
sa.Index(
    'idx_nutritional_value_recipes_id_recipe',
    nutritional_value_ingredients.c.id_ingredient
)

engine = sa.create_engine(DATABASE_URL)

metadata.create_all(engine)
