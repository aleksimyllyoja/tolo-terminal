import datetime
import itertools
import csv
from dateutil.rrule import rrule, DAILY

SEPARATOR = "#-"

def read_conf_and_logic():
    ls = open('calc.py', 'r').readlines()
    conf = compile(''.join(
        list(
            itertools.takewhile(
                lambda x: not x.startswith(SEPARATOR),
                ls
            )
        )
    ), 'conf', 'exec')
    logic = compile(''.join(
        list(
            itertools.dropwhile(
                lambda x: not x.startswith(SEPARATOR),
                ls
            )
        )
    ), 'logic', 'exec')
    return(conf, logic)

def read_index(fn):
    ivals = dict([
        (   datetime.datetime.strptime(l[0], '%d.%m.%Y').date(),
            float(l[1].replace(',', '.'))
        ) for l in
        csv.reader(open(fn), delimiter=';')
    ])

    def get_last(d):
        v = ivals.get(d)
        while not v:
            d = d-datetime.timedelta(days=1)
            v = ivals.get(d)

        return v

    last = get_last(t0-datetime.timedelta(days=1))
    for d in rrule(DAILY, dtstart=t0-datetime.timedelta(days=1), until=t1):
        if d.date() in ivals.keys():
            last = ivals.get(d.date())
        else:
            ivals[d.date()] = last

    return ivals

def get_data():
    conf, logic = read_conf_and_logic()

    exec(conf, globals())

    ivals = read_index('data/'+index+'.csv')
    data = []

    for date in rrule(DAILY, dtstart=t0, until=t1):
        yesterday = date - datetime.timedelta(days=1)
        date = date.date()
        ic = ivals.get(date)/ivals.get(yesterday.date())

        NEW_MONTH = yesterday.month != date.month
        NEW_YEAR = yesterday.year != date.year

        globals().update({
            'ic': ic,
            'NEW_YEAR': NEW_YEAR,
            'NEW_MONTH': NEW_MONTH
        })
        exec(logic, globals())

        data.append([date, sum, ic])

    return cols, data
