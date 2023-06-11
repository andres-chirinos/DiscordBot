import pymongo, requests, json, os
from __init__ import Cache

Memoria = pymongo.MongoClient(
    os.getenv(
        "MONGO_URL",
        "mongodb://mongo:QoodY7GX6kzhHebGIo2Q@containers-us-west-94.railway.app:7993",
    )
)

async def insert_one(database:str, collection:str, document):
    Database = Memoria.get_database(database)
    UserCollection = Database.get_collection(collection)
    data = UserCollection.insert_one(document)

async def find_one(database:str, collection:str, filter):
    Database = Memoria.get_database(database)
    UserCollection = Database.get_collection(collection)
    data = UserCollection.find_one(filter)
    return data

async def update_one(database:str, collection:str, filter, update):
    Database = Memoria.get_database(database)
    UserCollection = Database.get_collection(collection)
    UserCollection.update_one(filter, update)

async def push_role_connection(tokens, body):
    # GET/PUT /users/@me/applications/:id/role-connection
    url = f"https://discord.com/api/v10/users/@me/applications/{os.environ.get('DISCORD_CLIENT_ID')}/role-connection"
    data = json.dumps(body)
    response = requests.put(
        url,
        data,
        headers={
            "Authorization": f"Bearer {tokens['access_token']}",
            "Content-Type": "application/json",
        },
    )
    if not response.ok:
        raise Exception(f'Error putting discord metadata: [{response.status_code}] {response.text}')


async def get_role_connection(id):
    registermetadata = json.loads(Cache.get("registermetadata"))

    Database = Memoria.get_database("master")
    UserCollection = Database.get_collection(str(id))
    Identification = UserCollection.find_one(filter={"type": "identification"})

    metadata = dict()
    for registerdata in registermetadata:
        key = registerdata["key"]
        metadata[key] = Identification[key]

    role_connection_data = {
        "platform_name": Identification["type"],
        "platform_username": Identification["platform_username"],
        "metadata": metadata,
    }
    return role_connection_data

# async def get_role_connection(access_token, id:int):
#    # GET/PUT /users/@me/applications/:id/role-connection
#    url = f"https://discord.com/api/v10/users/@me/applications/{os.environ.get('CLIENT_ID')}/role-connection"
#    response = requests.get(url, headers={'Authorization': f'Bearer {access_token}'})
#    if response.ok:
#        data = response.json()
#        if data == {}:
#            data = role_connection_data
#        data['metadata'] = get_metadata(id)
#        return data
#    else:
#        raise Exception(f'Error getting discord metadata: [{response.status_code}] {response.text}')
