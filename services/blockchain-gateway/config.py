from decouple import config

WEB3_PROVIDER_URI = config('WEB3_PROVIDER_URI', default="http://127.0.0.1:8545")
CONTRACT_ADDRESS = config('CONTRACT_ADDRESS', default="")
PRIVATE_KEY = config('PRIVATE_KEY', default="")
LOCAL_RPC_URL = "http://127.0.0.1:8545"