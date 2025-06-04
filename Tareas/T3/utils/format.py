from collections import namedtuple


def format_field(field: str) -> str:
    return field.replace("_", " ").capitalize()


def format_header(header: list[str]) -> list[str]:
    return [format_field(field) for field in header]


def format_namedtuples(values: list[namedtuple]) -> tuple[list[str], list[list[str]]]:
    header = format_header(values[0]._fields if values else [])

    rows = []

    for value in values:
        row = []

        for field in value._fields:
            row.append(str(getattr(value, field)))

        rows.append(row)

    return header, rows


def format_dicts(values: list[dict]) -> tuple[list[str], list[list[str]]]:
    if not values:
        return [], []

    header = values[0].keys()
    rows = []

    for value in values:
        row = [str(value[key]) for key in header]
        rows.append(row)

    return format_header(header), rows
