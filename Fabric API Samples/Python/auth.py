import msal
from dotenv import load_dotenv
import os

load_dotenv('.env')

# Variables
tenant_id = os.getenv("TENANT_ID")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
scopes = ["https://api.fabric.microsoft.com/.default"]


def interactive_auth():
    """
    Authenticates the user interactively and returns an access token.

    This function uses the `msal` library to authenticate the user interactively using the provided client ID,
    authority URL, and tenant ID. It acquires an access token for the specified scopes and returns it if the authentication is successful.
    If authentication fails, it prints the error details and returns None.

    Returns:
        str: The access token if authentication is successful, None otherwise.
    """

    app = msal.PublicClientApplication(
        client_id=client_id,
        enable_broker_on_windows=True,
        authority="https://login.microsoftonline.com/" + tenant_id
    )

    result = app.acquire_token_interactive(scopes=scopes)

    if "access_token" in result:
        access_token = result["access_token"]
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))
        access_token = None
    
    return access_token


def client_auth():
    """
    Authenticates the client and returns an access token.

    This function uses the `msal` library to authenticate the client using the provided client ID, client secret,
    and authority URL. It acquires an access token for the specified scopes and returns it if the authentication is successful.
    If authentication fails, it prints the error details and returns None.

    Returns:
        str: The access token if authentication is successful, None otherwise.
    """
    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority="https://login.microsoftonline.com/" + tenant_id
    )

    result = app.acquire_token_for_client(scopes=scopes)

    if "access_token" in result:
        access_token = result["access_token"]
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))
        access_token = None
    
    return access_token
