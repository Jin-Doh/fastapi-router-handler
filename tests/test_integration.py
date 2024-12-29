def test_integration_with_fastapi(app, client, exception_handler):
    @app.get("/test")
    async def test_endpoint():
        return await exception_handler.exception_handler(
            lambda: {"message": "success"},
        )

    @app.get("/error")
    async def error_endpoint():
        return await exception_handler.exception_handler(
            lambda: (_ for _ in ()).throw(ValueError("test error")),
            e_code=400,
            e_msg="Custom error message",
        )

    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "success"}

    response = client.get("/error")
    assert response.status_code == 400
    assert response.json()["detail"] == "Custom error message"
