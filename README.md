# vega_utils
각종 라이브러리

    * 의존성:
        - python 3.8.10 이상
        - slack-sdk 3.11.2 이상
        - pytz 2021.3 이상
        - python-dateutil 2.8.2 이상
        - psutil 5.8.0 이상
------------------
### 사용법
```
    # install
        $  pip install git+https://github.com/jinland67/vega-utils.git

    # file logger 사용 시
        from vega_utils.logger import FileLogger, FileLoggerError, LogLevel
                :
                :
        log = FileLogger(
            log_path="./log/",
            log_file="test.log",
            log_level = LogLevel.DEBUG,
            log_compress=True
        )
                :
        # log 생성
        log.debug('this is a test log. time[%s]', time.time())
                :
    # socket logger 사용 시
        from vega_utils.logger import SocketLogger, SocketLoggerError, LogLevel
                :
                :
        log = SocketLogger(
            log_host="localhost",
            log_port=5000,
            log_level = LogLevel.DEBUG
            service_name='stree'
        )
                :
        # log 생성
        log.debug('this is a test log. time[%s]', time.time())

    # ProcessHandle 사용 시
        from vega_utils.process import ProcessHandle as ph
                :
                :
        result = ph.pids()

    # NetworkHandle 사용 시
        from vega_utils.network import NetworkHandle as nh
                :
                :
        result = nh.is_url()

    # StringHandle 사용 시
        from vega_utils.string import StringHandle as sh
                :
                :
        result = sh.emoji(value)

    # DateHandle 사용 시
        from vega_utils.datetime import DateHandle as dh
                :
                :
        result = dh.now()

    # Slack를 통한 메시지 전송 시
        from vega_utils.slack import Slack as slack
                :
                :
        slack.send('slac webhook url', blocks)
        [참고]
        blocks에 보내고자 하는 메시지 형식을 담아 전송. 형식은 slack 홈페이지 참조
```