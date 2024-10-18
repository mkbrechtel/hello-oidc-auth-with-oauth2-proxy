# Hello OIDC Authentication with oauth2-proxy!

An example on how to implement OIDC Authentication with oauth2-proxy and different Apps/Frameworks.

## Run!

To choose one of the different app setups run:
- FastAPI: `make app=fastapi`
- Flask: `make app=flask`
- [whoami test service](https://github.com/traefik/whoami): `make app=whoami`

Then go to http://localhost:4180

## Login
Go to [localhost:8007](http://localhost:8007)

Test user: `asdf` pass: `asdf`

## Services

- [Keycloak](http://localhost:8009)
- [oauth2-proxy](http://localhost:4180)
    - [userinfo](http://localhost:4180/oauth2/userinfo)
    - [sign in](http://localhost:4180/oauth2/sign_in)
    - [sign out](http://localhost:4180/oauth2/sign_out?rd=http://localhost:8009/realms/hello/protocol/openid-connect/logout)

## Development

### Update Keycloak Test Realm
To update the keycloak realm configuration, you can use the keycloak admin cli.
```
chmod -R a+rwX keycloak/data/import/
docker-compose down --remove-orphans
docker-compose run --rm keycloak export --dir /opt/keycloak/data/import --realm hello
```

This will update your import files in keycloak/data/import.
