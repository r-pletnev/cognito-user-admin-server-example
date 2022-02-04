import boto3
from typing import Optional


class CognitoProvider:
    def __init__(self, user_pool_id: str):
        self.user_pool_id = user_pool_id
        self.client = boto3.client("cognito-idp")

    def get_user_pools(self, max_results: Optional[int] = 50) -> dict:
        return self.client.list_user_pools(MaxResults=max_results)

    def get_user_list(self, email: Optional[str] = None):
        filter_param = ""
        if email:
            filter_param = f'email = "{email}"'

        return self.client.list_users(UserPoolId=self.user_pool_id, Filter=filter_param)

    def create_user(self, email: str):
        user_attributes = [
            {"Name": "email", "Value": email},
        ]
        self.client.admin_create_user(
            UserPoolId=self.user_pool_id, Username=email, UserAttributes=user_attributes
        )

    def delete_user(self, email: str):
        self.client.admin_delete_user(UserPoolId=self.user_pool_id, Username=email)
