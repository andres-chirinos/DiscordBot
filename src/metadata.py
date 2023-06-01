import pymongo, os, requests, json
from __init__ import discord_session

role_connection_data = {
    "platform_name": "Identificación",
    "platform_username": None,
    "metadata":{}
    }

metadata = {
    'verified': False,
    'rank':0,
    }

def changedatabase(Memoria:pymongo.MongoClient, id:int, data):
    metadatatable = Memoria['master']['metadata']
    metadatatable.update_one({'_id':id},{ "$set": data})
    return get_metadata(Memoria, id)

def create_metadata(Memoria:pymongo.MongoClient, id:int):
    metadatatable = Memoria['master']['metadata']
    data = metadata
    data['_id'] = id
    metadatatable.insert_one(data)
    return metadatatable.find_one({'_id':id})

def get_metadata(Memoria:pymongo.MongoClient, id:int):
    metadatatable = Memoria['master']['metadata']
    metadata = metadatatable.find_one({'_id':id})
    if not metadata:
        metadata = create_metadata(Memoria, id)
    del metadata['_id']
    return metadata

async def push_role_connection(access_token, body):
    # GET/PUT /users/@me/applications/:id/role-connection
    url = f'https://discord.com/api/v10/users/@me/applications/{discord_session.client_id}/role-connection'
    response = requests.put(url, data = json.dumps(body), headers={
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    })
    if not response.ok:
        raise Exception(f'Error pushing discord metadata: [{response.status_code}] {response.text}')

# Fetch the metadata currently pushed to Discord for the currently logged
# in user, for this specific bot.
async def get_role_connection(access_token, Memoria:pymongo.MongoClient, id:int):
    # GET/PUT /users/@me/applications/:id/role-connection
    url = f'https://discord.com/api/v10/users/@me/applications/{discord_session.client_id}/role-connection'
    response = requests.get(url, headers={'Authorization': f'Bearer {access_token}'})
    if response.ok:
        data = response.json()
        if data == {}:
            data = role_connection_data
        data['metadata'] = get_metadata(Memoria, id)
        return data
    else:
        raise Exception(f'Error getting discord metadata: [{response.status_code}] {response.text}')