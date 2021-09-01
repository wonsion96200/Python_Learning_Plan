# for calculating latency of EPSFB with handover

# import datetime
# import tkinter
from tkinter import Tk, Button, Label, scrolledtext, END, NORMAL
from tkinter import filedialog
from os import getcwd
from datetime import datetime


def open_file():
    open_file_types = [('All Files', '.*'), ('Text Files', '.txt')]
    file_path = filedialog.askopenfilename(title="Open", initialdir=getcwd(), filetypes=open_file_types)
    if file_path is not None:
        with open(file_path, "r") as fileRead:
            traceFlow = fileRead.readlines()

        latency = [["ue_trace_id       \t", "PhaseA\t", "PhaseB"]]
        lineNumber = 0
        for line in traceFlow:
            if "(NGAP)  HandoverRequired:" in line:
                HandoverRequiredTimeStamp = datetime.strptime(line.split()[1][0:15],
                                                                "%H:%M:%S.%f")  # convert 03:49:54.539548 to a time
                HandoverCommandTimeStamp = RRCReconfigTimeStamp = UEContextReleaseCommandTimeStamp = UEContextReleaseCompleteTimeStamp = \
                HandoverRequiredTimeStamp
                ue_trace_id = line.split()[11]
                print(HandoverRequiredTimeStamp)
                tempLineNumber = lineNumber + 1
                RRCReconfigFound = 0
                RRCReconfigCompleteFound = 0
                while tempLineNumber < len(traceFlow):
                    if "(NGAP)  HandoverCommand:" in traceFlow[tempLineNumber] and \
                            traceFlow[tempLineNumber].split()[11] == ue_trace_id:
                        HandoverCommandTimeStamp = datetime.strptime(traceFlow[tempLineNumber].split()[1][0:15],
                                                                        "%H:%M:%S.%f")
                        #print(HandoverCommandTimeStamp)
                    elif "(RRC5G) RRCReconfiguration:" in traceFlow[tempLineNumber] and \
                            traceFlow[tempLineNumber].split()[6] == ue_trace_id and RRCReconfigFound == 0:
                        RRCReconfigTimeStamp = datetime.strptime(traceFlow[tempLineNumber].split()[1][0:15],
                                                                   "%H:%M:%S.%f")
                        RRCReconfigFound = 1
                        print(RRCReconfigTimeStamp)
                    elif "(NGAP)  UEContextReleaseCommand:" in traceFlow[tempLineNumber] and "cause:radioNetwork:successful-handover" in traceFlow[tempLineNumber] and \
                            traceFlow[tempLineNumber].split()[11] == ue_trace_id:
                        UEContextReleaseCommandTimeStamp = datetime.strptime(traceFlow[tempLineNumber].split()[1][0:15],
                                                                         "%H:%M:%S.%f")
                        print(UEContextReleaseCommandTimeStamp)
                    elif "(NGAP)  UEContextReleaseComplete:" in traceFlow[tempLineNumber] and \
                            traceFlow[tempLineNumber].split()[11] == ue_trace_id:
                        UEContextReleaseCompleteTimeStamp = datetime.strptime(traceFlow[tempLineNumber].split()[1][0:15],
                                                                        "%H:%M:%S.%f")
                        break
                        # print(hoCommandTimeStamp)
                    tempLineNumber += 1
                phaseA = (HandoverCommandTimeStamp - HandoverRequiredTimeStamp).microseconds / 1000
                phaseB = (UEContextReleaseCommandTimeStamp - HandoverRequiredTimeStamp).microseconds / 1000
                #phaseC = (mobilityCommandTimeStamp - hoCommandTimeStamp).microseconds / 1000
                #phaseD = (ueRelCompleteTimeStamp - ueRelCommandTimeStamp).microseconds / 1000
                #phaseE = (mobilityCommandTimeStamp - measTimeStamp).microseconds / 1000
                print("Phase A latency: " + str(phaseA) + " ms")
                print("Phase B latency: " + str(phaseB) + " ms")
                # print("Phase C latency: " + str(phaseC) + " ms")
                # print("Phase D latency: " + str(phaseD) + " ms")
                latency.append([ue_trace_id + "\t", str(phaseA) + "\t", str(phaseB)])
            lineNumber += 1

        showText.delete(0.0, END)

        for i in latency:
            # print('\t'.join(i))
            showText.insert(END, ' '.join(i) + "\n")  # END: insert from the END


applicationWindow = Tk()
applicationWindow.title("EPSFB HO Latency Calculator V1.3")
applicationWindow.resizable(0, 0)  # if height and width are resizable
applicationWindow.geometry("850x450")  # window initial size

# showText = tkinter.Text(applicationWindow, width=50, state=tkinter.DISABLED)
# state=tkinter.DISABLED not allowed to edit
showText = scrolledtext.ScrolledText(applicationWindow, width=75, state=NORMAL, font=("Courier New", 10))
showText.grid(column=0, row=0, padx=10, pady=10)  # padx, pady 控件外填充

poweredBy = Label(applicationWindow, text="Powered by Suzhou SA CD Project")
poweredBy.grid(column=1, row=1)

openButton = Button(applicationWindow, text="Open", width=12, height=2, command=open_file)
openButton.grid(column=1, row=0)

applicationWindow.mainloop()  # show application window

# input("Please press any key to end")