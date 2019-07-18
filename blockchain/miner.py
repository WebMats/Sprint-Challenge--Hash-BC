import hashlib
import requests
import asyncio
import aiohttp
import ast
import json
import sys

from uuid import uuid4

from timeit import default_timer as timer

import random

async def aws_lambda_call(proof, index, step):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as client:
        aws = ""
        async with client.post(aws, data=json.dumps({'proof': proof, 'start': index, 'step': step})) as response:
            return await response.read()

async def create_lambda_batch(last_proof, step):
    print("GETTING NEW PROOF FROM AWS LAMBDA...")
    lambda_tasks = []
    for i in range(1, step + 1):
        lambda_tasks.append(asyncio.create_task(aws_lambda_call(last_proof, i, step)))
    done, pending = await asyncio.wait({*lambda_tasks}, return_when="FIRST_COMPLETED")
    first = done.pop()
    new_proof = ast.literal_eval(first.result().decode())
    if 'proof' in new_proof:
        return new_proof["proof"]
    return 0

# def valid_proof(last_hash, proof):
#     guess = f'{proof}'.encode()
#     guess_hash = hashlib.sha256(guess).hexdigest()
#     return guess_hash[:6] == last_hash[-6:]

# def proof_of_work(last_proof, start, step):
#     proof = start
#     #  TODO: Your code here
#     encode_last_proof = f'{last_proof}'.encode()
#     last_hash = hashlib.sha256(encode_last_proof).hexdigest()
#     while valid_proof(last_hash, proof) is False:
#         proof += step
#     return proof

async def main():
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com"
    coins_mined = 0
    f = open("./blockchain/my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()
    if len(id) == 0:
        f = open("./blockchain/my_id.txt", "w")
        # Generate a globally unique ID
        id = str(uuid4()).replace('-', '')
        print("Created new ID: " + id)
        f.write(id)
        f.close()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = await create_lambda_batch(data.get('proof'), 30)
        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))

asyncio.run(main())

# if __name__ == '__main__':
#     # What node are we interacting with?
#     if len(sys.argv) > 1:
#         node = sys.argv[1]
#     else:
#         node = "https://lambda-coin.herokuapp.com"

#     coins_mined = 0

#     # Load or create ID
#     f = open("./blockchain/my_id.txt", "r")
#     id = f.read()
#     print("ID is", id)
#     f.close()
#     if len(id) == 0:
#         f = open("./blockchain/my_id.txt", "w")
#         # Generate a globally unique ID
#         id = str(uuid4()).replace('-', '')
#         print("Created new ID: " + id)
#         f.write(id)
#         f.close()
#     # Run forever until interrupted
#     while True:
#         # Get the last proof from the server
#         r = requests.get(url=node + "/last_proof")
#         data = r.json()
#         new_proof = proof_of_work(data.get('proof'))

#         post_data = {"proof": new_proof,
#                      "id": id}

#         r = requests.post(url=node + "/mine", json=post_data)
#         data = r.json()
#         if data.get('message') == 'New Block Forged':
#             coins_mined += 1
#             print("Total coins mined: " + str(coins_mined))
#         else:
#             print(data.get('message'))
