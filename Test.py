from Action import *
from FSM import *
from Graph import *

def transfer_blackon(status):
	status['black'] = 'on'
	if status['app'] == 'on':
		status['app'] = 'off'
	return status
def transfer_blackoff(status):
	status['black'] = 'off'
	if status['app'] == 'off':
		status['app'] = 'on'
	return status

def transfer_appin(status):
	if status['black'] != 'on':
		status['app'] = 'on'
	return status

def transfer_appon(status):
	if status['app'] != 'na' and status['black']!='on':
		status['app'] = 'on'
	return status
	
def transfer_appoff(status):
	if status['app'] != 'na':
		status['app'] = 'off'
	return status

if __name__ == '__main__':
	fsm = FSM()
	action1 = Action()
	action1.transfer = transfer_blackon 
	action1.name = 'black_on'

	action2 = Action()
	action2.transfer = transfer_blackoff
	action2.name = 'black_off'

	action3 = Action()
	action3.transfer = transfer_appin
	action3.name = 'app_in'

	action4 = Action()
	action4.transfer = transfer_appon
	action4.name = 'app_on'
	
	action5 = Action()
	action5.transfer = transfer_appoff
	action5.name = 'app_off'

	fsm.startstates = [{'app':'na', 'black':'na'}]
	fsm.actionset = [action1, action2,action3,action4,action5]
	fsm.explore()

#	for edge in fsm.pathset:
#		print(str(edge))



