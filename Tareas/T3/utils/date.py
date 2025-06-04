def date_to_days(date: str, separator: str = "-"):
    years, months, days = map(int, date.split(separator))

    return years * 60 * 60 + months * 60 + days
