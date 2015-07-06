#! /usr/bin/python

# Sven Koppany for Swisscom

import requests # REST library
import subprocess 
import platform
import sys
import socket
import timeit # a simple wall-clocktime timer
from IPy import IP # used to validate IP addresses
from datetime import datetime

# Note: I had to look up how to do Python singletons. For that, I patterned this after
# an example provided by Alex Martelli. The idea here is that objects created
# from the Singleton class, albeit separate objects, share the same state from the
# SharedState class. Although this allows for the creation of multiple objects, the 
# shared state concept implements the core programmatic reason for using singleton
# objects, and I personally like the simplicity of this interpretation. 

class SharedState:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state

class helloHeidi(SharedState):
    def __init__(self, 
                    ipURL='http://getmyip.nova.scapp.io/', 
                    postURL='https://zapier.com/hooks/catch/bag1y1/'):

        # Get the shared state
        SharedState.__init__(self)

        # Gather the IP info into local vars
        self.globalIP = self.getGlobalIP(ipURL)
        self.localIP = self.getLocalIP()

        # POST the IP addresses and the current time, getting the HTTP status code
        self.postStatus = self.postIPInfo(postURL)

    # This is a simple check to see if the strings that are
    # being returned are valid IP addresses. This method uses
    # the IPy library and assumes that exceptions represent bad addys.

    def __validateIP(self, ipv4):
        """Validate IP address and return a four octet normalized string.
                -9 : invalid IP address """
        try:
            return IP(ipv4).strNormal()
        except:
            return -9 

    # Instructions: Call the JSON-API http://getmyip.nova.scapp.io/ to get your current public IP
    def getGlobalIP(self, url):
        """Get a list of valid global IPs from http://getmyip.nova.scapp.io/, or
                -1 : failure
                -2 : non-200 from the HTTP get
                -3 : requests exception 
                -9 : invalid address (from __validateIP) """

        # set an initial val in case everything fails
        ip = [-1]

        try:
            r = requests.get(url)
            if r.status_code == 200:
                ip = r.json()['ip'].split(',') #sometimes a comma-delimited list is returned
                ip = [g.strip() for g in ip] #trim the whitespace
                ip = [self.__validateIP(g) for g in ip] #validate each IP

            else: #if the status code is not 200
                ip = [-2]

        except: #more detailed exception handling could be added
            ip = [-3]

        return ip

    # Instructions: Call a local system-command (i.e. ifconfig) and get your current local IP (eth0) 
    def getLocalIP(self):
        """Get a list of valid local IPs (in this case, one), or
                -1 : general failure
                -9 : invalid address (from __validateIP)
                     assume the system process returned something weird """

        # set an initial val in case everything fails
        ip = [-1]

        # This should work on OSX and linux with ifconfig installed.
        # I am making assumptions here for devices
        # This is probably not the best way to get a local IP, tho
        if platform.system() == "Darwin": #osx
            device = "en0"
        else: #linux (please don't try this on Windows)
            device = "eth0"

        getArchLocalIP = "ifconfig " + device + \
                            " | grep -E \'inet\s\' \
                            | awk \'{ print $2 }\'"

        # Run the os command and hope for the best
        procIP = subprocess.check_output(getArchLocalIP, shell=True, stderr=subprocess.STDOUT).strip().decode("utf-8")

        # Assign to IP if the address looks valid, we should get '-9' for non-IPs
        ip = [self.__validateIP(procIP)]

        return ip

    # Instructions: A POST-CALL to https://zapier.com/hooks/catch/bag1y1/ having a body with this format;
    #       {
    #       "globalip": "8.8.8.8", 
    #       "localip": "8.8.8.8", 
    #       "localtime": "4:26pm"
    #       }
    def postIPInfo(self, url):
        """ POST the data to zapier.com """

        payload = {'globalip': self.globalIP,
                    'localip': self.localIP,
                    'localtime': datetime.now().strftime('%I:%M%p')}
        r = requests.post(url, data=payload)
        return r.status_code


if __name__ == "__main__":

    # Instructions: Measure the time needed for the process to run through and 
    #       current memory size of the singleton object at the end of the call 
    #       and print it out to the console

    # Time the creation of the heidi object
    tic = timeit.default_timer()
    heidi = helloHeidi()
    toc = timeit.default_timer()

    # Print out the requested info to console
    print("Creating a helloHeidi instance --> heidi")
    print("\nHeidi is %d bytes" % sys.getsizeof(heidi))
    print("Her init routines took %f seconds to execute" % (toc - tic))

    print("Heidi's global IP is %s and her local IP is %s" % (heidi.globalIP, heidi.localIP))
    print("Her POST returned with a status code %d" % heidi.postStatus)

    # Also, test out the singleton pattern as indicated above
    # A second instance should have a separate address in memory, but any change
    # to the variables of one should be reflected across all instances

    # UNCOMMENT EVERYTHING BELOW THIS LINE TO TEST THE SINGLETON

    # print("\n------------\nTesting the singleton\n-------------")
    # print("Creating a second helloHeidi object --> heidi2")
    # heidi2 = helloHeidi()

    # print("Heidi is at %s and Heidi2 is at %s" % (hex(id(heidi)), hex(id(heidi2))))
    # print("\nThey should be separate instance objects, but the state should be the same.")
    # print("\nA value change in one should reflect the other.")

    # # Show the initial globalIP vars for both
    # print("Initial GlobalIP:\n\tHeidi: %s\n\tHeidi2: %s" % (heidi.globalIP, heidi2.globalIP))
    # print("\nNow if we change Heidi's globalIP val, Heidi2 should reflect that change")
    
    # # Change a var in one instance
    # heidi.globalIP = "1.2.3.4"

    # # Show the globalIP vars again
    # print("Initial GlobalIP:\n\tHeidi: %s\n\tHeidi2: %s" % (heidi.globalIP, heidi2.globalIP))
    # print("\nIf the addresses are the same, then helloHeidi objects are behaving as a singleton")

    

	