import motor.motor_asyncio

from credentials import MONGODB_URI

client = motor.motor_asyncio.AsyncIOMotorClient(
    MONGODB_URI
)
db = client["blockchain"]
