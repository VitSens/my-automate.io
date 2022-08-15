class DateParser(object):

    @staticmethod
    def lex(line):
        lines = line.strip().split(' ')

        default = 'RRULE:'

        recurrenceType = {
            'every': 'FREQ=',
            'day': 'DAILY;',
        }

        for lan in lines:
            if recurrenceType.get(lan):
                default += recurrenceType.get(lan)

        return default
