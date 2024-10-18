def adicionar_cookie_tema(response, tema):
    response.set_cookie(
        key="tema",
        value=tema.lower(),
        httponly=True,
        expires="2099-01-01T00:00:00Z",
        samesite="lax",
    )
