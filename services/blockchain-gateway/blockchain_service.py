"""Blockchain gateway service - handles blockchain interactions for blood tracking."""

import sys
import os

# Setup path for imports
sys.path.insert(0, os.path.dirname(__file__))


def get_web3():
    """Get Web3 instance with fallback if web3 not installed."""
    try:
        from web3 import Web3
        return Web3()
    except (ImportError, ModuleNotFoundError):
        # Return None if web3 not available
        return None


def register_bag(bag_id: str, blood_type: str):
    """Register a blood bag on the blockchain."""
    w3 = get_web3()
    
    if w3 is None:
        # Fallback: web3 not available, return pending status
        print(f"Registering bag on blockchain (fallback mode): {bag_id} and {blood_type}")
        return {
            "tx_hash": None,
            "status": "pending_blockchain_unavailable"
        }
    
    if not w3.is_connected():
        raise ConnectionError("Blockchain not available")
    
    print(f"Registering bag on blockchain: {bag_id} and {blood_type}")
    
    return {
        "tx_hash": None,
        "status": "pending"
    }


if __name__ == "__main__":
    print("Blockchain gateway service running...")
    print(f"Sample registration: {register_bag('BAG001', 'O+')}")