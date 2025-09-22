from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

def sign_document(document_hash: str) -> bytes:
    signature = private_key.sign(
        document_hash.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature

def verify_signature(document_hash: str, signature: bytes) -> bool:
    try:
        public_key.verify(
            signature,
            document_hash.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False
