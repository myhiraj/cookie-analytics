from datetime import datetime, date, time

class Cookie:

    '''
    Represents a single cookie and its activity history, grouped by date.

    Raises:
        ValueError: If name is empty or whitespace.
    '''

    def __init__(self, name: str, timestamps: list[datetime] | None = None):
        if not name or not name.strip():
            raise ValueError("Cookie name cannot be empty")
        
        self.name: str = name
        self._activity: dict[date, list[time]] = {} # date → list of times seen on that date

        if timestamps is not None:
            self.insert_timestamps(timestamps)
    
    def insert_timestamps(self, timestamps: list[datetime]):
        '''Adds one or more timestamps to this cookie's activity history.'''
        for timestamp in timestamps:
            if timestamp.date() not in self._activity:
                self._activity[timestamp.date()] = [timestamp.time()]
            else:
                self._activity[timestamp.date()].append(timestamp.time())

    def get_activity_by_date(self, target_date: date) -> list[time]:
        '''Returns all recorded times this cookie was seen on the given date.'''
        return self._activity.get(target_date, [])

    def get_activity_frequency_by_date(self, target_date: date) -> int:
        '''Returns the frequency of this cookie's activity on the given date.'''
        return len(self.get_activity_by_date(target_date))

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Cookie(name={self.name}, activity={self._activity})"
    
    def __eq__(self, other):
        if not isinstance(other, Cookie):
            return NotImplemented
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
