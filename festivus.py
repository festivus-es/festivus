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
    for calendar in calendars:
        path = pathlib.Path("generated") / pathlib.Path(*calendar.location)
        path.mkdir(parents=True, exist_ok=True)
        file = path / "festivus.ics"
        with open(file, "w") as f:
            f.write(str(calendar.as_ical()))


class Calendar:
    def __init__(self, location):
        self.location = location
        self.days = []

    def parse(self, f):
        source = f.readline()
        while True:
            line = f.readline()
            if not line:
                break
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
