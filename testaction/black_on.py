class black_on(object):
    def __init__(self):
        self.name = 'black_on'
        print("init black_on")

    def transfer(self, status):
    	status['black'] = 'on'
    	if status['app'] == 'on':
    		status['app'] = 'off'
    	return status

