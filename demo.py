import jwt
from jwksutils import rsa_pem_from_jwk
import requests

# To run this example, follow the instructions in the project README

# obtain jwks from "https://login.microsoftonline.com/common/discovery/keys"). jwks_uri found in https://login.microsoftonline.com/common/.well-known/openid-configuration
response = requests.get("https://login.microsoftonline.com/common/discovery/keys")
jwks = response.json()

# configuration, these can be seen in valid JWTs from Azure:
valid_audiences = ['{Application-ID}'] # id of the application (i.e managed Identity) receiving the token
issuer = 'https://sts.windows.net/{tenantid}/' # iss in JWT and issuer in https://login.microsoftonline.com/common/.well-known/openid-configuration


class InvalidAuthorizationToken(Exception):
    def __init__(self, details):
        super().__init__('Invalid authorization token: ' + details)


def get_kid(token):
    headers = jwt.get_unverified_header(token)
    if not headers:
        raise InvalidAuthorizationToken('missing headers')
    try:
        return headers['kid']
    except KeyError:
        raise InvalidAuthorizationToken('missing kid')


def get_jwk(kid):
    for jwk in jwks.get('keys'):
        if jwk.get('kid') == kid:
            return jwk
    raise InvalidAuthorizationToken('kid not recognized')


def get_public_key(token):
    return rsa_pem_from_jwk(get_jwk(get_kid(token)))


def validate_jwt(jwt_to_validate):
    public_key = get_public_key(jwt_to_validate)

    decoded = jwt.decode(jwt_to_validate,
                         public_key,
                         verify=True,
                         algorithms=['RS256'],
                         audience=valid_audiences,
                         options={"verify_exp": False},  #remove this for prod, use this just for testing with old expired token
                         issuer=issuer)

    # do what you wish with decoded token:
    # if we get here, the JWT is validated
    print(decoded)


def main():
    import sys
    import traceback

    if len(sys.argv) < 2:
        print('Please provide a JWT as script argument')
        return
    
    jwt = sys.argv[1]

    if not jwt:
        print('Please pass a valid JWT')

    try:
        validate_jwt(jwt)
    except Exception as ex:
        traceback.print_exc()
        print('The JWT is not valid!')
    else:
        print('The JWT is valid!')


if __name__ == '__main__':
    main()
