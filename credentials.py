from envparse import env

env.read_envfile(".env")

MONGODB_URI = env.str("MONGODB_URI")
