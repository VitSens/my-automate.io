from dotenv import load_dotenv

from config import getToken
from integration import GoogleCalendar, Todoist

load_dotenv()

calendar = GoogleCalendar(getToken())


def createEvents():
    events = Todoist.getTasksByLabelIds(2161489278)
    calendar.save(events)


if __name__ == "__main__":
    createEvents()
