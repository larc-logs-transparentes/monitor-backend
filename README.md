# monitor-backend
Backend of monitor

###### Task 1: Database Replicator
###### Task 2: API for root verification
___

## Database Replicator
###### Background routine to get global tree data from original LogServer and copy to own server
#### Process is started automatically with API, and closes automatically a few seconds after API is shutdown
#### Every period, determined in it's config, the routine checks LogServer for new data. If there is, it copies it to own db.
___

## API for root verification
###### API offers endpoints for getting and checking roots

#### GET: get all roots: {url}/all_roots/{year}
```commandline
Send: {year} in address
url/all_roots/2023

Receive:
[
    {
        "_id": "6648b8b4932a0b5b3b3f60c5",
        "value": "58923e1f08b8338868e38491a9f284d1643849ce1e147342c91758c48a30e70f",
        "tree_name": "global_tree",
        "tree_size": 2,
        "signature": "10338a00350e784b5e8fc7df017d7e58334b48ebd9cef5f05ab32bb053d1f159fa5ef5e1becfefb4767f11c4cc9246cca85ae97ad7fe5d28374087a25ef0f20c",
        "timestamp": "2024-05-08T12:53:14.451184"
    },
    ...,
    {
        "_id": "664a7c55555c984db2e743d0",
        "value": "1aea4a83c833bac93eacf2f1baa5a36ed79d727e1230f781b353a6f9cec10a1c",
        "tree_name": "global_tree",
        "tree_size": 7,
        "signature": "cfd05a2251046a29b77ab2e97f9431b2ab705392427f72548a6c85a6dcbdabcfc6de590d3e5214755c82d085fd0e5c636b3457412adf42be8ab544e688e91b00",
        "timestamp": "2024-05-08T12:53:15.663054"
    }
]
```

#### GET: check one root: /check_root/{year}/{value}
```commandline
Send: {year} and {root value} in address
url/check_root/2023/c20364057fed49aa36403dabb6e29c4877656ee08d016a2dd567456e03ef5ebc

Receive: "match" (boolean) if got root in db, and "root" object or "error"
{
    "match": true,
    "root": {
        "_id": "6648b8b4932a0b5b3b3f60c6",
        "value": "c20364057fed49aa36403dabb6e29c4877656ee08d016a2dd567456e03ef5ebc",
        "tree_name": "global_tree",
        "tree_size": 3,
        "signature": "a1be5cf4dd5bfd8e70a8cd35df1ace2d05400f0fdc66a804c497c244e199b4b6b05279829ecfc98cf9caea437d34f70a6fc4a0bb973e198d36ef88f549370708",
        "timestamp": "2024-05-08T12:53:14.716154"
    }
}

or

{
    "match": false,
    "error": "Raiz não encontrada."
}
```

#### POST: check one root: /check_root/
```commandline
Send: "year" and "root" object in body of POST
{
    "year": 2023,
    "root": {
        "value": "c20364057fed49aa36403dabb6e29c4877656ee08d016a2dd567456e03ef5ebc",
        "tree_size": 3,
        "signature": "a1be5cf4dd5bfd8e70a8cd35df1ace2d05400f0fdc66a804c497c244e199b4b6b05279829ecfc98cf9caea437d34f70a6fc4a0bb973e198d36ef88f549370708"
    }
}

Receive: "match" (boolean) if got root in db, and "db_root" object or "error"
{
    "signature": true,
    "value": true,
    "match": true,
    "db_root": {
        "_id": "6648b8b4932a0b5b3b3f60c6",
        "value": "c20364057fed49aa36403dabb6e29c4877656ee08d016a2dd567456e03ef5ebc",
        "tree_name": "global_tree",
        "tree_size": 3,
        "signature": "a1be5cf4dd5bfd8e70a8cd35df1ace2d05400f0fdc66a804c497c244e199b4b6b05279829ecfc98cf9caea437d34f70a6fc4a0bb973e198d36ef88f549370708",
        "timestamp": "2024-05-08T12:53:14.716154"
    }
}

or validation status (signature and value), "db_root" found with tree_size, and hint of possible error

{
    "signature": true,
    "value": false,
    "match": false,
    "db_root": {
        "_id": "6648b8b4932a0b5b3b3f60c6",
        "value": "c20364057fed49aa36403dabb6e29c4877656ee08d016a2dd567456e03ef5ebc",
        "tree_name": "global_tree",
        "tree_size": 3,
        "signature": "a1be5cf4dd5bfd8e70a8cd35df1ace2d05400f0fdc66a804c497c244e199b4b6b05279829ecfc98cf9caea437d34f70a6fc4a0bb973e198d36ef88f549370708",
        "timestamp": "2024-05-08T12:53:14.716154"
    },
    "hint": "Verifique se o atributo tree_size enviado contém o valor correto."
}

or, if tree_size is not present in db,

{
    "match": false,
    "db": false,
    "error_key": "db",
    "error": "Banco de dados ainda não alcançou a raíz pedida, tente novamente mais tarde."
}
```