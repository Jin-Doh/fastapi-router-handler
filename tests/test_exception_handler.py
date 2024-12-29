import pytest
from fastapi import HTTPException


async def async_success_func():
    return {"message": "success"}


async def async_error_func():
    raise ValueError("test error")


def sync_success_func():
    return {"message": "success"}


def sync_error_func():
    raise ValueError("test error")


class TestExceptionHandler:
    @pytest.mark.asyncio
    async def test_async_success_case(self, exception_handler):
        result = await exception_handler.exception_handler(async_success_func)
        assert isinstance(result, dict), f"Expected dict, got {type(result)}"
        assert result == {
            "message": "success"
        }, f"Expected {'message': 'success'}, got {result}"

    @pytest.mark.asyncio
    async def test_sync_success_case(self, exception_handler):
        result = await exception_handler.exception_handler(sync_success_func)
        assert isinstance(result, dict), f"Expected dict, got {type(result)}"
        assert result == {
            "message": "success"
        }, f"Expected {'message': 'success'}, got {result}"

    @pytest.mark.asyncio
    async def test_async_error_case(self, exception_handler):
        with pytest.raises(HTTPException) as exc_info:
            await exception_handler.exception_handler(
                async_error_func, e_code=400, e_msg="Custom error message"
            )
        assert isinstance(
            exc_info.value, HTTPException
        ), f"Expected HTTPException, got {type(exc_info.value)}"
        assert (
            exc_info.value.status_code == 400
        ), f"Expected status code 400, got {exc_info.value.status_code}"
        p_1 = "Expected detail 'Custom error message',"
        p_2 = f"got {exc_info.value.detail}"
        assert exc_info.value.detail == "Custom error message", f"{p_1} {p_2}"

    @pytest.mark.asyncio
    async def test_with_params(self, exception_handler):
        async def func_with_params(params):
            return {"params": params}

        result = await exception_handler.exception_handler(
            func_with_params, func_params={"test": "value"}
        )
        assert isinstance(result, dict), f"Expected dict, got {type(result)}"
        assert result == {
            "params": {"test": "value"}
        }, f"Expected {'params': {'test': 'value'}}, got {result}"

    @pytest.mark.asyncio
    async def test_with_custom_error_handler(self, exception_handler):
        custom_handled = False

        def custom_error_handler(e):
            nonlocal custom_handled
            custom_handled = True

        await exception_handler.exception_handler(
            sync_error_func, additional_error_handle=custom_error_handler
        )
        assert (
            custom_handled is True
        ), f"Expected custom_handled to be True, got {custom_handled}"
