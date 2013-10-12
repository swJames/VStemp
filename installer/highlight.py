#!/usr/bin/env python

def highlight(string, status=''):
        attr = []
        if status == True:
                attr.append('32')
        elif status == False:
                attr.append('31')
	else:
		attr.append('36')
        attr.append('1')
        return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)
