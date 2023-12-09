"""
THIS FILE GENERATES AN ACCESS TOKEN USING YOUR MNEMONIC PHRASE FROM .env

RUN VIA 'python3 ./gen_wc_access_token.py' AND COPY THE OUTPUT TO YOUR .env FILE
"""

import os

from dotenv import load_dotenv
from farcaster import Warpcast

load_dotenv()

# Make sure to set FARCASTER_MNEMONIC in your .env file
wc = Warpcast(os.getenv("FARCASTER_MNEMONIC"))

# prints true if the client is connected to the farcaster node
print(wc.get_healthcheck())

# expires in 1 year
minutes = 525600

# Generate a new access token
access_token = wc.create_new_auth_token(expires_in=minutes)

# save it to FARC_SECRET in your .env file
print(access_token)
