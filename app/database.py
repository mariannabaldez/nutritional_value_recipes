import sqlalchemy as sa
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
        sa.JSON(), # {str:{measure:str, quantity:float}}
        sa.ForeignKey("ingredients.id")
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
        sa.JSON(),
        sa.ForeignKey("recipes.ingredients")
    )
)

# Índices:
# Crie índices para a tabela 'ingredients'
# sa.Index(
#     'idx_ingredients_id',
#     ingredients.c.id
# )

# Crie índices para a tabela 'recipes'
sa.Index(
    'idx_recipes_id',
    recipes.c.id
)

# Crie índices para a tabela 'nutritional_value_ingredients'
sa.Index(
    'idx_nutritional_value_recipes_nutritional_value_indredients',
    nutritional_value_recipes.c.nutritional_value_indredients

)

engine = sa.create_engine(DATABASE_URL)

metadata.create_all(engine)
