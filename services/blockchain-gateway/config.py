from decouple import config

SEPOLIA_RPC_URL = config('SEPOLIA_RPC_URL', default="")
CONTRACT_ADDRESS = config('CONTRACT_ADDRESS', default="")
PRIVATE_KEY = config('PRIVATE_KEY', default="")
LOCAL_RPC_URL = "http://127.0.0.1:8545"