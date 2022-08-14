import re
import logging

try:
    from .patterns import re_field, re_pos, re_pro, re_temp, re_temp_target

    from .call_handler import recieve

    from .const import TEMPS, INFOS, STATUS, AXIS, PROGRESS
    from .const import REQUEST_INFO, REQUEST_POSITION, REQUEST_PROGRESS, REQUEST_STATUS, REQUEST_TEMPERATURE
    from .const import CHANGE_TEMPERATURE
    from .const import UNAVAILABLE
except ImportError:
    from patterns import re_field, re_pos, re_pro, re_temp, re_temp_target

    from call_handler import recieve

    from const import TEMPS, INFOS, STATUS, AXIS, PROGRESS
    from const import REQUEST_INFO, REQUEST_POSITION, REQUEST_PROGRESS, REQUEST_STATUS, REQUEST_TEMPERATURE
    from const import CHANGE_TEMPERATURE
    from const import UNAVAILABLE


_LOGGER = logging.getLogger(__name__)

def get_info(addr):
    '''returns basic printer information'''

    data = recieve(addr, REQUEST_INFO)
    printer_info = {}
    
    for field in INFOS:
        try:
            re_string = re_field(field)
            printer_info[field] = re.search(re_string, data).groups()[0]
        except:  
            # TODO add Logger entry
            printer_info[field] = UNAVAILABLE

    return printer_info


def get_head(addr):
    '''returns the position of the printer head'''

    data = recieve(addr, REQUEST_POSITION)
    head_pos = {}
    
    for field in AXIS:
        try:
            re_string = re_pos(field)
            head_pos[field] = re.search(re_string, data).groups()[0]
        except:  
            # TODO add Logger entry
            head_pos[field] = UNAVAILABLE

    return head_pos


def get_temp(addr):
    ''' returns the actual temps and goal temps'''

    data = recieve(addr, REQUEST_TEMPERATURE)
    actual = {}
    target = {}

    for field in TEMPS:
        re_temper = re_temp(field)
        re_target = re_temp_target(field)
        try:
            actual[field] = re.search(re_temper, data).groups()[0]
        except:
            actual[field] = UNAVAILABLE

        try:
            target[field] = re.search(re_target, data).groups()[0]
        except:
            target[field] = UNAVAILABLE

    temps = {}
    for key in TEMPS:
        temps[key + '_actual'] = actual[key]
        temps[key + '_target'] = target[key]

    return temps


def get_progress(addr):
    '''returns the progress of current print'''

    data = recieve(addr, REQUEST_PROGRESS)
    re_string = re_pro()

    try:
        re_groups = re.search(re_string, data).groups()
        finished = re_groups[0]
        total = re_groups[1]

        percentage = 0 if total == '0' else int((int(finished) / int(total)) * 10000) / 100

        return {PROGRESS[0]: int(finished),
                PROGRESS[1]: int(total),
                PROGRESS[2]: percentage}

    except:
        return {PROGRESS[0]: UNAVAILABLE,
                PROGRESS[1]: UNAVAILABLE,
                PROGRESS[2]: UNAVAILABLE}


def get_status(addr):
    '''returns the current status of printer'''

    data = recieve(addr, REQUEST_STATUS)
    infos = {}

    for field in STATUS:
        try:
            re_string = re_field(field)
            infos[field] = re.search(re_string, data).groups()[0]
        except:
            infos[field] = UNAVAILABLE

    return infos



