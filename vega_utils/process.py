import psutil


class ProcessHandleError(Exception):
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


class ProcessHandle:
    # --------------------------------------
    # process의 동작여부를 체크
    # [주의]
    # 	- type이 name 일 경우
    #       value = {
    #           "exe": "python3.8",
    #           "file": "test.py" 
    #       }
    #       result = alive('name', value)
    #       return --> pid list
    #	- type이 pid일 경우
    #       result = alive('pid', pid)
    #       return --> True or False
    # --------------------------------------
    @staticmethod
    def alive(type, value):
        try:
            pids = []
            if type == 'name':
                for proc in psutil.process_iter():
                    try:
                        # Check if process name contains the given name string.
                        if value['file'] in proc.cmdline() and value['exe'] in proc.exe():
                            pids.append(proc.pid)
                            break
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
                return pids
            elif type == 'pid':
                return psutil.pid_exists(value)
        except Exception as e:
            msg = 'ProcessHandle exception occured in alive(). Message: %s' % str(e)
            raise ProcessHandleError(msg)        

    # --------------------------------------
    # process의 종료
    # [주의]
    # 	type이 name이면, value는 process name 즉 문자열
    #	type이 pid이면, value는 process id 즉 숫자
    # --------------------------------------
    @staticmethod
    def kill(pid):
        try:
            if psutil.pid_exists(pid):
                p = psutil.Process(pid)
                p.terminate()
        except Exception as e:
            msg = 'ProcessHandle exception occured in kill(). Message: %s' % str(e)
            raise ProcessHandleError(msg)

    # --------------------------------------
    # 현재 실행중인 pid를 정렬해서 리턴
    # return
    #	[
    #		{'name': 'systemd', 'pid': 1, 'username': 'root'},
    #		{'name': 'kthreadd', 'pid': 2, 'username': 'root'}
    #	]
    # --------------------------------------
    @staticmethod
    def pids():
        try:
            result = []
            for proc in psutil.process_iter(attrs=['pid', 'name', 'username']):
                result.append(proc.info)
            return result
        except Exception as e:
            msg = 'ProcessHandle exception occured in alive(). Message: %s' % str(e)
            raise ProcessHandleError(msg)

    # --------------------------------------
    # 현재 CPU 정보를 리턴
    # return:	{'count': 1, 'logical': 1, 'cpu_time': 1, 'idle_time': 1, 'speed': 1}
    # --------------------------------------
    @staticmethod
    def cpu():
        try:
            result = dict(count=0, logical=0, cpu_time=0, idle_time=0)
            result['speed'] = psutil.cpu_freq().current/1024
            result['count'] = psutil.cpu_count(logical=False)
            result['logical'] = psutil.cpu_count()
            cpu = psutil.cpu_times_percent()
            result['cpu_time'] = 100 - cpu.idle
            result['idle_time'] = cpu.idle
            return result
        except Exception as e:
            msg = 'ProcessHandle exception occured in cpu(). Message: %s' % str(e)
            raise ProcessHandleError(msg)

    # --------------------------------------
    # 현재 메모리 정보를 리턴
    # return:	{'total': 'systemd', 'avail': 1}
    # --------------------------------------
    @staticmethod
    def memory(unit):
        try:
            result = dict(total=0, avail=0)
            mem = psutil.virtual_memory()
            if unit == 'K':
                result['total'] = mem.total/1024
                result['avail'] = mem.available/1024
            elif unit == 'M':
                result['total'] = mem.total/1024**2
                result['avail'] = mem.available/1024**2
            elif unit == 'G':
                result['total'] = mem.total/1024**3
                result['avail'] = mem.available/1024**3
            return result
        except Exception as e:
            msg = 'ProcessHandle exception occured in memory(). Message: %s' % str(e)
            raise ProcessHandleError(msg)