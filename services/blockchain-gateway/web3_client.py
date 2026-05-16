from web3 import Web3
from .config import LOCAL_RPC_URL, SEPOLIA_RPC_URL

def get_web3():
    if SEPOLIA_RPC_URL:
        return Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
    return Web3(Web3.HTTPProvider(LOCAL_RPC_URL))

def check_connection():
    w3 = get_web3()
    return w3.is_connected()