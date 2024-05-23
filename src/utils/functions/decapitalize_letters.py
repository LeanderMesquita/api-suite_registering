def decapitalize_letters(captalized_str: str) -> str:
    try:
        return ''.join([char.lower() if char.isupper() else char for char in captalized_str])
    except Exception as e:
        raise e


