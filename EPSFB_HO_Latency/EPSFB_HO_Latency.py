# for calculating latency of EPSFB with handover

import datetime

with open("gnb_Measurement_HO_ok.flow", "r") as fileRead:
    traceFlow = fileRead.readlines()
    fileRead.close()

latency = [["ue_trace_id     \t", "PhaseA\t", "PhaseB\t", "PhaseC\t", "PhaseD\t"]]
lineNumber = 0
for line in traceFlow:
    if "(NGAP)  PDUSessionResourceModifyRequest:" in line:
        pduModifyTimeStamp = datetime.datetime.strptime(line.split()[1][0:15], "%H:%M:%S.%f") # convert 03:49:54.539548 to a time
        rrcReconfTimeStamp = measTimeStamp = hoRequiredTimeStamp = hoCommandTimeStamp = mobilityCommandTimeStamp = ueRelCommandTimeStamp = ueRelCompleteTimeStamp = pduModifyTimeStamp
        ueTraceId = line.split()[10]
        # print(pduModifyTimeStamp)
        tempLineNumber = lineNumber + 1
        measFound = 0
        while tempLineNumber < len(traceFlow):
            if "(RRC5G) RRCReconfiguration:" in traceFlow[tempLineNumber] and traceFlow[tempLineNumber].split()[5] == ueTraceId:
                rrcReconfTimeStamp = datetime.datetime.strptime(traceFlow[tempLineNumber].split()[1][0:15], "%H:%M:%S.%f")
                # print(rrcReconfTimeStamp)
            elif "(RRC5G) MeasurementReport:" in traceFlow[tempLineNumber] and traceFlow[tempLineNumber].split()[5] == ueTraceId and measFound == 0:
                measTimeStamp = datetime.datetime.strptime(traceFlow[tempLineNumber].split()[1][0:15], "%H:%M:%S.%f")
                measFound = 1
                # print(measTimeStamp)
            elif "(NGAP)  HandoverRequired:" in traceFlow[tempLineNumber] and traceFlow[tempLineNumber].split()[10] == ueTraceId:
                hoRequiredTimeStamp = datetime.datetime.strptime(traceFlow[tempLineNumber].split()[1][0:15], "%H:%M:%S.%f")
                # print(hoRequiredTimeStamp)
            elif "(NGAP)  ParsingError:" in traceFlow[tempLineNumber] and traceFlow[tempLineNumber].split()[10] == ueTraceId:
                hoCommandTimeStamp = datetime.datetime.strptime(traceFlow[tempLineNumber].split()[1][0:15], "%H:%M:%S.%f")
                # print(hoCommandTimeStamp)
            elif "(RRC5G) MobilityFromNRCommand:" in traceFlow[tempLineNumber] and traceFlow[tempLineNumber].split()[5] == ueTraceId:
                mobilityCommandTimeStamp = datetime.datetime.strptime(traceFlow[tempLineNumber].split()[1][0:15], "%H:%M:%S.%f")
                # print(mobilityCommandTimeStamp)
            elif "(NGAP)  UEContextReleaseCommand:" in traceFlow[tempLineNumber] and traceFlow[tempLineNumber].split()[10] == ueTraceId:
                ueRelCommandTimeStamp = datetime.datetime.strptime(traceFlow[tempLineNumber].split()[1][0:15], "%H:%M:%S.%f")
                # print(ueRelCommandTimeStamp)
            elif "(NGAP)  UEContextReleaseComplete:" in traceFlow[tempLineNumber] and traceFlow[tempLineNumber].split()[10] == ueTraceId:
                ueRelCompleteTimeStamp = datetime.datetime.strptime(traceFlow[tempLineNumber].split()[1][0:15], "%H:%M:%S.%f")
                # print(ueRelCompleteTimeStamp)
                break
            tempLineNumber += 1
        phaseA = (rrcReconfTimeStamp - pduModifyTimeStamp).microseconds / 1000
        phaseB = (hoRequiredTimeStamp - measTimeStamp).microseconds / 1000
        phaseC = (mobilityCommandTimeStamp - hoCommandTimeStamp).microseconds / 1000
        phaseD = (ueRelCompleteTimeStamp - ueRelCommandTimeStamp).microseconds / 1000
        # print("Phase A latency: " + str(phaseA) + " ms")
        # print("Phase B latency: " + str(phaseB) + " ms")
        # print("Phase C latency: " + str(phaseC) + " ms")
        # print("Phase D latency: " + str(phaseD) + " ms")
        latency.append([ueTraceId + "\t", str(phaseA) + "\t", str(phaseB) + "\t", str(phaseC) + "\t", str(phaseD) + "\t"])
    lineNumber += 1

for i in latency:
    print(' '.join(i))

# input("Please press any key to end")
