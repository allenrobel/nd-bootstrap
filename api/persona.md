# Persona

## Endpoint Path

/v2/bootstrap/persona

## Endpoint Method

POST

## Request Body

```json
{
  "persona": "LAN",
  "minExternalIPS": 3
}
```

## Response

### 500

#### Text

Number of nodes are zero

### 200

#### Body

```json
{
  "persona":"LAN",
  "clusterSize":1
}
```

