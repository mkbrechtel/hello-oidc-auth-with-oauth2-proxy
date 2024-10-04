# Hello OIDC Authentication with oauth2-proxy and Python!

An example on how to implement OIDC Authentication with oauth2-proxy and Python.

## Setup

```
docker-compose up
```

## Services

- Keycloak http://localhost:8009
- oauth2-proxy http://localhost:8007


## Update Keycloak Test Realm
To update the keycloak realm configuration, you can use the keycloak admin cli.
```
chmod -R a+rwX keycloak/data/import/
docker-compose down
docker-compose run --rm keycloak export --dir /opt/keycloak/data/import --realm hello
```

This will update your local in keycloak/data/import.
