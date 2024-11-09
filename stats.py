import datetime
import pathlib


WEEKDAYS = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)
KINDS = {
    "(Estatal)": "Spain",
    "(Local)": "City",
    "(Autonómica)": "Autonomous community",
    "(Autonòmica)": "Autonomous community",
}

print(
    "\t".join(
        (
            "country",
            "autonomous_community",
            "city",
            "year",
            "month",
            "day",
            "weekday number",
            "weekday name",
            "date",
            "kind",
            "name",
        )
    )
)


for f in pathlib.Path(".").glob("*/*/*/*/*.cal"):
    if str(f) in (
        "data/España/Comunitat Valenciana/Paterna/2022.cal",
        "data/España/Comunitat Valenciana/Burjassot/2022.cal",
    ):
        continue
    for line in f.read_text().splitlines():
        if line.startswith("#"):
            continue
        date, rest = line.split(" ", 1)
        name, kind = rest.rsplit(" ", 1)
        date = datetime.date.fromisoformat(date)
        _, country, autonomous_community, city, _ = f.parts
        row = (
            country,
            autonomous_community,
            city,
            date.year,
            date.month,
            date.day,
            date.weekday(),
            WEEKDAYS[date.weekday()],
            date.isoformat(),
            KINDS[kind],
            name,
        )
        print("\t".join(map(str, row)))
