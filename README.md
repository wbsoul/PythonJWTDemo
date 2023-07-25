# Validating JWTs with Python
This demo demonstrates how to validate JWTs using Python, obtaining RSA public keys from JWKS.

This code has been described in this blog post: [https://robertoprevato.github.io/Validating-JWT-Bearer-tokens-from-Azure-AD-in-Python/](https://robertoprevato.github.io/Validating-JWT-Bearer-tokens-from-Azure-AD-in-Python/).

**Important**: this code is just an example: it contains configuration to validate JWTs issued by Azure AD, for an application configured in my test tenant.

This code have been slightly modified to get all the JWT keys from: "https://login.microsoftonline.com/common/discovery/keys"


# Install requirements
Note: `cryptography` package might require extra dependencies, please refer to its documentation to know how to install it.

# Example
```bash
python demo.py <JWT>
```
