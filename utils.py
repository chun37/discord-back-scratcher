from typing import List


def snake_case_to_title_case(string: str) -> str:
    return string.replace("_", " ").title()


def permissions_to_error_text(permissions: List[str]) -> str:
    missing_perms_txt = (
        f"`{snake_case_to_title_case(permission)}`" for permission in permissions
    )
    return f"権限 {', '.join(missing_perms_txt)} を追加してください"
