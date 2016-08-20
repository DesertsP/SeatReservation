import requests
import re


class YsuWireless(object):
    def __init__(self, user, pwd):
        self.data = {"DDDDD": user, "upass": pwd, "0MKKey": ''}
        self.URL = "http://202.206.240.243/"
        self.s = requests.session()

    def connect(self):
        try:
            res = self.s.post(url=self.URL, data=self.data)
        except Exception, e:
            print e
            return -1
        if re.findall("<S.+\S", res.text):
            return 1
        else:
            return 0

    def flux(self):
        res = self.s.get(url=self.URL)
        usedFlux = re.findall("flow='(\d+)", res.text)[0]
        usedFlux = float(usedFlux) / (1024.0 * 1024.0)
        flux = 4.0 - usedFlux
        return "%.2f GB" % flux
