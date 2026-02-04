import json, os

class TimeTable:
    def __init__(self, filename="timetable.json"):
        self.filename = filename
        self.schedule = {}
        self.faculty_availability = {}
        self.load()

    def add_class(self, day, time, subject, faculty, classroom):
        if day not in self.schedule:
            self.schedule[day] = []
        self.schedule[day].append((time, subject, faculty, classroom))
        self.save()

    def remove_class(self, day, time, subject=None):
        if day in self.schedule:
            self.schedule[day] = [
                (t, s, f, c) for (t, s, f, c) in self.schedule[day]
                if not (t == time and (subject is None or s == subject))
            ]
            self.save()

    def mark_faculty_unavailable(self, faculty):
        self.faculty_availability[faculty] = False
        self.auto_manage(faculty)
        self.save()

    def auto_manage(self, faculty):
        for day, classes in self.schedule.items():
            new_classes = []
            for time, subject, f, classroom in classes:
                if f == faculty:
                    substitute = self.find_substitute(faculty)
                    if substitute:
                        new_classes.append((time, subject, substitute, classroom))
                    else:
                        swapped = self.swap_class(subject, faculty, day, time, classroom)
                        new_classes.append(swapped if swapped else (time, subject, "POSTPONED", classroom))
                else:
                    new_classes.append((time, subject, f, classroom))
            self.schedule[day] = new_classes

    def swap_class(self, subject, faculty, current_day, current_time, classroom):
        days = sorted(self.schedule.keys())
        for day in days:
            if day > current_day:
                for idx, (t, s, f, c) in enumerate(self.schedule[day]):
                    if s == subject and f == faculty:
                        if any(f == faculty and c == classroom for (t2, s2, f, c) in self.schedule[current_day]):
                            continue
                        self.schedule[day].pop(idx)
                        return (current_time, subject, faculty, classroom)
        return None

    def find_substitute(self, faculty):
        for f, available in self.faculty_availability.items():
            if available and f != faculty:
                return f
        return None

    def save(self):
        with open(self.filename, "w") as f:
            json.dump({"schedule": self.schedule, "faculty_availability": self.faculty_availability}, f, indent=4)

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.schedule = data.get("schedule", {})
                self.faculty_availability = data.get("faculty_availability", {})
