from pandas._libs.tslibs.timestamps import Timestamp
from pandas import Series
from datetime import datetime

def count_days(serie: Series) -> Series:
    try:
        serie=serie.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    except:
        pass
    min_date=serie.min()
    return (serie - min_date).apply(lambda x: x.days)