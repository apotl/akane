from enum import Enum

class BoardStatus(Enum):
	BOARD_OK = 0
	BOARD_EXISTS = -1
	BOARD_DOES_NOT_EXIST = -2
	BOARD_SETTING_UNCHANGED = -3

BooleanText = \
	{
		0: 'No',
		1: 'Yes'
	}
