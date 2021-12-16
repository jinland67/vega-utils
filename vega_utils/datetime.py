import re
import time
import random
import calendar
import pytz
from dateutil.parser import parse
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

# ----------------------------------------------------
# User define library import area
# ----------------------------------------------------
from vega_utils.string import StringHandle as sh


class DatetimeHandleError(Exception):
    # -----------------------------------------------
    # 생성할 때 value 값을 입력 받은다.
    # -----------------------------------------------
    def __init__(self, value):
        self.value = value

    # -----------------------------------------------
    # 생성할 때 받은 value 값을 확인 한다.
    # -----------------------------------------------
    def __str__(self):
        return self.value

class DatetimeHandle:
    # ======================================
    # 주어진 숫자의 100만분의 1초
    # ======================================
    @staticmethod
    def usleep(sleep_time):
        try:
            time.sleep(sleep_time/1000000)
        except Exception as e:
            msg = 'DatetimeHandle exception occured in usleep(). Message: %s' % str(e)
            raise DatetimeHandleError(msg)

    # ======================================
    # 주어진 범위 안에서 random하게 sleep
    # ======================================
    @staticmethod
    def rsleep(**kwargs):
        try:
            range_sleep = (1, 3)
            for i, j in kwargs.items():
                if i == 'range':
                    range_sleep = j
            sleep_time = random.randrange(range_sleep[0], range_sleep[1]) * random.random()
            time.sleep(sleep_time)
        except Exception as e:
            msg = 'DatetimeHandle exception occured in rsleep(). Message: %s' % str(e)
            raise DatetimeHandleError(msg)

    # ======================================
    # 현재 시간을 문자열로 리턴
    # now(format='%Y-%m-%d %H:%M:%S')
    # ======================================
    @staticmethod
    def now(**kwargs):
        try:
            format = '%Y-%m-%d %H:%M:%S'
            for i, j in kwargs.items():
                if i == 'format':
                    format = j
            return datetime.now().strftime(format)
        except Exception as e:
            msg = 'DatetimeHandle exception occured in now(). Message: %s' % str(e)
            raise DatetimeHandleError(msg)

    # ======================================
    # 오늘 날짜를 문자열로 리턴
    # format = '%Y-%m-%d'
    # ======================================
    @staticmethod
    def today(**kwargs):
        try:
            format = '%Y-%m-%d'
            for i, j in kwargs.items():
                if i == 'format':
                    format = j
            return date.today().strftime(format)
        except Exception as e:
            msg = 'DatetimeHandle exception occured in today(). Message: %s' % str(e)
            raise DatetimeHandleError(msg)

    # ======================================
    # 어제 날짜를 문자열로 리턴
    # format = '%Y-%m-%d'
    # ======================================
    @staticmethod
    def yesterday(**kwargs):
        try:
            format = '%Y-%m-%d'
            for i, j in kwargs.items():
                if i == 'format':
                    format = j
            return (date.today() - timedelta(days=1)).strftime(format)
        except Exception as e:
            msg = 'DatetimeHandle exception occured in yesterday(). Message: %s' % str(e)
            raise DatetimeHandleError(msg)

    # ======================================
    # 내일 일자를 문자열로 리턴
    # format = '%Y-%m-%d'
    # ======================================
    @staticmethod
    def tomorrow(**kwargs):
        try:
            format = '%Y-%m-%d'
            for i, j in kwargs.items():
                if i == 'format':
                    format = j
            return (date.today() + timedelta(days=1)).strftime(format)
        except Exception as e:
            msg = 'DatetimeHandle exception occured in tomorrow(). Message: %s' % str(e)
            raise DatetimeHandleError(msg)

    # ======================================
    # 해당월의 마지막 일자를 리턴
    # ======================================
    @staticmethod
    def last_day(year, month):
        try:
            return str(calendar.monthrange(int(year), int(month))[1])
        except Exception as e:
            msg = 'DatetimeHandle exception occured in last_day(). Message: %s' % str(e)
            raise DatetimeHandleError(msg)

    # ======================================
    # 문자 데이타를 date type으로 리턴
    # datetime('2021-01-01', format='date')
    # datetime('2021-01-01', format='datetime')
    # ======================================
    @staticmethod
    def datetime(str_date, **kwargs):
        try:
            type = ''
            for i, j in kwargs.items():
                if i == 'format':
                    type = j
            date_time = parse(str_date)
            if type == 'date':
                return date_time.strftime('%Y-%m-%d')
            elif type == 'datetime':
                return date_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                return ''
        except Exception as e:
            msg = 'DatetimeHandle exception occured in datetime(). Message: %s' % str(e)
            raise DatetimeHandleError(msg)

    # ======================================
    # 날자를 계산해서 계산된 날짜를 문자열로 리턴
    # calc_date(ago=('2021-04-13', 'day', 1))
    # calc_date(after=('2021-04-13', 'day', 1))
    # ======================================
    @staticmethod
    def calc_date(**kwargs):
        try:
            calc_type = ''
            calc_data = ()
            if len(kwargs.items()) == 0:
                return ''
            for i, j in kwargs.items():
                if i == 'ago':
                    calc_type = 'ago'
                    calc_data = j
                if i == 'after':
                    calc_type = 'after'
                    calc_data = j
            if len(calc_data) != 3:
                return ''
            base_date = datetime.strptime(calc_data[0], '%Y-%m-%d').date()
            if calc_type == 'ago':
                if calc_data[1] == 'day':
                    return (base_date - timedelta(days=calc_data[2])).strftime('%Y-%m-%d')
                elif calc_data[1] == 'week':
                    return (base_date - timedelta(weeks=calc_data[2])).strftime('%Y-%m-%d')
                elif calc_data[1] == 'month':
                    return (base_date - relativedelta(months=calc_data[2])).strftime('%Y-%m-%d')
                elif calc_data[1] == 'year':
                    return (base_date - relativedelta(years=calc_data[2])).strftime('%Y-%m-%d')
                else:
                    return ''
            elif calc_type == 'after':
                if calc_data[1] == 'day':
                    return (base_date + timedelta(days=calc_data[2])).strftime('%Y-%m-%d')
                elif calc_data[1] == 'week':
                    return (base_date + timedelta(weeks=calc_data[2])).strftime('%Y-%m-%d')
                elif calc_data[1] == 'month':
                    return (base_date + relativedelta(months=calc_data[2])).strftime('%Y-%m-%d')
                elif calc_data[1] == 'year':
                    return (base_date + relativedelta(years=calc_data[2])).strftime('%Y-%m-%d')
                else:
                    return ''
            else:
                return ''
        except Exception as e:
            msg = 'DatetimeHandle exception occured in calc_date(). Message: %s' % str(e)
            raise DatetimeHandleError(msg)

    # ======================================
    # convert_timezone
    # 주어진 datetime 문자열을 옵션에 따라 변환하여 문자열로 리턴
    # result = convert_timezone('datetime', from_zone='US/Eastern', to_zone='Asia/Seoul', format='%Y-%m-%d %H:%M:%S')
    # [참고]
    #   - from_zone을 기준으로 주어진 datetime을 계산한다.
    #   - from_zone이 없을 경우 UTC를 기준으로 한다.
    #   - to_zone이 없을 경우 Asia/Seoul을 기준으로 한다.
    #   - format이 없을 경우 '%Y-%m-%d %H:%M:%S'을 기준으로 한다.
    # ======================================
    @staticmethod
    def convert_timezone(datetime_string, **kwargs):
        try:
            from_zone = 'UTC'
            to_zone = 'Asia/Seoul'
            format = '%Y-%m-%d %H:%M:%S'
            for i, j in kwargs.items():
                if i == 'from_zone':
                    from_zone = j
                if i == 'to_zone':
                    to_zone = j
                if i == 'format':
                    format = j
            from_datetime = pytz.timezone(from_zone).localize(parse(datetime_string))
            to_datetime = from_datetime.astimezone(pytz.timezone(to_zone))
            return to_datetime.strftime(format)
        except Exception as e:
            msg = 'DatetimeHandle exception occured in convert_timezone(). Message: %s' % str(e)
            raise DatetimeHandleError(msg)

    # ======================================
    # convert_datetime
    # 주어진 문자열을 datetime 값으로 리턴
    # result = convert_datetime(value, style='EN', format='')
    # [참고]
    #
    # ======================================
    @staticmethod
    def convert_datetime(value, **kwargs):
        try:
            result = ''
            style = kwargs.get('style', 'EN')
            format = kwargs.get('format', '%Y-%m-%d')
            # ~일전 또는 ~ago로 표현되는 날짜가 들어올 경우
            if 'ago' in value or 'yesterday' in value or '전' in value or '어제' in value:
                if 'minute' in value or 'minutes' in value or '분' in value:
                    result = date.today().strftime(format)
                elif 'hour' in value or 'hours' in value or '시간' in value:
                    result = date.today().strftime(format)
                elif 'yesterday' in value or '어제' in value:
                    result = (date.today() - timedelta(days=1)).strftime(format)
                elif 'day' in value or 'days' in value or '일' in value:
                    count = sh.convert_number(value, style=style)
                    result = (date.today() - timedelta(days=count)).strftime(format)
                elif 'week' in value or 'weeks' in value or '주' in value:
                    count = sh.convert_number(value, style=style)
                    result = (date.today() - timedelta(weeks=count)).strftime(format)
                elif 'month' in value or 'months' in value or '월' in value:
                    count = sh.convert_number(value, style=style)
                    result = (date.today() - relativedelta(months=count)).strftime(format)
                elif 'year' in value or 'years' in value or '년' in value:
                    count = sh.convert_number(value, style=style)
                    result = (date.today() - relativedelta(years=count)).strftime(format)
            else:
                if len(value) == 0:
                    result = ''
                elif style == 'KO':
                    if '년' in value or '월' in value or '일' in value:
                        result = value.replace('년', '-').replace('월', '-').replace('일', '')
                        result = parse(re.sub('[^0-9-.]', '', result)).strftime(format)
                    else:
                        result = parse(re.sub('[^0-9-.]', '', value)).strftime(format)
                elif style == 'EN':
                    month = ''
                    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    for i in months:
                        if i in value:
                            month = i
                            break
                    result = re.sub('[^0-9,./]', '', value)
                    result = month + ' ' + result
                    result = parse(result).strftime(format)
            return result
        except Exception as e:
            msg = 'DatetimeHandle exception occured in convert_datetime(). Message: %s' % str(e)
            raise DatetimeHandleError(msg)
