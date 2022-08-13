def re_temp(field):
	'''T0:200 /200 T1:47 /0 B:49 /50'''

	return field + ':([0-9].*?) '


def re_temp_target(field):
	'''T0:200 /200 T1:47 /0 B:49 /50'''

	return field + ':[0-9].*? \/([0-9].*?)[ \\r\\n]'


def re_pos(field):
	'''X:147.993 Y:74.9949 Z:150 A:0 B:0'''

	return field + ':(.+?)[ \\r\\n]'


def re_field(field):
    '''Machine Type: T-REX'''

    return field + ': ?(.+?)\\r\\n'


def re_pro():
	'''SD printing byte 12738825/12738824'''

	return '([0-9].*)\/([0-9].*?)\\r'