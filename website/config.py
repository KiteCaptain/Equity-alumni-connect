# import os

# # Configuration parameters
# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'mrcaptain@12345.vectorized.ithinkthisisverystrongforasecuritykey'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

# # Database URI
# class DevelopmentConfig(Config):
#     DB_USERNAME = 'milton'
#     DB_PASSWORD = 'test%401234'
#     DB_HOST = 'elp-server.postgres.database.azure.com'
#     DB_NAME = 'postgres'
#     DB_SSL_MODE = 'require'
#     SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?sslmode={DB_SSL_MODE}'

# class ProductionConfig(Config):
#     # Production configuration settings
#     pass

# class TestingConfig(Config):
#     # Testing configuration settings
#     pass
