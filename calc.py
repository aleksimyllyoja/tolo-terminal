t0 = datetime.date(2015, 4, 7)
t1 = datetime.date(2015, 5, 7)

index = 'omxh25'

mi = 100
ci = sum = seed = 100
ae = 0.018

cols = ['date', 'sum', 'ic']

#--

if NEW_MONTH:
    sum += mi

if NEW_YEAR:
    sum -= sum*ae

sum*=ic
