# README

## Install

```sh
pip install -e .
# Run the cli
subnetting
```

# Blog


## Login

This was a bit more tedious mainly because of my lack knowledge of ASP.NET's framework.

I first I tracked via a browser/burp the login flow (or so I thought..):

```sh
>> POST Account/Login
>>      body {username, password, state, boilerplate} 

<< Set-Cookie: .ASPXAUTH=AUTHENTICATION_COOKIE_HERE; path=/; HttpOnly; SameSite=Lax
```

Simple enough..

This is where I learned how ASP.NET does MAC more specifically, I had wired an initial `GET` to the homepage to generate the state, but transitioning from `GET /` -> `POST /Account/Login` was a no go with `__VIEWSTATE`.

So I just to swap for `GET /Account/Login` -> `POST /Account/Login` in hindsight obvious and I should just default to assuming the pages are sensitve to proper state flow.

So the updated flow

```sh
>> GET Account/Login
        # Pick up the login page state from HTML as usual
>> POST Account/Login
>>      body {username, password, state, boilerplate} 

<< Set-Cookie: .ASPXAUTH=AUTHENTICATION_COOKIE_HERE; path=/; HttpOnly; SameSite=Lax
```

Awesome this worked. Lastly I tested on an authenticated route to ensure my shiny new cookie worked:

```sh
>> GET Account/Profile
```

## Refactor `Game` class

I wanted build or methods but this architecture was getting bloated and logic was leaking everywhere.

I reviewed another api wrapper repo I like https://github.com/tenable/pyTenable for inspiration

The way Steve seperated the main class `TenableSC` and forks into seperate modules is great and where I'm heading my design to.

Here's what I ended up on:

```
# ./subnetting/base.py
class Endpoint:
def __init__(self, api: "Game"):
    self._api = api

# ./subnetting/account.py
class AccountAPI(Endpoint):
    def login(self, username: str, password: str) -> None: ...

# main.py
game.account.login(username, password)
```

### Adjustments for state

Attemping to use this nesting pattern proved to not work well for my use case.

The main difference between pyTenable and mine? State. Which I chose to add state optionally, I could simplify functions and not allow state, but state allows for more complex features in the future. Which I'm not sure I'd need, so should I remove my state and make a bunch of stateless functions? Probably.

