import re



class NetworkHandleError(Exception):
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



class NetworkHandle:
    # ======================================
    # 주어진 숫자의 100만분의 1초
    # ======================================
    @staticmethod
    def is_url(value):
        try:
            p = re.compile("^(?:https?:\\/\\/)?(?:www\\.)?[a-zA-Z0-9./]+$")
            m = p.match(value)
            if m is None:
                return False
            return True
        except Exception as e:
            msg = 'NetworkHandleError exception occured in is_url(). Message: %s' % str(e)
            raise NetworkHandleError(msg)

