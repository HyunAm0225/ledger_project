# Ledger Project

## Run Server

```shell
docker-compose up -d --no-deps --build
```

## Test Django Server
```shell
docker-compose run django python manage.py test
```


# API 명세

## User

### token_info

```json
{
  "access_token": str,
  "refresh_token": str,
  "expires_at": int,
}
```

### user_info

```json
{
  "id": int,
  "email": str,
  "created_at": str,
  "updated_at": str,
}
```

### Users.register

- 회원가입 API
- [POST] /users/register/

**request.body**

```json
{  
  "email" : str,
  "password" : str
}
```

response

```json
{
  "token" : <token_info>,
  "user" : <user_info>
}
```

### Users.Login

- 로그인 API
- [POST] /users/login/

request.body

```json
{
  "email" : str,
  "password" : str
}
```

res

```json
{
  "user" : <user_info>,
  "token_info" : <token_info>
}
```

### Users.Logout

- 로그아웃 API
- [POST] /users/logout
- isAuthenticated

**request.body**

```json
{
  "refresh_token" : str,
}
```

response

```json
{
  "result" : True,
}
```

## Ledger

### ledger_info

```json
{
  "id": int,
  "user": int,
  "memo": str,
  "amount": int,
  "created_at": str,
  "updated_at": str,
  "is_active": bool,
}
```

### [POST] ledegers

- 금액, 메모 작성
- isAuthenticated

**request.body**

```json
{
  "amount" : int, // biginteger field
  "memo" : str
}
```

**response**

```json
{
  "result" : bool,
  "ledgers" : <ledger_info>
}
```

### [PATCH] ledgers.pk

- 수정기능
- isAuthenticated

request.body

```json
{
  "amount" : int, // nullable
  "memo" : str // nullable
}
```

**response**

```json
{
  "result" : bool,
  "ledgers" : ledger_info
}
```

### [DELETE] ledgers.pk

- 삭제기능
- isAuthenticated

request.body

```json
{

}
```

**response**

```json
{
  "result" : bool,
  "ledgers" : <ledger_info>
}
```

### [PATCH] ledgers.pk.restore

- 복구기능
- isAuthenticated

request.body

```json
{

}
```

**response**

```json
{
  "result" : bool,
  "ledgers" : <ledger_info>
}
```

### [GET] ledgers

- 가계부 리스트 보는 기능
    - 추가기능(해당 유저의 가계부만 보이게 구현)
- isAuthenticated

request.body

```json
{

}
```

**response**

```json
{
  "result" : bool,
  "ledgers" : [<ledger_info>]
}
```

### [GET] ledgers.pk

- 가계부 세부내역 보는 기능
    - 추가기능(해당 유저의 가계부만 보이게 구현)
- isAuthenticated

request.body

```json
{

}
```

**response**

```json
{
  "result" : bool,
  "ledgers" : <ledger_info>
}
```