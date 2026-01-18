def validate_luau(code: str) -> bool:
    return "loadstring" in code and "HttpGet" in code
