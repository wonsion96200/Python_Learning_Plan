# for calculating latency of XN handover

# import datetime
import tkinter as tk
from tkinter import filedialog, scrolledtext, END, NORMAL
from os import getcwd
from datetime import datetime


def calculateXNHOLatency(traceFlowsrc, traceFlowtar):
    latency = []
    lineNumbersrc = 0
    for linesrc in traceFlowsrc:
        if "(XNAP)  HandoverRequest:" in linesrc and "==>" in linesrc:
            # HORequestsrcTimestr = linesrc.split()[1]  # get str "02:07:25.965778322" to compare
            HORequestsrcTimeStamp = datetime.strptime(linesrc.split()[1][0:15],
                                                      "%H:%M:%S.%f")  # convert 03:49:54.539548 to a time
            rrcReconfTimeStamp = measTimeStamp = HORequestAcksrcTimeStamp = UEContextReleasesrcTimeStamp = HORequesttarTimestamp = \
                HORequestAcktarTimeStamp = rrcReconfCompleteTimeStamp = PSSwitchRequestTimeStamp = \
                PSSwitchRequestackTimeStamp = UEContextReleasetarTimeStamp = HORequestsrcTimeStamp
            ueTraceIdsrc = linesrc.split()[11]
            # print(HORequestsrcTimeStamp)
            # print(ueTraceIdsrc)
            tempLineNumbersrc = lineNumbersrc
            # measFound = 0
            while tempLineNumbersrc >= 0:
                if "(RRC5G) MeasurementReport:" in traceFlowsrc[tempLineNumbersrc] and \
                        ueTraceIdsrc in traceFlowsrc[tempLineNumbersrc]:
                    measTimeStamp = datetime.strptime(traceFlowsrc[tempLineNumbersrc].split()[1][0:15], "%H:%M:%S.%f")
                    # print(measTimeStamp)
                    break
                tempLineNumbersrc -= 1

            tempLineNumbersrc = lineNumbersrc
            HORequestAcksrcFound = 0
            while tempLineNumbersrc < len(traceFlowsrc):
                if "(XNAP)  HandoverRequestAcknowledge:" in traceFlowsrc[tempLineNumbersrc] and \
                        ueTraceIdsrc in traceFlowsrc[tempLineNumbersrc] and \
                        "<==" in traceFlowsrc[tempLineNumbersrc]:
                    HORequestAcksrcTimeStamp = datetime.strptime(traceFlowsrc[tempLineNumbersrc].split()[1][0:15],
                                                                 "%H:%M:%S.%f")
                    # print(HORequestAcksrcTimeStamp)
                    HORequestAcksrcFound = 1
                elif "(RRC5G) RRCReconfiguration:" in traceFlowsrc[tempLineNumbersrc] and \
                        ueTraceIdsrc in traceFlowsrc[tempLineNumbersrc] and HORequestAcksrcFound == 1:
                    rrcReconfTimeStamp = datetime.strptime(traceFlowsrc[tempLineNumbersrc].split()[1][0:15],
                                                           "%H:%M:%S.%f")
                    # print(rrcReconfTimeStamp)
                elif "(XNAP)  UEContextRelease:" in traceFlowsrc[tempLineNumbersrc] and \
                        ueTraceIdsrc in traceFlowsrc[tempLineNumbersrc] and "<==" in traceFlowsrc[tempLineNumbersrc]:
                    UEContextReleasesrcTimeStamp = datetime.strptime(traceFlowsrc[tempLineNumbersrc].split()[1][0:15],
                                                           "%H:%M:%S.%f")
                    break
                tempLineNumbersrc += 1

            lineNumbertar = 0
            HORequesttarfound = 0
            ueTraceIdtar = "ueTraceIdtar"
            rrcReconfCompletefound = 0
            while lineNumbertar < len(traceFlowtar):
                if "(XNAP)  HandoverRequest:" in traceFlowtar[lineNumbertar] and HORequesttarfound == 0 and \
                        "<==" in traceFlowtar[lineNumbertar]:
                    if abs((datetime.strptime(traceFlowtar[lineNumbertar].split()[1][0:15], "%H:%M:%S.%f") -
                           HORequestsrcTimeStamp)).total_seconds() * 1000 < 10:
                        HORequesttarfound = 1
                        ueTraceIdtar = traceFlowtar[lineNumbertar].split()[11]
                        HORequesttarTimestamp = datetime.strptime(traceFlowtar[lineNumbertar].split()[1][0:15],
                                                                  "%H:%M:%S.%f")
                        # print(HORequesttarTimestamp)
                elif "(XNAP)  HandoverRequestAcknowledge:" in traceFlowtar[lineNumbertar] and \
                        ueTraceIdtar in traceFlowtar[lineNumbertar] and \
                        "==>" in traceFlowtar[lineNumbertar]:
                    HORequestAcktarTimeStamp = datetime.strptime(traceFlowtar[lineNumbertar].split()[1][0:15],
                                                                 "%H:%M:%S.%f")
                elif "(RRC5G) RRCReconfigurationComplete:" in traceFlowtar[lineNumbertar] and \
                        ueTraceIdtar in traceFlowtar[lineNumbertar] and \
                        HORequesttarfound == 1 and rrcReconfCompletefound == 0:
                    rrcReconfCompletefound = 1
                    rrcReconfCompleteTimeStamp = datetime.strptime(traceFlowtar[lineNumbertar].split()[1][0:15],
                                                                   "%H:%M:%S.%f")
                elif "(NGAP)  PathSwitchRequest:" in traceFlowtar[lineNumbertar] and \
                        ueTraceIdtar in traceFlowtar[lineNumbertar]:
                    PSSwitchRequestTimeStamp = datetime.strptime(traceFlowtar[lineNumbertar].split()[1][0:15],
                                                                 "%H:%M:%S.%f")
                elif "(NGAP)  PathSwitchRequestAcknowledge:" in traceFlowtar[lineNumbertar] and \
                        ueTraceIdtar in traceFlowtar[lineNumbertar]:
                    PSSwitchRequestackTimeStamp = datetime.strptime(traceFlowtar[lineNumbertar].split()[1][0:15],
                                                                    "%H:%M:%S.%f")
                elif "(XNAP)  UEContextRelease:" in traceFlowtar[lineNumbertar] and \
                        ueTraceIdtar in traceFlowtar[lineNumbertar] and \
                        "==>" in traceFlowtar[lineNumbertar]:
                    UEContextReleasetarTimeStamp = datetime.strptime(traceFlowtar[lineNumbertar].split()[1][0:15],
                                                                     "%H:%M:%S.%f")
                    break
                lineNumbertar += 1

            phaseA = (HORequestsrcTimeStamp - measTimeStamp).total_seconds() * 1000
            phaseB = (HORequestAcktarTimeStamp - HORequesttarTimestamp).total_seconds() * 1000
            phaseC = (rrcReconfTimeStamp - HORequestAcksrcTimeStamp).total_seconds() * 1000
            phaseD = (PSSwitchRequestTimeStamp - rrcReconfCompleteTimeStamp).total_seconds() * 1000
            phaseE = (UEContextReleasetarTimeStamp - PSSwitchRequestackTimeStamp).total_seconds() * 1000
            E2E = (UEContextReleasesrcTimeStamp - measTimeStamp).total_seconds() * 1000
            NG_process = (PSSwitchRequestackTimeStamp - PSSwitchRequestTimeStamp).total_seconds() * 1000
            latency.append(
                [ueTraceIdsrc + "\t", ueTraceIdsrc + "\t", str(round(phaseA, 3)) + "\t", str(round(phaseB, 3)) +
                 "\t", str(round(phaseC, 3)) + "\t", str(round(phaseD, 3)) + "\t", str(round(phaseE, 3)) + "\t",
                 str(round(phaseA + phaseC, 3)) + "\t", str(round(phaseB + phaseD + phaseE, 3)) + "\t",
                 str(round(E2E, 3)) + "\t", str(round(NG_process, 3))])

        lineNumbersrc += 1
    return latency


def open_file():
    open_file_types = [('All Files', '.*'), ('Text Files', '.txt')]
    file_path1 = filedialog.askopenfilename(title="Open", initialdir=getcwd(), filetypes=open_file_types)
    if file_path1 is not None:
        with open(file_path1, "r") as fileRead:
            traceFlowsrc = fileRead.readlines()

    file_path2 = filedialog.askopenfilename(title="Open", initialdir=getcwd(), filetypes=open_file_types)
    if file_path2 is not None:
        with open(file_path2, "r") as fileRead:
            traceFlowtar = fileRead.readlines()

    latencyHeader = [["ue_trace_id_src\t", "ue_trace_id_tar\t", "PhaseA\t", "PhaseB\t", "PhaseC\t", "PhaseD\t",
                      "PhaseE\t", "TotalSrc\t", "TotalTar\t", "E2E\t", "NG_process\t"]]

    showText.delete(0.0, END)
    for i in latencyHeader:
        # print('\t'.join(i))
        showText.insert(END, ' '.join(i) + "\n")  # END: insert from the END
    for i in calculateXNHOLatency(traceFlowsrc, traceFlowtar):
        # print('\t'.join(i))
        showText.insert(END, ' '.join(i) + "\n")  # END: insert from the END
    for i in calculateXNHOLatency(traceFlowtar, traceFlowsrc):
        # print('\t'.join(i))
        showText.insert(END, ' '.join(i) + "\n")  # END: insert from the END


if __name__ == '__main__':

    applicationWindow = tk.Tk()
    applicationWindow.title("XN HO Latency Calculator V1.0")
    applicationWindow.resizable(0, 0)  # if height and width are resizable
    applicationWindow.geometry("960x550")  # window initial size

    # showText = tk.Text(applicationWindow, width=50, state=tk.DISABLED)
    # state=tk.DISABLED not allowed to edit
    showText = scrolledtext.ScrolledText(applicationWindow, width=75, state=NORMAL, font=("Lucida Console", 10))
    # showText.grid(column=0, row=0, padx=10, pady=10)  # padx, pady 控件外填充
    showText.place(x=20, y=50, width=930, height=450)

    poweredBy = tk.Label(applicationWindow, text="Powered by Suzhou SA CD Project")
    # poweredBy.grid(column=1, row=1)
    poweredBy.place(x=740, y=520, width=200, height=20)

    openButton = tk.Button(applicationWindow, text="Open", width=12, height=2, command=open_file)
    # openButton.grid(column=1, row=0)
    openButton.place(x=830, y=15, width=80, height=25)

    applicationWindow.mainloop()  # show application window

    # input("Please press any key to end")
