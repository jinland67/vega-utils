import re

class StringHandleError(Exception):
        #------------------------------------------------
    # 생성할 때 value 값을 입력 받은다.
    # -----------------------------------------------
    def __init__(self, value):
        self.value = value

    #------------------------------------------------
    # 생성할 때 받은 value 값을 확인 한다.
    # -----------------------------------------------
    def __str__(self):
        return self.value

class StringHandle:
    # ======================================
    # 문자열 중에서 숫자만 찾아내서 리스트로 리턴
    # ======================================
    @staticmethod
    def find_number(string):
        try:
            return re.findall('\d+', string)
        except Exception as e:
            msg = 'StringHandle exception occured in find_number(). Message: %s' % str(e)
            raise StringHandleError(msg)

    # ======================================
    # 문자열 중에서 이모티콘을 제거
    # ======================================
    @staticmethod
    def emoji(string):
        try:
            EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
            return  EMOJI.sub(r'', string)
        except Exception as e:
            msg = 'StringHandle exception occured in emoji(). Message: %s' % str(e)
            raise StringHandleError(msg)

    # -----------------------------------------------
    # 단위가 표시된 문자열을 숫자로 변경
    # convert_number('10.4M', style='EN')
    # convert_number('10.5백만, style='KO')
    # -----------------------------------------------
    @staticmethod
    def convert_number(value, **kwargs):
        try:
            result = ''
            style = kwargs.get('style', 'EN')
            en_units = ['K', 'M', 'B', 'T']
            ko_units = ['백', '천', '만', '억']
            if style == 'KO':
                result = re.sub('[^0-9.,백천만억]', '', value)
                if '.' in result:
                    dp_size = len(re.sub('[^0-9]', '', result.split('.')[1]))
                    for seq in value:
                        if seq in ko_units:
                            if seq == '백':
                                result = result.replace('백', '') + '00'
                            if seq == '천':
                                result = result.replace('천', '') + '000'
                            if seq == '만':
                                result = result.replace('만', '') + '0000'
                            if seq == '억':
                                result = result.replace('억', '') + '00000000'
                    result = re.sub('[^0-9]', '', result[:(0 - dp_size)])
                else:
                    if len(result) == 0:
                        result = '0'
                    if '백' in result:
                        result = result.replace('백', '') + '00'
                    if '천' in result:
                        result = result.replace('천', '') + '000'
                    if '만' in result:
                        result = result.replace('만', '') + '0000'
                    if '억' in result:
                        result = result.replace('억', '') + '00000000'
                    result = re.sub('[^0-9]', '', result)
            if style == 'EN':
                result = re.sub('[^0-9.,KMBT]', '', value)
                if '.' in result:
                    dp_size = len(re.sub('[^0-9]', '', result.split('.')[1]))
                    for seq in value:
                        if seq in en_units:
                            if seq == 'K':
                                result = result.replace('K', '') + '000'
                            if seq == 'M':
                                result = result.replace('M', '') + '000000'
                            if seq == 'B':
                                result = result.replace('B', '') + '000000000'
                            if seq == 'T':
                                result = result.replace('T', '') + '000000000000'
                    result = re.sub('[^0-9]', '', result[:(0 - dp_size)])
                else:
                    if len(result) == 0:
                        result = '0'
                    elif 'K' in result:
                        result = result.replace('K', '') + '000'
                    elif 'M' in result:
                        result = result.replace('M', '') + '000000'
                    elif 'B' in result:
                        result = result.replace('B', '') + '000000000'
                    elif 'T' in result:
                        result = result.replace('T', '') + '000000000000'
                    else:
                        result = re.sub('[^0-9]', '', result)
            return int(result)
        except Exception as e:
            msg = 'StringHandle exception occured in convert_number(). value: %s Message: %s' % (result, str(e))
            raise StringHandleError(msg)
