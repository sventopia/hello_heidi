#! /usr/bin/python

import request
import resource

# Call the JSON-API http://getmyip.nova.scapp.io/ to get your current public IP 
# Call a local system-command (i.e. ifconfig) and get your current local IP (eth0) 
# Create a python singleton class / object and save the parameters in there 
# Create a method in the singleton which does:
# 	A POST-CALL to https://zapier.com/hooks/catch/bag1y1/ having a body with this format;
# 		{
# 		"globalip": "8.8.8.8", 
# 		"localip": "8.8.8.8", 
# 		"localtime": "4:26pm"
# 		}
# 	Measure the time needed for the process to run through and 
# 	current memory size of the singleton object at the end of the call 
# 	and print it out to the console