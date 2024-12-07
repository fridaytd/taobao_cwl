import json
import pathlib

from typing import TypeVar, Type
from app.shared.exceptions import JsonError

T_Var = TypeVar("T_Var", dict, list)


def read_json(
    json_path: pathlib.Path,
    output_type: Type[T_Var],
) -> T_Var:
    with open(json_path) as f:
        data = json.load(f)

    if not isinstance(data, output_type):
        raise JsonError(
            f"data is an instance of {type(data)}, is not instance of {output_type}"
        )

    return data


def write_json(
    json_path: pathlib.Path,
    data: dict | list,
) -> None:
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)
