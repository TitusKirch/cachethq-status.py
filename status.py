import os
import urllib3

class Status:
    # init and pass protocol and address
    def __init__(self, protocol, address):
        self.protocol = protocol
        self.address = address

        # status codes
        # 0 => Unknown
        # 1 => Operational
        # 2 => Performance Issues
        # 3 => Partial Outage
        # 4 => Major Outage

        #setup default status
        self.status = 0
    
    # calls the appropriate get method using the protocol
    def get(self):
        # check protocol
        if self.protocol == "ping":
            self.status = self.ping()
        elif self.protocol == "http":
            self.status = self.http()
        
        # return status
        return self.status

    # ping protocol
    def ping(self):
        response = os.system("ping -c 1 " + self.address +" >/dev/null ")
        if response == 0:
            return 1
        else:
            return 4
    
    # http protocol
    def http(self):
        try:
            site_code = urllib3.PoolManager().request('GET', self.address).status
            if site_code == 200:
                return 1
            elif site_code == 503:
                return 3
            else:
                return 4
        except:
            return 4


