import datetime
import os
from datetime import datetime as dt

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from sqlalchemy.exc import IntegrityError

from db import session
from db.model import Task
from utils import DateParser

load_dotenv()


class GoogleCalendar:
    __calendarId = os.getenv("CALENDAR_ID")

    def __init__(self, creds):
        self.__creds = creds
        self.__service = build('calendar', 'v3', credentials=creds)

    def getEvents(self):
        try:
            events = self.__service.events().list(calendarId=self.__calendarId).execute()
            return events
        except HttpError as err:
            print(err)

    def save(self, events):
        new_events = []

        for event in events:
            try:
                time = event.due.datetime if event.due.datetime is not None else event.due.date
                e = Task(task_id=event.id, title=event.content, description=event.description, date=time)
                session.add(e)
                session.commit()
            except IntegrityError as e:
                session.rollback()
                continue

            new_events.append(self.__transformToCalendarEventWithoutTimestamp(event))

        for event in new_events:
            self.__service.events().insert(calendarId=self.__calendarId, body=event).execute()

        return new_events

    @staticmethod
    def __transformToCalendarEventWithoutTimestamp(event):
        if event.due is None:
            raise Exception('Event without date')

        formats = '%Y-%m-%d' if event.due.datetime is None else '%Y-%m-%dT%H:%M:%S'
        time = event.due.datetime if event.due.datetime is not None else event.due.date
        delta = datetime.timedelta(minutes=5) if event.due.datetime is not None else datetime.timedelta(days=1)

        newEvent = {
            'summary': event.content,
            'description': event.description,
            'start': {
                'dateTime': dt.strftime(dt.strptime(time, formats), '%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'Europe/Moscow',
            },
            'end': {
                'dateTime': dt.strftime(dt.strptime(time, formats) + delta,
                                        '%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'Europe/Moscow',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 5},
                ],
            },
        }

        if event.due.recurring:
            newEvent['recurrence'] = []
            newEvent.get('recurrence').append(DateParser.lex(event.due.string))

        return newEvent
