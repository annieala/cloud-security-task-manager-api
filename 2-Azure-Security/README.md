# Task 2: Ensuring Application Data Security

## Overview

This guide walks you through securing your Task Manager API using Azure's enterprise security features. You'll implement encrypted storage with customer-managed keys and deploy your API through Azure API Management with authentication, rate limiting, and HTTPS enforcement.


---

## Prerequisites

- Completed Task 1 (Flask Task Manager API)
- Active Azure Sandbox environment via Microsoft Learn
- Azure Portal access
- Basic understanding of REST APIs and Azure services

---

## Part 1: Secure Data Storage with Azure Storage 
### Objective
Secure your task data by implementing encrypted blob storage with customer-managed encryption keys.

### Step 1.1: Create Azure Storage Account

1. **Navigate to Azure Portal**
   - Go to [portal.azure.com](https://portal.azure.com)
   - Click **"Create a resource"** → Search for **"Storage account"**

2. **Configure Storage Account**
   - **Subscription:** Select your Microsoft Learn Sandbox subscription
   - **Resource Group:** Use existing or create new (e.g., `rg-taskmanager`)
   - **Storage account name:** Choose unique name (e.g., `sttaskmanager[yourname]`)
   - **Region:** Select closest region to your location
   - **Performance:** Standard
   - **Redundancy:** LRS (Locally Redundant Storage) - sufficient for sandbox

3. **Advanced Settings**
   - Under **Security**, ensure **"Enable storage account key access"** is checked
   - Click **"Review + Create"** → **"Create"**
   - Wait for deployment to complete (~2 minutes)

### Step 1.2: Create Blob Container

1. **Navigate to Your Storage Account**
   - Go to **"Containers"** under Data storage section
   - Click **"+ Container"**

2. **Configure Container**
   - **Name:** `task-data`
   - **Public access level:** Private (no anonymous access)
   - Click **"Create"**

### Step 1.3: Verify Storage Service Encryption (SSE)

1. **Check Default Encryption**
   - In your Storage Account, go to **"Encryption"** under Security + networking
   - Verify **"Encryption type"** shows **"Microsoft-managed keys (MMK)"**
   - Note: SSE is enabled by default and encrypts data at rest

📸 **Screenshot Required:** Capture the Encryption settings page showing SSE enabled with date/time visible

### Step 1.4: Implement Customer-Managed Keys (CMK)

#### Create Azure Key Vault

1. **Create Key Vault Resource**
   - Click **"Create a resource"** → Search for **"Key Vault"**
   - **Resource Group:** Same as Storage Account
   - **Key vault name:** Unique name (e.g., `kv-taskmanager-[yourname]`)
   - **Region:** Same as Storage Account
   - **Pricing tier:** Standard

2. **Configure Access**
   - Go to **"Access policies"** (or **"Access configuration"** in newer portal)
   - Ensure access policy model is selected
   - Click **"Create"**

#### Create Encryption Key

1. **Generate Key in Key Vault**
   - Open your Key Vault
   - Go to **"Keys"** under Objects
   - Click **"+ Generate/Import"**
   - **Options:** Generate
   - **Name:** `storage-encryption-key`
   - **Key type:** RSA
   - **RSA key size:** 2048
   - Click **"Create"**

#### Link Storage Account to Key Vault

1. **Enable Managed Identity on Storage Account**
   - Go to your Storage Account
   - Navigate to **"Identity"** under Security + networking
   - Turn **"System assigned"** status to **On**
   - Click **"Save"** and note the Object ID

2. **Grant Storage Account Access to Key Vault**
   - Go back to your Key Vault
   - Click **"Access policies"**
   - Click **"+ Create"** (or **"+ Add Access Policy"**)
   - **Key permissions:** Select **"Get"**, **"Unwrap Key"**, **"Wrap Key"**
   - Click **"Next"**
   - **Principal:** Search for your Storage Account name and select it
   - Click **"Next"** → **"Next"** → **"Create"**

3. **Configure CMK on Storage Account**
   - Return to your Storage Account
   - Go to **"Encryption"** under Security + networking
   - Change **"Encryption type"** to **"Customer-managed keys"**
   - **Encryption key:** Select **"Select from Key Vault"**
   - Choose your Key Vault and the key you created
   - **Identity type:** System-assigned managed identity
   - Click **"Save"**

📸 **Screenshot Required:** 
- Key Vault overview showing the encryption key
- Storage Account encryption page showing CMK configuration with Key Vault linked

### Step 1.5: Enable Secure Transfer (HTTPS)

1. **Configure Secure Transfer**
   - In your Storage Account, go to **"Configuration"** under Settings
   - Find **"Secure transfer required"**
   - Set to **"Enabled"** (should be enabled by default)
   - Click **"Save"** if you made changes

📸 **Screenshot Required:** Configuration page showing "Secure transfer required" enabled with date/time

---

## Part 2: Protect API with Azure API Management 

### Objective
Deploy your Task Manager API through Azure API Management with authentication, rate limiting, CORS policies, IP filtering, and HTTPS enforcement.

### Step 2.1: Deploy Azure API Management

1. **Create APIM Resource**
   - Click **"Create a resource"** → Search for **"API Management"**
   - **Subscription:** Microsoft Learn Sandbox
   - **Resource Group:** Same as previous resources
   - **Region:** Same as Storage Account
   - **Resource name:** Unique name (e.g., `apim-taskmanager-[yourname]`)
   - **Organization name:** Your name or organization
   - **Administrator email:** Your email
   - **Pricing tier:** **Consumption** (best for sandbox/development)
   
   > **Note:** Consumption tier provisions faster (~5 minutes) compared to other tiers

2. **Complete Deployment**
   - Click **"Review + Create"** → **"Create"**
   - Wait for deployment (Consumption tier: ~5 min, Developer tier: ~40 min)

### Step 2.2: Import Your Flask API

#### Option A: Using OpenAPI/Swagger (Recommended)

1. **Generate Swagger from Flask**
   - Install flask-swagger-ui:
     ```bash
     pip install flask-swagger-ui flask-restx
     ```
   
2. **Update your Flask app** to include Swagger:
   ```python
   from flask import Flask, jsonify, request
   from flask_restx import Api, Resource, fields
   
   app = Flask(__name__)
   api = Api(app, version='1.0', title='Task Manager API',
             description='A simple Task Manager API')
   
   task_model = api.model('Task', {
       'id': fields.Integer(required=True),
       'title': fields.String(required=True),
       'description': fields.String(),
       'completed': fields.Boolean()
   })
   
   # Your existing task routes here...
   ```

3. **Import to APIM**
   - In APIM, go to **"APIs"** → Click **"+ Add API"**
   - Select **"OpenAPI"**
   - **OpenAPI specification:** Paste your API's Swagger URL or upload file
   - **Display name:** Task Manager API
   - **Name:** task-manager-api
   - **API URL suffix:** tasks
   - Click **"Create"**

#### Option B: Manual Definition

1. **Create Blank API**
   - In APIM, go to **"APIs"** → **"+ Add API"**
   - Select **"HTTP"** or **"Blank API"**
   - **Display name:** Task Manager API
   - **Name:** task-manager-api
   - **Web service URL:** Your Flask API URL (if deployed) or `http://localhost:5000`
   - **API URL suffix:** tasks

2. **Add Operations Manually**
   - Click **"+ Add operation"**
   - Example for GET all tasks:
     - **Display name:** Get All Tasks
     - **Name:** get-all-tasks
     - **URL:** GET /tasks
   - Repeat for POST, PUT, DELETE operations

#### Option C: Using HTTP Endpoint (If API is deployed/tunneled)

1. **Expose Local Flask API** (if testing locally):
   ```bash
   # Install ngrok
   ngrok http 5000
   ```
   - Copy the HTTPS URL provided by ngrok

2. **Import to APIM**
   - Select **"HTTP"** API type
   - Use the ngrok URL as **"Web service URL"**

### Step 2.3: Implement Authentication

Choose ONE of the following methods:

#### Option A: Subscription Keys (Simplest)

1. **Enable Subscription Requirement**
   - Go to your API in APIM
   - Click **"Settings"**
   - Ensure **"Subscription required"** is checked
   - Click **"Save"**

2. **Create Subscription**
   - Go to **"Subscriptions"** in APIM
   - Click **"+ Add subscription"**
   - **Name:** `task-manager-subscription`
   - **Display name:** Task Manager Access
   - **Scope:** Select your API
   - Click **"Create"**
   - Copy the **Primary key** (you'll use this in API requests)

3. **Test with Subscription Key**
   ```bash
   curl -H "Ocp-Apim-Subscription-Key: YOUR_KEY_HERE" \
        https://your-apim.azure-api.net/tasks/tasks
   ```

📸 **Screenshot Required:** Subscriptions page showing created subscription with key (can hide part of the key)

#### Option B: OAuth 2.0 / JWT with Azure AD (Advanced)

1. **Register App in Azure AD**
   - Go to **"Azure Active Directory"** → **"App registrations"**
   - Click **"+ New registration"**
   - **Name:** TaskManagerAPIApp
   - Click **"Register"**

2. **Configure API Permissions**
   - In your app, go to **"API permissions"**
   - Add necessary permissions

3. **Add Validation Policy in APIM**
   - Go to your API → **"Design"** tab
   - Click **"All operations"**
   - In **"Inbound processing"**, click **"</>""** (Code editor)
   - Add JWT validation policy:
   ```xml
   <inbound>
       <validate-jwt header-name="Authorization" failed-validation-httpcode="401">
           <openid-config url="https://login.microsoftonline.com/{tenant-id}/.well-known/openid-configuration" />
           <audiences>
               <audience>api://your-app-id</audience>
           </audiences>
       </validate-jwt>
   </inbound>
   ```

📸 **Screenshot Required:** Policy configuration showing JWT validation settings

### Step 2.4: Configure Rate Limiting

1. **Add Rate Limit Policy**
   - Go to your API → **"Design"** tab
   - Select **"All operations"**
   - In **"Inbound processing"**, click **"+ Add policy"**
   - Select **"Limit call rate"** (or edit code directly)

2. **Configure Limits**
   - Click **"</>""** to edit XML:
   ```xml
   <inbound>
       <rate-limit calls="10" renewal-period="60" />
       <quota calls="100" renewal-period="86400" />
   </inbound>
   ```
   - This limits to 10 calls per minute and 100 calls per day
   - Adjust values based on your requirements

3. **Save Configuration**

📸 **Screenshot Required:** Policy editor showing rate-limit configuration with visible parameters

### Step 2.5: Configure CORS Policy

1. **Add CORS Policy**
   - In **"Inbound processing"**, click **"+ Add policy"**
   - Select **"CORS"** or edit XML:
   ```xml
   <inbound>
       <cors allow-credentials="true">
           <allowed-origins>
               <origin>https://yourdomain.com</origin>
               <origin>http://localhost:3000</origin>
           </allowed-origins>
           <allowed-methods>
               <method>GET</method>
               <method>POST</method>
               <method>PUT</method>
               <method>DELETE</method>
           </allowed-methods>
           <allowed-headers>
               <header>*</header>
           </allowed-headers>
       </cors>
   </inbound>
   ```

2. **Customize Origins**
   - Replace with your actual client domains
   - For testing, you can use `*` but avoid in production

📸 **Screenshot Required:** CORS policy configuration showing allowed origins and methods

### Step 2.6: Configure IP Filtering

1. **Add IP Filter Policy**
   - In **"Inbound processing"**, add IP filtering:
   ```xml
   <inbound>
       <ip-filter action="allow">
           <address>192.168.1.100</address>
           <address-range from="10.0.0.1" to="10.0.0.255" />
       </ip-filter>
   </inbound>
   ```
   - **OR** to block specific IPs:
   ```xml
   <inbound>
       <ip-filter action="forbid">
           <address>203.0.113.5</address>
       </ip-filter>
   </inbound>
   ```

2. **Get Your Current IP**
   - Visit https://whatismyipaddress.com/
   - Add your IP to the allow list for testing

📸 **Screenshot Required:** IP filter policy showing configured IP addresses/ranges

### Step 2.7: Enforce HTTPS

1. **Verify HTTPS Enforcement**
   - In APIM, go to **"APIs"** → Your API → **"Settings"**
   - **URL scheme:** Ensure **"HTTPS"** is selected (HTTP should be unchecked)
   - Click **"Save"**

2. **Test HTTP Rejection** (Optional)
   - Try accessing via HTTP - should fail:
   ```bash
   curl http://your-apim.azure-api.net/tasks/tasks
   ```

### Step 2.8: Complete Policy Configuration Example

Here's a complete policy combining all security measures:

```xml
<policies>
    <inbound>
        <base />
        <!-- Rate Limiting -->
        <rate-limit calls="10" renewal-period="60" />
        <quota calls="100" renewal-period="86400" />
        
        <!-- IP Filtering -->
        <ip-filter action="allow">
            <address>YOUR_IP_ADDRESS</address>
        </ip-filter>
        
        <!-- CORS -->
        <cors allow-credentials="true">
            <allowed-origins>
                <origin>https://yourdomain.com</origin>
            </allowed-origins>
            <allowed-methods>
                <method>GET</method>
                <method>POST</method>
                <method>PUT</method>
                <method>DELETE</method>
            </allowed-methods>
            <allowed-headers>
                <header>*</header>
            </allowed-headers>
        </cors>
        
        <!-- JWT Validation (if using OAuth) -->
        <!-- <validate-jwt header-name="Authorization">
            <openid-config url="https://login.microsoftonline.com/{tenant}/.well-known/openid-configuration" />
        </validate-jwt> -->
        
    </inbound>
    <backend>
        <base />
    </backend>
    <outbound>
        <base />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>
```

---

## Testing Your Secured API

### Test with Subscription Key

```bash
# Set your variables
APIM_URL="https://your-apim.azure-api.net/tasks"
SUBSCRIPTION_KEY="your-subscription-key"

# GET all tasks
curl -H "Ocp-Apim-Subscription-Key: $SUBSCRIPTION_KEY" $APIM_URL/tasks

# POST new task
curl -X POST \
  -H "Ocp-Apim-Subscription-Key: $SUBSCRIPTION_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","description":"Testing APIM","completed":false}' \
  $APIM_URL/tasks
```

### Test Rate Limiting

Run multiple requests quickly to trigger rate limit:

```bash
for i in {1..15}; do
  curl -H "Ocp-Apim-Subscription-Key: $SUBSCRIPTION_KEY" $APIM_URL/tasks
  echo "Request $i"
done
```

Expected: First 10 succeed, then 429 (Too Many Requests) errors.

### Connect to Secure Blob Storage from Flask

Update your Flask app to use Azure Blob Storage:

```python
from azure.storage.blob import BlobServiceClient
import os
import json

# Connection string from Storage Account
connection_string = "your_connection_string_here"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "task-data"

@app.route('/tasks', methods=['GET'])
def get_tasks():
    blob_client = blob_service_client.get_blob_client(
        container=container_name, 
        blob="tasks.json"
    )
    try:
        tasks_data = blob_client.download_blob().readall()
        tasks = json.loads(tasks_data)
        return jsonify(tasks)
    except:
        return jsonify([])

@app.route('/tasks', methods=['POST'])
def create_task():
    # Get existing tasks
    # Add new task
    # Upload updated tasks to blob
    # ...
```

---

## Screenshot Checklist

### Part 1: Storage Security 
- [ ] SSE Encryption settings showing Microsoft-managed keys enabled
- [ ] Key Vault showing encryption key created
- [ ] Storage Account encryption page showing CMK with Key Vault linked
- [ ] Configuration page showing "Secure transfer required" enabled

### Part 2: API Management
- [ ] Authentication setup (Subscription keys OR OAuth/JWT configuration)
- [ ] Rate limiting policy with visible parameters (calls, renewal period)
- [ ] CORS policy showing allowed origins and methods
- [ ] IP filtering policy with configured IP addresses
- [ ] API Settings showing HTTPS enforcement

**Important:** All screenshots must have date/time visible (Windows: Win+Shift+S, Mac: Cmd+Shift+4)

---

## Common Issues & Troubleshooting

### Storage Account Issues

**Issue:** Cannot enable CMK
- **Solution:** Ensure managed identity is enabled on Storage Account first
- Check Key Vault access policies include the Storage Account

**Issue:** "Secure transfer required" grayed out
- **Solution:** This is usually already enabled by default. If you see it enabled, you're good.

### APIM Issues

**Issue:** APIM deployment taking too long
- **Solution:** Use Consumption tier (5 min) instead of Developer tier (40 min)

**Issue:** 401 Unauthorized errors
- **Solution:** Ensure subscription key is included in request header: `Ocp-Apim-Subscription-Key`

**Issue:** Rate limit not working
- **Solution:** Verify policy is in "Inbound processing" section and saved properly

**Issue:** CORS errors in browser
- **Solution:** Add your client origin to allowed origins in CORS policy

**Issue:** IP filter blocking you
- **Solution:** Get your current public IP and add it to the allow list

### Backend Connection Issues

**Issue:** APIM can't reach local Flask API
- **Solution:** 
  - Deploy Flask to Azure App Service, or
  - Use ngrok to expose local API: `ngrok http 5000`
  - Use ngrok HTTPS URL in APIM backend

---

## Best Practices

### Security
1. **Never commit keys:** Use Azure Key Vault references in code
2. **Rotate keys regularly:** Set up key rotation policies in Key Vault
3. **Use managed identities:** Avoid storing connection strings when possible
4. **Apply least privilege:** Grant minimum necessary permissions

### API Management
1. **Start with restrictive policies:** Loosen gradually as needed
2. **Monitor usage:** Use APIM analytics to detect unusual patterns
3. **Version your APIs:** Use versioning for backward compatibility
4. **Cache responses:** Add caching policies for frequently accessed data

### Development
1. **Test in sandbox first:** Always test before production
2. **Use separate environments:** Dev, staging, production
3. **Document your APIs:** Use OpenAPI/Swagger specifications
4. **Implement logging:** Add Application Insights for monitoring

---

## Additional Resources

### Official Documentation
- [Azure Storage Encryption](https://learn.microsoft.com/en-us/azure/storage/common/storage-service-encryption)
- [Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/)
- [Azure API Management](https://learn.microsoft.com/en-us/azure/api-management/)
- [APIM Policies](https://learn.microsoft.com/en-us/azure/api-management/api-management-policies)

### Tutorials
- [Secure Azure Storage with CMK](https://learn.microsoft.com/en-us/azure/storage/common/customer-managed-keys-configure-key-vault)
- [Protect APIs with APIM](https://learn.microsoft.com/en-us/azure/api-management/api-management-howto-protect-backend-with-aad)

### Tools
- [Azure Storage Explorer](https://azure.microsoft.com/en-us/features/storage-explorer/)
- [Postman](https://www.postman.com/) - API testing
- [ngrok](https://ngrok.com/) - Expose local APIs

---

## Submission Guidelines

1. **Complete all steps** in both Part 1 and Part 2
2. **Take all required screenshots** with visible date/time stamps
3. **Organize screenshots** clearly labeled:
   - `screenshot_1_sse_encryption.png`
   - `screenshot_2_keyvault_key.png`
   - `screenshot_3_cmk_configuration.png`
   - etc.
4. **Test your API** through APIM before submission
5. **Document any deviations** from instructions with explanations

---

## Conclusion

By completing this task, you've implemented enterprise-grade security for your Task Manager API including:
- ✅ Encrypted data storage with customer-managed keys
- ✅ Secure HTTPS-only communication
- ✅ API authentication and access control
- ✅ Rate limiting and abuse prevention
- ✅ CORS and IP filtering policies

These are production-ready security practices used by organizations worldwide to protect their APIs and data.

**Good luck! 🚀**

---

## Quick Reference Commands

```bash
# Install Azure SDK for Python (if integrating storage)
pip install azure-storage-blob azure-identity

# Get your public IP
curl https://api.ipify.org

# Test APIM endpoint
curl -H "Ocp-Apim-Subscription-Key: YOUR_KEY" \
     https://your-apim.azure-api.net/tasks/tasks

# Run ngrok for local testing
ngrok http 5000
```

---

*Last Updated: November 2025*
*Compatible with: Azure Portal (Current), Microsoft Learn Sandbox*