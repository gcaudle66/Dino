class Ap:
    def __init__(self,apname, ethmac):
        self.apname = apname
        self.ethmac = ethmac

    def configure(self, *args, **kwargs):
        """
        Config in this Method defines the current state of AP config.
        """
        self.pri_cntr = ""
        self.sec_cntr = ""
        self.ip4_add = ""
        self.dnac_managed = False
        self.dnac_ip4_add = "unset"
    def tag_mapping(self):
        self.tag_RF = ""
        self.tag_Site = ""
        self.tag_Policy
    def status_flags(self, *args, **kwargs):
        self.flag_isAlive = False
        self.flag_isRegistered = False
        self.flag_isModified = False
        self.flag_setReboot = False
        self.flag_setDefault = False
        self.flag_ackModified = False
