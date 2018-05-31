#!/usr/bin/env python2

import libMSRx05
import sys

if __name__=="__main__":
	port='/dev/tty.PL2303-00002014'
	show_debug=False

	while True:
		device=libMSRx05.x05(port)
		device.reset()
		device.setLED(7)

		if show_debug:
			print('Firmware Version:'+device.getFirmwareVersion())
			print('Device Model: '+device.getDeviceModel())
			coercivity='Low'
			if device.getCo():
				coercivity='High'
			print('Coercivity: '+coercivity)
			lz=device.getLZ()
			border=str(round(lz[0]*25.4/210,1))
			middle=str(round(lz[1]*25.4/75,1))
			print('[LeadingZeros] Track1&3: '+border+'mm, Track2: '+middle+'mm')

		valid=False
		while not valid:
			print('Enter Data to Write:')
			data=sys.stdin.readline().strip()
			valid=True
			for cc in data:
				if cc<'0' or cc>'9':
					valid=False
					print('Invalid character \''+cc+'\'.')
					break

		print('Erasing Tracks')
		print(device.eraseTracks([1,1,1]))

		print('Writing')
		while True:
			write=device.writeISO(['',';'+data+'?',''])
			if not write:
				print('  Error...try again...')
			else:
				print('  Success')
				break

		print('Reading')
		while True:
			read=device.readISO()
			if len(read)!=3:
				print('  Error...try again...')
			else:
				print('  '+str(read))
				break

		device.close()
