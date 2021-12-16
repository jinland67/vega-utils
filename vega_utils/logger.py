import time
import socket
import zipfile
import os.path
from enum import Enum
from datetime import date, datetime, timedelta
from inspect import getframeinfo, stack

# ----------------------------------------------------
# Logger
# ----------------------------------------------------
#	- FileLogger(options)
#		. log_path='logfile이 저장될 dir_name'
#		. log_file='logfile name'
#		- log_level='저장할 log level'
#		- log_compress='True or False'
#	- SocketLogger(options)
#		. log_level='저장할 log level'
#		. service_name='서비스명'	--> vlogd에는 여러 process의 log가 저장되므로 tail -f | grep 'service_name'으로 처리하기 위한 값
# ----------------------------------------------------
# Logger 사용법
#   - import FileLogger
#   - log = FileLogger(options)
#   - log.trace('write log message')
# ----------------------------------------------------
# ----------------------------------------------------
# [log 종류]
# ----------------------------------------------------
# 	log.trace('log_message')
# 	log.debug('log_message')
# 	log.info('log_message')
# 	log.warning('log_message')
# 	log.error('log_message')
# 	log.fatal('log_message')
#
# ----------------------------------------------------
# [로그레벨]
# from logger import LogLevel
# 	TRACE, DEBUG, INFO, WARN, ERROR, FATAL
# ----------------------------------------------------
class LogLevel(Enum):
    TRACE = 0
    DEBUG = 1
    INFO  = 2
    WARN  = 3
    ERROR = 4
    FATAL = 5

class FileLoggerError(Exception):
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

class SocketLoggerError(Exception):
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


# ----------------------------------------------
# Class FileLogger
# log = FileLogger(log_path='파일경로', log_file='파일명', err_file='오류로그 파일명', log_level='DEBUG', log_compress=True)
# [기본값]
#       log_path = 현재경로
#       log_file = 'app.log'
#       err_file = 'error.log'
#       log_level = 'INFO'
#       log_compress = True
# ----------------------------------------------
class FileLogger:
    def __init__(self, **kwargs):
        self.__log_path = '.'
        self.__log_file = 'app.log'
        self.__err_file = 'error.log'
        self.__logging = LogLevel
        self.__log_level = self.__logging.INFO.value
        self.__log_compress = True

        for i, j in kwargs.items():
            if i == 'log_path':
                self.__log_path = j
            if i == 'log_file':
                self.__log_file = j
            if i == 'log_level':
                if j == 'TRACE':
                    self.__log_level = self.__logging.TRACE.value
                if j == 'DEBUG':
                    self.__log_level = self.__logging.DEBUG.value
                if j == 'INFO':
                    self.__log_level = self.__logging.INFO.value
                if j == 'WARN':
                    self.__log_level = self.__logging.WARN.value
                if j == 'ERROR':
                    self.__log_level = self.__logging.ERROR.value
                if j == 'FATAL':
                    self.__log_level = self.__logging.FATAL.value
            if i == 'err_file':
                self.__err_file = j
            if i == 'log_compress':
                self.__log_compress = j

    # -----------------------------------------------
    # 현재 로그파일이 오늘 생성된 파일인지 아니면 어제 날짜로 생성된 파일인지 체크
    # -----------------------------------------------
    def __check_compress(self):
        try:
            # 로그파일을 일자별로 관리하기 위한 작업
            today = date.today().isoformat()
            modify_time = os.path.getmtime(self.__log_path + '/' + self.__log_file)
            modify_time = time.strftime('%Y-%m-%d', time.localtime(modify_time))
            yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
            if today != modify_time:
                zip = zipfile.ZipFile(self.__log_path + '/' + self.__log_file + '-' + yesterday + '.zip', 'w')
                zip.write(self.__log_path + '/' + self.__log_file, compress_type=zipfile.ZIP_DEFLATED)
                zip.close()
                with open(self.__log_path + '/' + self.__log_file, 'r+') as f:
                    f.truncate(0)
        except Exception as e:
            msg = 'FileLogger exception occured in check_compress(). Message: %s' % str(e)
            raise FileLoggerError(msg)

    # -----------------------------------------------
    # 로그의 내용을 파일에 저장
    # -----------------------------------------------
    def __write(self, data):
        try:
            if os.path.exists(self.__log_path + '/' + self.__log_file):
                file_mode = 'a'
                if self.__log_compress:
                    self.__check_compress()
            else:
                file_mode = 'w'
            with open(self.__log_path + '/' + self.__log_file, file_mode, encoding='utf8') as f:
                f.write(data)
                f.write('\n')
        except Exception as e:
            msg = 'FileLogger exception occured in write(). Message: %s' % str(e)
            raise FileLoggerError(msg)

    # -----------------------------------------------
    # ERROR 또는 FATAL 오류의 경우 
    # -----------------------------------------------
    def __write_error(self, data):
        try:
            if os.path.exists(self.__log_path + '/' + self.__err_file):
                file_mode = 'a'
                if self.__log_compress:
                    self.__check_compress()
            else:
                file_mode = 'w'
            with open(self.__log_path + '/' + self.__err_file, file_mode, encoding='utf8') as f:
                f.write(data)
                f.write('\n')
        except Exception as e:
            msg = 'FileLogger exception occured in write_error(). Message: %s' % str(e)
            raise FileLoggerError(msg)

    # -----------------------------------------------
    # 로그의 헤더 포맷을 구성한다.
    # -----------------------------------------------
    def __make_header(self):
        try:
            today = datetime.now()
            caller = getframeinfo(stack()[2][0])
            result  = today.strftime('%Y-%m-%d %H:%M:%S') + ':'
            result += caller.filename + '(' + str(caller.lineno) + '):'
            return result
        except Exception as e:
            msg = 'FileLogger exception occured in make_header(). Message: %s' % str(e)
            raise FileLoggerError(msg)

    # -----------------------------------------------
    # 로그 파일의 형식을 구성한다.
    # -----------------------------------------------
    def __make_format(self, *message):
        try:
            format = ''
            data = ()
            # sprintf 형태의 표현 만들기
            index = 0
            for i in message[0]:		# tuple로 받은 인자를 다시 tuple로 전달 받았을 때 처리 방법.
                if index == 0:
                    format = i
                else:
                    data = data + (i,)
                index += 1
            if len(message[0]) == 1:
                result = format
            else:
                result = format % data
            return result
        except Exception as e:
            msg = 'FileLogger exception occured in make_format(). Message: %s' % str(e)
            raise FileLoggerError(msg)

    # -----------------------------------------------
    # 로그 생성 레벨을 변경하고자 할 때
    # -----------------------------------------------
    def set_level(self, log_level):
        try:
            if log_level == 'TRACE':
                self.__log_level = self.__logging.TRACE.value
            if log_level == 'DEBUG':
                self.__log_level = self.__logging.DEBUG.value
            if log_level == 'INFO':
                self.__log_level = self.__logging.INFO.value
            if log_level == 'WARN':
                self.__log_level = self.__logging.WARN.value
            if log_level == 'ERROR':
                self.__log_level = self.__logging.ERROR.value
            if log_level == 'FATAL':
                self.__log_level = self.__logging.FATAL.value
        except Exception as e:
            msg = 'FileLogger exception occured in set_level(). Message: %s' % str(e)
            raise FileLoggerError(msg)

    # -----------------------------------------------
    # TRACE 레벨의 로그를 요청
    # -----------------------------------------------
    def trace(self, *message):
        try:
            if self.__log_level <= self.__logging.TRACE.value:
                result  = self.__make_header()
                result += "TRACE: >> "
                result += self.__make_format(message)
                self.__write(result)
        except Exception as e:
            msg = 'FileLogger exception occured in trace(). Message: %s' % str(e)
            raise FileLoggerError(msg)

    # -----------------------------------------------
    # DEBUG 레벨의 로그를 요청
    # -----------------------------------------------
    def debug(self, *message):
        try:
            if self.__log_level <= self.__logging.DEBUG.value:
                result  = self.__make_header()
                result += "DEBUG: >> "
                result += self.__make_format(message)
                self.__write(result)
        except Exception as e:
            msg = 'FileLogger exception occured in debug(). Message: %s' % str(e)
            raise FileLoggerError(msg)

    # -----------------------------------------------
    # INFO 레벨의 로그를 요청
    # -----------------------------------------------
    def info(self, *message):
        try:
            if self.__log_level <= self.__logging.INFO.value:
                result  = self.__make_header()
                result += "INFO : >> "
                result += self.__make_format(message)
                self.__write(result)
        except Exception as e:
            msg = 'FileLogger exception occured in info(). Message: %s' % str(e)
            raise FileLoggerError(msg)

    # -----------------------------------------------
    # WARN 레벨의 로그를 요청
    # -----------------------------------------------
    def warn(self, *message):
        try:
            if self.__log_level <= self.__logging.WARN.value:
                result  = self.__make_header()
                result += "WARN : >> "
                result += self.__make_format(message)
                self.__write(result)
                self.__write_error(result)
        except Exception as e:
            msg = 'FileLogger exception occured in warn(). Message: %s' % str(e)
            raise FileLoggerError(msg)

    # -----------------------------------------------
    # ERROR 레벨의 로그를 요청
    # -----------------------------------------------
    def error(self, *message):
        try:
            if self.__log_level <= self.__logging.ERROR.value:
                result  = self.__make_header()
                result += "ERROR: >> "
                result += self.__make_format(message)
                self.__write(result)
                self.__write_error(result)
        except Exception as e:
            msg = 'FileLogger exception occured in error(). Message: %s' % str(e)
            raise FileLoggerError(msg)

    # -----------------------------------------------
    # FATAL 레벨의 로그를 요청
    # -----------------------------------------------
    def fatal(self, *message):
        try:
            if self.__log_level <= self.__logging.FATAL.value:
                result  = self.__make_header()
                result += "FATAL: >> "
                result += self.__make_format(message)
                self.__write(result)
                self.__write_error(result)
        except Exception as e:
            msg = 'FileLogger exception occured in fatal(). Message: %s' % str(e)
            raise FileLoggerError(msg)


# ----------------------------------------------
# Class SocketLogger
# log = SocketLogger(log_level='DEBUG', service_name='xxxx')
# [설명]
#       log_level = 'INFO'
#       service_name = 'socketlog를 생성한 프로젝트명'
# ----------------------------------------------
class SocketLogger:
    def __init__(self, **kwargs):
        self.__EOF = 'VEGA_LOG_END'
        self.__HOST = '127.0.0.1'
        self.__PORT = 5000
        self.__logging = LogLevel
        self.__log_level = self.__logging.INFO.value
        self.__service_name = '[UNDEFINED]'
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((self.__HOST, self.__PORT))

        for i, j in kwargs.items():
            if i == 'log_level':
                if j == 'TRACE':
                    self.__log_level = self.__logging.TRACE.value
                if j == 'DEBUG':
                    self.__log_level = self.__logging.DEBUG.value
                if j == 'INFO':
                    self.__log_level = self.__logging.INFO.value
                if j == 'WARN':
                    self.__log_level = self.__logging.WARN.value
                if j == 'ERROR':
                    self.__log_level = self.__logging.ERROR.value
                if j == 'FATAL':
                    self.__log_level = self.__logging.FATAL.value
            if i == 'service_name':
                self.__service_name = j

    # -----------------------------------------------
    # 로그를 log daemon으로 전송
    # -----------------------------------------------
    def __send(self, data):
        try:
            data = data + self.__EOF
            self.__client.send(data.encode())
        except Exception as e:
            msg = 'SocketLogger exception occured in send(). Message: %s' % str(e)
            raise SocketLoggerError(msg)

    # -----------------------------------------------
    # 로그 메시지의 헤더를 구성
    # -----------------------------------------------
    def __make_header(self):
        try:
            today = datetime.now()
            caller = getframeinfo(stack()[2][0])
            result  = today.strftime('%Y-%m-%d %H:%M:%S') + ':'
            result += self.__service_name + ':'
            result += caller.filename + '(' + str(caller.lineno) + '):'
            return result
        except Exception as e:
            msg = 'SocketLogger exception occured in make_header(). Message: %s' % str(e)
            raise SocketLoggerError(msg)

    # -----------------------------------------------
    # 로그 메시지의 형식을 구성
    # -----------------------------------------------
    def __make_format(self, *message):
        try:
            format = ''
            data = ()
            # sprintf 형태의 표현 만들기
            index = 0
            for i in message[0]:		# tuple로 받은 인자를 다시 tuple로 전달 받았을 때 처리 방법.
                if index == 0:
                    format = i
                else:
                    data = data + (i,)
                index += 1
            if len(message[0]) == 1:
                result = format
            else:
                result = format % data
            return result
        except Exception as e:
            msg = 'SocketLogger exception occured in make_format(). Message: %s' % str(e)
            raise SocketLoggerError(msg)

    # -----------------------------------------------
    # 로그 daemon과의 connection을 종료
    # -----------------------------------------------
    def close(self):
        try:
            self.__client.close()
        except Exception as e:
            msg = 'SocketLogger exception occured in close(). Message: %s' % str(e)
            raise SocketLoggerError(msg)

    # -----------------------------------------------
    # 로그 생성 레벨 설정
    # -----------------------------------------------
    def set_level(self, log_level):
        try:
            if log_level == 'TRACE':
                self.__log_level = self.__logging.TRACE.value
            if log_level == 'DEBUG':
                self.__log_level = self.__logging.DEBUG.value
            if log_level == 'INFO':
                self.__log_level = self.__logging.INFO.value
            if log_level == 'WARN':
                self.__log_level = self.__logging.WARN.value
            if log_level == 'ERROR':
                self.__log_level = self.__logging.ERROR.value
            if log_level == 'FATAL':
                self.__log_level = self.__logging.FATAL.value
        except Exception as e:
            msg = 'SocketLogger exception occured in set_level(). Message: %s' % str(e)
            raise SocketLoggerError(msg)

    # -----------------------------------------------
    # TRACE 레벨의 로그를 전송
    # -----------------------------------------------
    def trace(self, *message):
        try:
            if self.__log_level <= self.__logging.TRACE.value:
                result  = self.__make_header()
                result += "TRACE: >> "
                result += self.__make_format(message)
                self.__send(result)
        except Exception as e:
            msg = 'SocketLogger exception occured in trace(). Message: %s' % str(e)
            raise SocketLoggerError(msg)

    # -----------------------------------------------
    # DEBUG 레벨의 로그를 전송
    # -----------------------------------------------
    def debug(self, *message):
        try:
            if self.__log_level <= self.__logging.DEBUG.value:
                result  = self.__make_header()
                result += "DEBUG: >> "
                result += self.__make_format(message)
                self.__send(result)
        except Exception as e:
            msg = 'SocketLogger exception occured in debug(). Message: %s' % str(e)
            raise SocketLoggerError(msg)

    # -----------------------------------------------
    # INFO 레벨의 로그를 전송
    # -----------------------------------------------
    def info(self, *message):
        try:
            if self.__log_level <= self.__logging.INFO.value:
                result  = self.__make_header()
                result += "INFO : >> "
                result += self.__make_format(message)
                self.__send(result)
        except Exception as e:
            msg = 'SocketLogger exception occured in info(). Message: %s' % str(e)
            raise SocketLoggerError(msg)

    # -----------------------------------------------
    # WARN 레벨의 로그를 전송
    # -----------------------------------------------
    def warn(self, *message):
        try:
            if self.__log_level <= self.__logging.WARN.value:
                result  = self.__make_header()
                result += "WARN : >> "
                result += self.__make_format(message)
                self.__send(result)
        except Exception as e:
            msg = 'SocketLogger exception occured in warn(). Message: %s' % str(e)
            raise SocketLoggerError(msg)

    # -----------------------------------------------
    # ERROR 레벨의 로그를 전송
    # -----------------------------------------------
    def error(self, *message):
        try:
            if self.__log_level <= self.__logging.ERROR.value:
                result  = self.__make_header()
                result += "ERROR: >> "
                result += self.__make_format(message)
                self.__send(result)
        except Exception as e:
            msg = 'SocketLogger exception occured in error(). Message: %s' % str(e)
            raise SocketLoggerError(msg)

    # -----------------------------------------------
    # FATAL 레벨의 로그를 전송
    # -----------------------------------------------
    def fatal(self, *message):
        try:
            if self.__log_level <= self.__logging.FATAL.value:
                result  = self.__make_header()
                result += "FATAL: >> "
                result += self.__make_format(message)
                self.__send(result)
        except Exception as e:
            msg = 'SocketLogger exception occured in fatal(). Message: %s' % str(e)
            raise SocketLoggerError(msg)
