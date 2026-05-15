from datetime import datetime, date, time

class Cookie:

    def __init__(self, name: str, timestamps: list[datetime] | None = None):
        self.name: str = name
        self._activity: dict[date, list[time]] = {}

        if timestamps is not None:
            self.insert_timestamps(timestamps)
    
    def insert_timestamps(self, timestamps: list[datetime]):
        for timestamp in timestamps:
            if timestamp.date() not in self._activity:
                self._activity[timestamp.date()] = [timestamp.time()]
            else:
                self._activity[timestamp.date()].append(timestamp.time())

    def get_activity_by_date(self, target_date: date):
        return self._activity.get(target_date, [])

    def get_activity_frequency_by_date(self, target_date: date):
        return len(self.get_activity_by_date(target_date))

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Cookie(name={self.name}, activity={self._activity})"
    
    def __hash__(self):
        return hash(self.name)
