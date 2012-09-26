import time, platform

get_time = time.time
if platform.system() == 'Windows':
    get_time = time.clock