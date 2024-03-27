import datetime
import pathlib

import ics


def find_calendars():
    calendar_paths = dict()
    for path in pathlib.Path("data").glob("**/*.cal"):
        location = path.parts[1:-1]
        calendar_paths[location] = calendar_paths.get(location, [])
        calendar_paths[location].append(path)
    calendars = []
    for location, paths in calendar_paths.items():
        calendars.append(get_calendar(location, paths))
    return calendars


def get_calendar(location, paths):
    calendar = Calendar(location)
    for path in paths:
        with open(path, encoding="utf-8") as f:
            calendar.parse(f)
    return calendar


def generate_calendars():
    calendars = find_calendars()
    base = pathlib.Path("generated")
    for calendar in calendars:
        path = base / pathlib.Path(*calendar.location)
        path.mkdir(parents=True, exist_ok=True)
        file = path / "festivus.ics"
        with open(file, "w") as f:
            f.write(calendar.as_ical().serialize())

    with open(base / "index.html", "w") as f:
        f.write(
            """
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
        <ul>
        """
        )
        prev_last_year = None
        for calendar in sorted(
            calendars, key=lambda c: (-c.years()[-1], c.location[::-1])
        ):
            last_year = calendar.years()[-1]
            if last_year != prev_last_year:
                if prev_last_year:
                    f.write("</ul></li>")
                f.write(f"<li>{last_year}<ul>")
            url = "/".join(list(calendar.location) + ["festivus.ics"])
            f.write(
                f'<li><a href="{url}">{calendar.location[2]}</a> {calendar.location[1]}, {calendar.location[0]} {calendar.years()}</li>'
            )
            prev_last_year = last_year
        f.write("</ul></li></ul></body>")


class Calendar:
    def __init__(self, location):
        self.location = location
        self.days = []

    def parse(self, f):
        source = f.readline()
        for line in f:
            self.add(Day(line.strip(), source.strip()))

    def add(self, day):
        self.days.append(day)

    def __repr__(self):
        return f"{self.location} {repr(self.days)}"

    def as_ical(self):
        ical = ics.Calendar()
        for day in self.days:
            event = ics.Event(
                name=day.description, description=day.source, begin=day.date
            )
            event.make_all_day()
            ical.events.add(event)
        return ical

    def years(self):
        return sorted(set([d.date.year for d in self.days]))


class Day:
    def __init__(self, line, source):
        date_str, self.description = line.split(" ", 1)
        self.date = datetime.date.fromisoformat(date_str)
        self.source = source

    def __str__(self):
        return f"{self.date} {self.description} {self.source}"

    def __repr__(self):
        return repr(str(self))


if __name__ == "__main__":
    generate_calendars()
