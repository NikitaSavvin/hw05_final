import datetime as dt


def year(request):
    yr = dt.datetime.today().year
    return {
        'year': yr
    }
