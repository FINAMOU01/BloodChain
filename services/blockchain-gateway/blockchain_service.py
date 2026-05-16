from .web3_client import get_web3
from .config import CONTRACT_ADDRESS

def register_bag(bag_id: str, blood_type: str):
    w3 = get_web3()
    if not w3.is_connected():
        raise ConnectionError("Blockchain not available")
    
    print(f"Registering bag on blockchain: {bag_id} and {blood_type}")
    
    return {
        "tx_hash": None,
        "status": "pending"
    }