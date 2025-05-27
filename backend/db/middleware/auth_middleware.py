import boto3
from fastapi import Cookie, HTTPException
from secret_keys import SecretKeys


cognito_client = boto3.client(
    "cognito-idp", region_name=SecretKeys().REGION_NAME
)  # Adjust region as needed


def _get_user_from_cognito(access_token: str):

    try:
        response = cognito_client.get_user(AccessToken=access_token)

        return {
            attr["Name"]: attr["Value"] for attr in response.get("UserAttributes", [])
        } 
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token: " + str(e),
        )


def get_current_user(access_token: str = Cookie(None)):

    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Access token is required. User not authenticated.",
        )

    user_info = _get_user_from_cognito(access_token)

    if not user_info:
        raise HTTPException(
            status_code=401,
            detail="User not found or invalid access token.",
        )

    print("User Info:", user_info)  # Debugging line to check user info
    return user_info
