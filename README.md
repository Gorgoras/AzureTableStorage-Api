# AzureTableStorage-Api

![CI](https://github.com/Gorgoras/AzureTableStorage-Api/workflows/CI/badge.svg)

Azure functions wrapper for common table operations that are not easy to get with standard queries to Azure Table Storage.

**Authentication**

The function will try to authenticate with the data lake by using a connection string, stored as a secret in a Key Vault. If running in the cloud, it will try to login with a Managed Identity, and if that fails it will try with a Service Principal (useful to debug on premise). 

For this function to work properly on premise, you need to add the local.settings.json file at root level and set the following attributes:
* TENANT_ID: self explanatory.
* SP_ID: the application ID for the Service Principal.
* SP_SECRET: the aplication secret for the Service Principal.
* KeyVault_DNS: the dns pointing towards the Keyvault storing the connection string as a secret (e.g: https://keyvault-name.vault.azure.net/).
* SecretName: the name of the secret where the connection string is stored.

To deploy and run this function to Azure, make sure to set those attributes at Settings->Configuration as Application Settings. If you set a Managed Identity for the Function app, then you only need to set the last 2 attributes, as the other ones are used to authenticate as a Service Principal.

Also, remember to authorize the Service Principal or the Managed Identity to the secrets at the Azure Key Vault.

**Endpoints**
* [createTable](documentation/createTable.md) :
	*	`POST /api/createTable/` 
	*	`GET /api/createTable/` 

* [getAggFromTable](documentation/getAggFromTable.md) : 
	* `POST /api/getAggFromTable/` 
	* `GET /api/getAggFromTable/` 

* [cleanTableStorage](documentation/cleanTableStorage.md) :
	*	`POST /api/cleanTableStorage/` 
	*	`GET /api/cleanTableStorage/` 

* [bulkInsert](documentation/bulkInsert.md) :
	*	`POST /api/bulkInsert/` 

* [insertRow](documentation/insertRow.md) :
	*	`POST /api/insertRow/` 

* [deleteRows](documentation/deleteRows.md) :
	*	`POST /api/deleteRows/` 
	*	`GET /api/deleteRows/` 

