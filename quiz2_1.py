# Generate NE delete, add and OAM script automatically
siteID = input("Please input the site ID: ")
# print(siteID)
oamIP = input("Please input the OAM IP: ")

with open(siteID + "_add.txt", "w") as nodeaddtxt:
    nodeaddtxt.truncate()
    nodeaddtxt.write("cmedit create NetworkElement=" + siteID + " networkElementId=" + siteID + ",neType=RadioNode,ossPrefix=\"SubNetwork=ONRM_ROOT_MO,SubNetwork=Riyadh_Nodes,MeContext=" + siteID + "\",timeZone=\"Asia/Riyadh\" -ns=OSS_NE_DEF -version=2.0.0\n")
    nodeaddtxt.write("cmedit create NetworkElement=" + siteID + ",ComConnectivityInformation=1 ComConnectivityInformationId=1,snmpVersion=\"SNMP_V3\",snmpWriteCommunity=\"public\",snmpReadCommunity=\"public\", transportProtocol=\"TLS\",port=6513, ipAddress=\"" + oamIP + "\" -ns=COM_MED -version=1.1.0\n")
    nodeaddtxt.write("secadm credentials create --secureusername rbs --secureuserpassword \"rbs\" -n " + siteID + "\n")
    nodeaddtxt.write("cmedit get NetworkElement=" + siteID + ",SecurityFunction=1,NetworkElementSecurity=1\n")
    nodeaddtxt.write("cmedit set NetworkElement=" + siteID + ",CmNodeHeartbeatSupervision=1 active=true\n")
    nodeaddtxt.write("cmedit set NetworkElement=" + siteID + ",PmFunction=1 pmEnabled=true\n")
    nodeaddtxt.write("cmedit set NetworkElement=" + siteID + ",FmAlarmSupervision=1 active=true\n")
    nodeaddtxt.write("cmedit set NetworkElement=" + siteID + ",InventorySupervision=1 active=true\n")
    nodeaddtxt.write("cmedit action NetworkElement=" + siteID + ",CmFunction=1 sync\n")
    nodeaddtxt.write("cmedit get NetworkElement=" + siteID + ",CmFunction=1\n")
    nodeaddtxt.close()

with open(siteID + "_delete.txt", "w") as nodedeltxt:
    nodedeltxt.truncate()
    nodedeltxt.write("cmedit set NetworkElement=" + siteID + ",PmFunction=1 pmEnabled=false --force\n")
    nodedeltxt.write("cmedit set NetworkElement=" + siteID + ",CmNodeHeartbeatSupervision=1 active=false\n")
    nodedeltxt.write("cmedit set NetworkElement=" + siteID + ",InventorySupervision=1 active=false\n")
    nodedeltxt.write("alarm disable " + siteID + "\n")
    nodedeltxt.write("cmedit action NetworkElement=" + siteID + ",CmFunction=1 deleteNrmDataFromEnm\n")
    nodedeltxt.write("cmedit delete NetworkElement=" + siteID + " -ALL --force\n")
    nodedeltxt.close()

oamPart1 = """<Entities xmlns:xsi=\"http: // www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"EntitiesSchema.xsd\">
  <Entity>
    <PublishCertificatetoTDPS>true</PublishCertificatetoTDPS>
    <EntityProfile Name=\"DUSGen2OAM_CHAIN_EP\"/>
    <KeyGenerationAlgorithm>
      <Name>RSA</Name>
      <KeySize>2048</KeySize>
    </KeyGenerationAlgorithm>
    <Category>
      <Modifiable>true</Modifiable>
      <Name>NODE-OAM</Name>
    </Category>
    <EntityInfo>
"""
oamPart2 = """      <Subject>
        <SubjectField>
          <Type>ORGANIZATION</Type>
          <Value>Ericsson</Value>
        </SubjectField>
        <SubjectField>
          <Type>ORGANIZATION_UNIT</Type>
          <Value>STC</Value>
        </SubjectField>
        <SubjectField>
          <Type>COUNTRY_NAME</Type>
          <Value>SA</Value>
        </SubjectField>
        <SubjectField>
          <Type>COMMON_NAME</Type>
"""
oamPart3 = """        </SubjectField>
      </Subject>
    </EntityInfo>
  </Entity>
</Entities>
"""

with open("Entity_" + siteID + "_oam.txt", "w") as nodeoamtxt:
    nodeoamtxt.truncate()
    nodeoamtxt.write(oamPart1)
    nodeoamtxt.write("      <Name>" + siteID + "-oam</Name>\n")
    nodeoamtxt.write(oamPart2)
    nodeoamtxt.write("          <Value>" + siteID + "-oam</Value>\n")
    nodeoamtxt.write(oamPart3)
    nodeoamtxt.close()