def calcularVlan(olt, sl):
    vlan = 0
    if olt == "Olt ZTE 1":
        if int(sl) < 10:
            vlan = 1000 + (int(sl) - 1)
        else:
            vlan = 1000 + (int(sl) - 3)
    elif olt == "Olt ZTE 2":
        vlan = 3001
    elif olt == "Olt Nokia Vicente Pires":
        vlan = 2009 + (int(sl))
    elif olt == "Olt Nokia Ceilandia 1":
        vlan = 2049 + (int(sl))
    elif olt == "Olt Nokia Ceilandia 2":
        vlan = 2057 + (int(sl))
    elif olt == "Olt Nokia Recando das Emas":
        vlan = 2065 + (int(sl))
    return vlan

def scriptZTE(serial, sl, pn, ps, oltEsc, contratoDig, modeloOnu):
    if contratoDig == "":
        contratoDig = "0000"
    scriptMult = ""
    if ps == None: ps = "1"
    vlan = calcularVlan(oltEsc, sl)
    if modeloOnu == "zte wifi":
        scriptMult = ("configure terminal\ninterface gpon-olt_1/" + sl + "/" + pn + "\n"
            "   onu " + str(ps) + " type F670L sn " + serial + "\n"
            "exit \n"
            "   interface gpon-onu_1/" + sl + "/" + pn + ":" + str(ps) + "\n"
            "   name " + contratoDig + "\n"
            "   sn-bind enable sn\n"
            "   tcont 4 profile 1G\n"
            "   tcont 4 profile 1G\n"
            "   gemport 1 tcont 4\n"
            "   service-port 1 vport 1 user-vlan " + str(vlan) + " vlan " + str(vlan) + "\n"
            "   ip dhcp snooping enable vport 1\n"
            "   port-identification format TEST vport 1\n"
            "   dhcpv4-l2-relay-agent enable vport 1\n"
            "exit\n"
            "   pon-onu-mng gpon-onu_1/" + sl + "/" + pn + ":" + str(ps) + "\n"
            "   service 1 gemport 1 vlan " + str(vlan) + "\n"
            "   wan-ip 1 mode dhcp vlan-profile slot" + sl + "-" + str(vlan) + " host 1\n"
            "   ssid ctrl wifi_0/1 user-isolation disable\n"
            "   ssid ctrl wifi_0/5 user-isolation disable\n"
            "   security-mgmt 1 state enable mode forward protocol web\n"
            "exit\n")
    elif modeloOnu == "bridge":
        scriptMult = ("configure terminal\ninterface gpon-olt_1/" + sl + "/" + pn + "\n"
            "   onu " + str(ps) + " type F670L sn " + serial + "\n"
            "exit \n"
            "   interface gpon-onu_1/" + sl + "/" + pn + ":" + str(ps) + "\n"
            "   fec upstream\n"
            "   sn-bind enable sn\n"
            "   tcont 4 profile 1G\n"
            "   gemport 1 tcont 4\n"
            "   service-port 1 vport 1 user-vlan " + str(vlan) + " vlan " + str(vlan) + "\n"
            "   ip dhcp snooping enable vport 1\n"
            "   port-identification format TEST vport 1\n"
            "   dhcpv4-l2-relay-agent enable vport 1\n"
            "exit\n"
            "   pon-onu-mng gpon-onu_1/" + sl + "/" + pn + ":" + str(ps) + "\n"
            "   service 1 gemport 1 vlan " + str(vlan) + "\n"
            "   vlan port eth_0/1 mode tag vlan " + str(vlan) + "\n"
            "exit\n")
    return scriptMult

def scriptNokia(serial, sl, pn, ps, oltEsc, contratoDig, modeloOnu):
    if modeloOnu == "nokia 2":
        swVer = "AUTO"
        preConf = "PREALCL73X"
    else:
        swVer = "AUTO"
        preConf = "AUTO"
    if contratoDig == "":
        contratoDig = "xxxx"
    script = ""
    vlan = calcularVlan(oltEsc, sl)
    if ps==None or ps=="": ps="1"
    if modeloOnu == "nokia" or modeloOnu == "nokia 2":
        script = ("ENT-ONT::ONT-1-1-" + sl + "-" + pn + "-" + str(ps) + "::::DESC1=\"ONU NOKIA\",DESC2=\"" + contratoDig + "\",SERNUM=" + serial + ",SWVERPLND=" + swVer + ",DLSW=" + swVer + ",OPTICSHIST=ENABLE,PLNDCFGFILE1=" + preConf + ",DLCFGFILE1=" + preConf + ",VOIPALLOWED=VEIP;\n"
                        "ED-ONT::ONT-1-1-" + sl + "-" + pn + "-" + str(ps) + ":::::IS;\n"
                        "ENT-ONTCARD::ONTCARD-1-1-" + sl + "-" + pn + "-" + str(ps) + "-14:::VEIP,1,0::IS;\n"
                        "ENT-LOGPORT::ONTL2UNI-1-1-" + sl + "-" + pn + "-" + str(ps) + "-14-1:::;\n"
                        "ED-ONTVEIP::ONTVEIP-1-1-" + sl + "-" + pn + "-" + str(ps) + "-14-1:::::IS;\n"
                        "SET-QOS-USQUEUE::ONTL2UNIQ-1-1-" + sl + "-" + pn + "-" + str(ps) + "-14-1-0::::USBWPROFNAME=HSI_1G_UP;\n"
                        "SET-VLANPORT::ONTL2UNI-1-1-" + sl + "-" + pn + "-" + str(ps) + "-14-1:::MAXNUCMACADR=4,CMITMAXNUMMACADDR=1;\n"
                        "ENT-VLANEGPORT::ONTL2UNI-1-1-" + sl + "-" + pn + "-" + str(ps) + "-14-1:::0," + str(vlan) + ":PORTTRANSMODE=SINGLETAGGED;\n"
                        "ENT-VLANEGPORT::ONTL2UNI-1-1-" + sl + "-" + pn + "-" + str(ps) + "-14-1:::0,777:PORTTRANSMODE=SINGLETAGGED;\n"
                        "ENT-HGUTR069-SPARAM::HGUTR069SPARAM-1-1-" + sl + "-" + pn + "-" + str(ps) + "-1::::PARAMNAME=InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.X_CT-COM_WANGponLinkConfig.VLANIDMark,PARAMVALUE=" + str(vlan) + ";\n")
    elif modeloOnu == "bridge" or modeloOnu == "zte wifi":
        script = ("ENT-ONT::ONT-1-1-" + sl + "-" + pn + "-" + str(ps) + "::::DESC1=\"Bridge\",DESC2=\"" + contratoDig + "\",SERNUM=" + serial + ",SWVERPLND=DISABLED;\n"
                        "ED-ONT::ONT-1-1-" + sl + "-" + pn + "-" + str(ps) + ":::::IS;\n"
                        "ENT-ONTCARD::ONTCARD-1-1-" + sl + "-" + pn + "-" + str(ps) + "-1:::10_100BASET,1,0::IS;\n"
                        "ENT-LOGPORT::ONTL2UNI-1-1-" + sl + "-" + pn + "-" + str(ps) + "-1-1:::;\n"
                        "ED-ONTVEIP::ONTVEIP-1-1-" + sl + "-" + pn + "-" + str(ps) + "-1-1:::::IS;\n"
                        "SET-QOS-USQUEUE::ONTL2UNIQ-1-1-" + sl + "-" + pn + "-" + str(ps) + "-1-1-0::::USBWPROFNAME=HSI_1G_UP;\n"
                        "SET-VLANPORT::ONTL2UNI-1-1-" + sl + "-" + pn + "-" + str(ps) + "-1-1:::MAXNUCMACADR=32,CMITMAXNUMMACADDR=1;\n"
                        "ENT-VLANEGPORT::ONTL2UNI-1-1-" + sl + "-" + pn + "-" + str(ps) + "-1-1:::0," + str(vlan) + ":PORTTRANSMODE=UNTAGGED;\n"
                        "SET-VLANPORT::ONTL2UNI-1-1-" + sl + "-" + pn + "-" + str(ps) + "-1-1:::DEFAULTCVLAN=" + str(vlan) + ";\n")
    return script