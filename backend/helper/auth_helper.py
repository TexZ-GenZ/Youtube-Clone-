import base64
import hashlib
import hmac

def get_secret_hash(
    client_id: str,
    client_secret: str,
    username: str,
) :
    message = username + client_id

    digest = hmac.new(
        client_secret.encode("utf-8"),
        message.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()

    return base64.b64encode(digest).decode()