from pymongo.mongo_client import MongoClient
from environs import Env


env = Env()
env.read_env()
uri = env('MONGO_URI')
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection


def main():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
