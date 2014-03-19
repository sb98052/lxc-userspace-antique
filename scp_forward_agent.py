#!/usr/bin/python

# Run this script as:
# scp -S scp_forward_agent.py user@node

import sys
import os

new_args = []
fixed = False
for arg in sys.argv[1:]:
	if ('-oForwardAgent=no'==arg):
		arg = '-oForwardAgent=yes'
		fixed = True
	new_args.append(arg)

if (not fixed):
	new_args = ['-oForwardAgent=yes'] + new_args

os.execv('/usr/bin/ssh',['/usr/bin/ssh']+new_args)
