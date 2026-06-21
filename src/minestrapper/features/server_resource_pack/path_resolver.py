from pathlib import Path

def resolve_server_path(path_str: str, server_root: str | Path) -> Path:
    if (not path_str):
        raise ValueError(
            "Resource pack path is not set in config."
            "Did you mean to disable the server_resource_pack feature?"
        )

    path = Path(path_str)

    if not path.is_absolute():
        path = Path(server_root) / path

    path = path.resolve()

    if (not path.exists()):
        raise ValueError(f"Resource pack path {path} does not exist.")
    
    if (not path.is_file()):
        raise ValueError(f"Resource pack path {path} is not a file.")
    
    if (path.suffix.lower() != ".zip"):
        raise ValueError(f"Resource pack path {path} is not a zip file.")
    
    return path
