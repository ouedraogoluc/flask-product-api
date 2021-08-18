import os 

#database initialization
if os.environ.get('DATABASE_URL') is None:
    # get connexion from postgresql
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@localhost:5432/product_db" # postgres://nomUtilisateur:motpasse@ipserver:port/basedbname
else:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace("postgres://", "postgresql://", 1)

# track les modifications
SQLALCHEMY_TRACK_MODIFICATIONS = False