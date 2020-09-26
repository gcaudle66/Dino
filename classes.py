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


class AcPo:
    """
    This class defines the access point and all of its glory...
    or at least all we are concerned about in this version of Dino
    """
    
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
        self.location = "default"
    def tag_mapping(self):
        self.tag_RF = ""
        self.tag_Site = ""
        self.tag_Policy = ""
    def status_flags(self, *args, **kwargs):
        """
        The below flags are various markers to set for
        different conditions based on events.
            ##flaf_isAlive(Bool) Indicates True if Dino is able to
            validate the AP is reachable
            ##flag_isRegistered(Bool) True Indicates if the AP is currently
             registered to a WLC
            ##flag_isModified(Bool) True indicates that the current "Pre" state/config
            for the AP has changed. NOTE: This state/config is an offline copy stored
            in memory in Dino, not an active realtime config. Any changes would have
            to be pushed for them to take affect
            ##flag_setReboot(Tuple "(Bool, delay_time_value)") True indicate that the AP has
            a reboot scheduled to occur. *args passed to tuple indicate timer till reload.
            ##flag_setDefault(Bool) True indicate this AP has been flagged to perform a factory
             default operation on the config. If Scheduled this flag works with flag_reboot
            ##flag_ackModified(UNDECIDED) Idea is to have the user of Dino confirm the changes to
        be pushed to any and all APs first, in which it would trigger this flag and log the event.
        Still undecided if it will be used
        :param args:
        :param kwargs:
        :return:
        """
        self.flag_isAlive = False
        self.flag_isRegistered = False
        self.flag_isModified = False
        self.flag_setReboot = False
        self.flag_setDefault = False
        self.flag_ackModified = False

    def ap_state(self):
        """
        This func controls the current and recent
        state/config of the AP to be used for
        sanity and completion checks. State is
        copied to the class if modifications are
        slated for this AP . Should a pre-post check
        fail either by seeing unintented state values
        or another validation check...this app will
        error out and dump to a log "why".
        """
        ## state_data is a dict containing all data stored for
        ### object as gathered since last poll. This is "PRE" config
        #### data for check
        self.pre_state_data = {}
        def __check__(self):
            """
            AP's !! PRE modifaction !! data current state/config data stored
            To be used for sanity comparisons and atomic checks and compare
            to the POST modification for "desired state" checks
            """
            self.pre_state_data
        def __update__(self):
            """
            Force polling of APs controller device for new state info
            related to AP
            """


class ConnexList(object):
	def __init__(self, match_list):
		self.connexList = match_list
		self.connexArgs = {}
		self.sendCmds = []
	def __enter__(self):
		self.connexList = match_list.copy()
		self.ConnexArgs = self.setConnArgs(self)
		return self.connexList, ConnexArgs
	def setConnArgs(self):
		import getpass
		self.connexArgs = {"ip": self.connexList[0]}
		return self.connexArgs
	def getConnArgs(self):
		self.getConnArgs = print(self.connexArgs)
	def getCmds(self):
		self.sendCmds = ap_rename20.api_create_commands(connexList)
		return self.sendCmds
	def __exit__(self):
		self.connexList.clear()
