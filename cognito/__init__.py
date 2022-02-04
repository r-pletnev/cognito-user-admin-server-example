from .client import CognitoProvider

import os


cognito_client = CognitoProvider(user_pool_id=os.environ.get("USER_POOL_ID"))
