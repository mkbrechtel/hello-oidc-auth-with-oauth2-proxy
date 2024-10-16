# Hello OIDC Authentication with oauth2-proxy!

An example on how to implement OIDC Authentication with oauth2-proxy and different Apps/Frameworks.

## Setup

```
docker-compose -f compose.yaml -f compose.fastapi.yaml up
```

## Login
Go to [localhost:8007](http://localhost:8007)

Test user: `asdf` pass: `asdf`

## Services

- [FastAPI App (without auth)](http://localhost:8000)
- [Keycloak](http://localhost:8009)
- [oauth2-proxy](http://localhost:8007)
    - [userinfo](http://localhost:8007/oauth2/userinfo)
    - [sign in](http://localhost:8007/oauth2/sign_in)
    - [sign out](http://localhost:8007/oauth2/sign_out?rd=http://localhost:8009/realms/hello/protocol/openid-connect/logout)

## Development

### Update Keycloak Test Realm
To update the keycloak realm configuration, you can use the keycloak admin cli.
```
chmod -R a+rwX keycloak/data/import/
docker-compose down
docker-compose run --rm keycloak export --dir /opt/keycloak/data/import --realm hello
```

This will update your import files in keycloak/data/import.
