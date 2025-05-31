from collections import namedtuple


def formatField(field: str) -> str:
    return field.replace("_", " ").capitalize()


def formatHeader(header: list[str]) -> list[str]:
    return [formatField(field) for field in header]


def formatNamedtuples(values: list[namedtuple]) -> tuple[list[str], list[list[str]]]:
    header = formatHeader(values[0]._fields if values else [])

    rows = []

    for value in values:
        row = []

        for field in value._fields:
            row.append(str(getattr(value, field)))

        rows.append(row)

    return formatHeader(header), rows


def formatDicts(values: list[dict]) -> tuple[list[str], list[list[str]]]:
    if not values:
        return [], []

    header = values[0].keys()
    rows = []

    for value in values:
        row = [str(value[key]) for key in header]
        rows.append(row)

    return formatHeader(header), rows
