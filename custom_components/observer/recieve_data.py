import logging

try:
    from .encodedata import get_head, get_info, get_progress, get_status, get_temp

    from .const import MAX_RETRYS
    from .const import TEMPS_LONG, INFOS, STATUS, AXIS, PROGRESS
    from .const import UNAVAILABLE
except ImportError:
    from encodedata import get_head, get_info, get_progress, get_status, get_temp

    from const import MAX_RETRYS
    from const import TEMPS_LONG, INFOS, STATUS, AXIS, PROGRESS
    from const import UNAVAILABLE


_Logger = logging.getLogger(__name__)


async def retry(addr, fun_handle, keys):
    ''' function to try to collect the data MAX_RETRYS times and returns the collected data'''

    collect = {}
    for _ in range(MAX_RETRYS):
        try:
            data = await fun_handle(addr)
        except:
            continue

        for key in keys:
            if data[key] != UNAVAILABLE:
                collect[key] = data[key]

        if len(collect) == len(data):
            break

    for key in keys:
        if not key in collect.keys():
            collect[key] = UNAVAILABLE

    return collect


async def get_data(addr):
    '''collect data from printer and returns it formatted and collected'''

    head_dict = await retry(addr, get_head, AXIS)
    info_dict = await retry(addr, get_info, INFOS)
    status_dict = await retry(addr, get_status, STATUS)
    temp_dict = await retry(addr, get_temp, TEMPS_LONG)
    progress_dict = await retry(addr, get_progress, PROGRESS)

    if 'X' in INFOS:
        info_dict['X_status'] = 'X: ' + info_dict.pop('X')

    data_dict = {**status_dict, **head_dict, **info_dict, **temp_dict, **progress_dict}

    return data_dict


if __name__ == '__main__':
    
    #Testing
	addr = {'ip': '192.168.178.98',
		    'port': 8899}

	print(get_data(addr))

