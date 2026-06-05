"""Web3 client for blockchain interactions."""


def get_config():
    """Load configuration with fallback."""
    try:
        from config import LOCAL_RPC_URL, WEB3_PROVIDER_URI
        return LOCAL_RPC_URL, WEB3_PROVIDER_URI
    except (ImportError, ModuleNotFoundError):
        # Fallback if config module not available
        return "http://localhost:8545", None


def get_web3():
    """Get Web3 instance."""
    try:
        from web3 import Web3
        local_rpc, provider_uri = get_config()
        if provider_uri:
            return Web3(Web3.HTTPProvider(provider_uri))
        return Web3(Web3.HTTPProvider(local_rpc))
    except (ImportError, ModuleNotFoundError):
        return None


def check_connection():
    """Check blockchain connection."""
    w3 = get_web3()
    if w3 is None:
        return False
    return w3.is_connected()