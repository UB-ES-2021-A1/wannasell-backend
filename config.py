from decouple import config

class Config:
    pass

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}