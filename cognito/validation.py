import json
import os

import jwt
import urllib.request


def get_well_known_jwk(region: str, user_pool_id: str) -> dict:
    jwk_url = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"
    with urllib.request.urlopen(jwk_url) as url:
        jwks = json.loads(url.read().decode())
    public_keys = {}
    for jwk in jwks["keys"]:
        kid = jwk["kid"]
        public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
    return public_keys


def is_valid_token(access_token: str) -> (bool, str):
    public_keys = get_well_known_jwk(
        os.environ.get("AWS_DEFAULT_REGION"), os.environ.get("M2M_USER_POOL_ID")
    )
    try:
        kid = jwt.get_unverified_header(access_token).get("kid")
    except jwt.DecodeError as err:
        return False, f"token invalid. {err}"
    key = public_keys[kid]
    try:
        payload = jwt.decode(access_token, key=key, algorithms=["RS256"])
    except jwt.InvalidTokenError as err:
        return False, f"Error: {err}"

    if payload["client_id"] != os.environ.get("M2M_CLIENT_ID"):
        return False, "Wrong m2m client id"
    if payload["scope"] != os.environ.get("M2M_SCOPE"):
        return False, "Wrong m2m scope"
    return True, ""


if __name__ == "__main__":
    pass
