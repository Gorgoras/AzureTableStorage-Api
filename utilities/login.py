import os
from azure.keyvault.secrets import SecretClient
from azure.identity import ManagedIdentityCredential
from azure.identity import ClientSecretCredential



def getConnectionString():
    """Retrieves the connection string using either Managed Identity
    or Service Principal"""

    KeyVault_DNS = os.environ["KeyVault_DNS"]
    SecretName = os.environ["SecretName"]

    try:
        creds = ManagedIdentityCredential()
        client = SecretClient(vault_url=KeyVault_DNS, credential=creds)
        retrieved_secret = client.get_secret(SecretName)
    except:
        creds = ClientSecretCredential( client_id=os.environ["SP_ID"],
                                        client_secret=os.environ["SP_SECRET"],
                                        tenant_id=os.environ["TENANT_ID"])
        client = SecretClient(vault_url=KeyVault_DNS, credential=creds)
        retrieved_secret = client.get_secret(SecretName)
        
    return retrieved_secret