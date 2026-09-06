# Verify Remote Services

## Endpoint

/bootstrap/verifyremoteservices

## Verb

POST

## Request Body

{
  "nameServers": [
    "192.168.7.1"
  ],
  "ntpConfig": {
    "servers": [
      {
        "host": "192.168.7.6",
        "prefer": true
      }
    ]
  }
}

## Response

200 no body
