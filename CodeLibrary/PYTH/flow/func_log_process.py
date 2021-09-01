#!python2
# coding=utf-8
import os

import obj_data
import obj_file
import obj_log2csv
from obj_log_grep import Grep
from obj_read_config import Config

config = Config()

grep_datetime = "'[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9] '"
grep_datetime_with_c = "'[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9];[0-9][0-9]:[0-9][0-9]:[0-9][0-9];'"

grep2csv = obj_log2csv


class LogProcess(Grep):
    def __init__(self):
        """
        """
        super(Grep, self).__init__()
        self.log_prefix = config.log_prefix
        self.grep_v = ""
        self.grep_i2 = ""
        self.grep_i3 = ""

    def nr_cell_relation(self):
        self.grep_files = "*_hgetcnrcellrelation*.log"
        self.grep_v = ""
        self.output_file = "record_NRCellRelation.txt"
        self.grep_i = "',NRCellRelation='"
        self.grep_i2 = "',ExternalNRCellCU='"
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.nr_cell_relation2csv(grep_file)
        return csv_file

    def external_nr_cell_cu(self):
        self.grep_files = "*_hgetcexternalnrcellcu*.log"
        self.grep_v = ""
        self.output_file = "record_ExternalNRCellCU.txt"
        self.grep_i = "',ExternalNRCellCU='"
        self.grep_i2 = ""
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.external_nr_cell_cu2csv(grep_file)
        return csv_file

    def external_gnb_cucp_function(self):
        self.grep_files = "*_hgetcexternalgnbcucpfunction*.log"
        self.grep_v = ""
        self.output_file = "record_ExternalGNBCUCPFunction.txt"
        self.grep_i = "',ExternalGNBCUCPFunction='"
        self.grep_i2 = ""
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.external_gnb_cucp_function2csv(grep_file)
        return csv_file

    def nr_freq_relation(self):
        self.grep_files = "*_hgetcnrfreqrelation*.log"
        self.grep_v = ""
        self.output_file = "record_NRFreqRelation.txt"
        self.grep_i = "',NRFreqRelation='"
        self.grep_i2 = ""
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.nr_freq_relation2csv(grep_file)
        return csv_file

    def nr_frequency(self):
        self.grep_files = "*_hgetcnrfrequency*.log"
        self.grep_v = ""
        self.output_file = "record_NRFrequency.txt"
        self.grep_i = "',NRFrequency='"
        self.grep_i2 = ""
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.nr_frequency2csv(grep_file)
        return csv_file

    def gnb_cucp_function(self):
        self.grep_files = "*_hgetcgnbcucpfunction*.log"
        self.grep_v = ""
        self.output_file = "record_GNBCUCPFunction.txt"
        self.grep_i = "'GNBCUCPFunction='"
        self.grep_i2 = ""
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.gnb_cucp_function(grep_file)
        return csv_file

    def counters_cell(self):
        self.grep_files = "*_pmxocsv*.log"
        self.grep_v = ""
        self.output_file = "record_counters_cell.txt"
        self.grep_i = "E 'NRCellCU=|NRCellDU=|EUtranCellFDD=|EUtranCellTDD='"
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.pmxocsv2csv(grep_file)
        return csv_file

    def mtd_debug(self):
        self.grep_files = "*_mtddebug*.log"
        self.grep_v = ""
        self.output_file = "record_mtd_debug.txt"
        self.grep_i = "'numPktsDrop'"
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.mtd_debug2csv(grep_file)
        return csv_file

    def sleeping_cell(self):
        self.grep_files = "*_pmxn*.log"
        self.grep_v = ""
        self.output_file = "record_sleeping_cell.txt"
        self.grep_i = "E 'ifHCInUcastPkts;|pmPdcpPktReceivedDl;|pmRrcConnLevSum;'"
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.sleeping_cell2csv(grep_file)
        return csv_file

    def altc(self):
        self.grep_files = "*_altc.log"
        self.grep_v = "E 'External Link Failure|Service Unavailable|Service Degraded'"
        self.output_file = "record_alarm.txt"
        self.grep_i = grep_datetime_with_c
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.altc2csv(grep_file)
        # no_contact
        self.grep_files = "mobatch_result.txt"
        self.grep_i = "'no contact '"
        self.grep_v = ""
        self.output_file = "record_no_contact.txt"
        grep_file_no_contact = self.execute_grep()
        # put no_contact to altc as "Heartbeat Failure"
        if grep_file_no_contact and csv_file:
            grep2csv.nocontact2csvaltc(grep_file_no_contact, csv_file)

        data = obj_data.read_csv_to_data(csv_file)

        csv_file = obj_data.write_data_to_csv(data, csv_file)
        return csv_file, grep_file_no_contact

    def invlrc(self):
        self.grep_files = "*_invlrc.log"
        self.grep_i = "' ;CXC'"
        self.grep_v = ""
        self.output_file = "record_license.txt"
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.invlrc2csv(grep_file)
        return csv_file

    def lggc(self):
        self.grep_files = "*_lggc*.log"
        self.grep_v = "E 'Manual restart|Upgrade activate|Caused by restartUnit action from OMF|faultDescription: " \
                      "Application ordered restart|Power on|Data restore|Software restore|Restart ordered due to Link" \
                      " timeout' "
        self.output_file = "record_crash.txt"
        self.grep_i = grep_datetime_with_c
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.lggc2csv(grep_file)
        return csv_file

    def lgjc(self):
        self.grep_files = "*_lgjc*.log"
        self.grep_v = "'External Link Failure'"
        self.output_file = "record_alarm_history.txt"
        self.grep_i = grep_datetime_with_c
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.lgjc2csv(grep_file)
        return csv_file

    def lgoc(self):
        self.grep_files = "*_lgoc*.log"
        self.grep_v = "E 'ACT'"
        self.output_file = "record_audit.txt"
        self.grep_i = grep_datetime_with_c
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.lgoc2csv(grep_file)
        return csv_file

    def lgprc(self):
        self.grep_files = "*_lgprc*.log"
        self.grep_v = ""
        self.output_file = "record_crash_bb.txt"
        self.grep_i = grep_datetime_with_c
        grep_file = self.execute_grep()
        return grep_file

    def lguc(self):
        # lguc confirm complete
        self.grep_files = "*_lguc*.log"
        self.grep_v = ""
        self.output_file = "record_upgrade.txt"
        self.grep_i = grep_datetime_with_c + ".*'confirm complete'"
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.lguc2csv(grep_file)
        return csv_file

    def cvsw(self):
        # Current SwVersion
        self.grep_files = "*_cvcu.log"
        self.grep_i = "'Current SwVersion:'"
        self.grep_v = ""
        self.output_file = "record_sw_version.txt"
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.cvsw2csv(grep_file)
        return csv_file

    def upgrade_package(self):
        # lprswm UpgradePackage
        self.grep_files = "*_lprswm*.log"
        self.grep_i = "'UpgradePackage='"
        self.grep_v = ""
        self.output_file = "record_Package.txt"
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.up2csv(grep_file)
        return csv_file

    def st_disable(self):
        # st disable
        self.grep_files = "*_st*.log"
        self.grep_i = "'disable'"
        self.grep_v = "E '(TermPointToENB|FieldReplaceableUnit=SUP)'"
        self.output_file = "record_st_disable.txt"
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.st2csv(grep_file)
        return csv_file

    def st_cell(self):
        self.grep_files = "*_st*cell*.log"
        self.grep_i = "E ',NRCellDU=|,EUtranCellFDD=|,EUtranCellTDD='"
        self.grep_v = ""
        self.output_file = "record_st_cell.txt"
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.st2csv(grep_file)
        data = obj_data.read_csv_to_data(csv_file)
        st_cell = []
        for line in data:
            line[-1] = line[-1].split("=")[-1]
            st_cell.append(line)
        csv_file = obj_data.write_data_to_csv(st_cell, csv_file)
        return csv_file

    def st_field(self):
        self.grep_files = "*_st*field*.log"
        self.grep_i = "'FieldReplaceableUnit='"
        self.grep_v = "'FieldReplaceableUnit=SUP'"
        self.output_file = "record_st_Field.txt"
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.st2csv(grep_file)
        return csv_file

    def st_term_point_to_cn(self):
        # st TermPointToAmf and TermPointToMme
        self.grep_files = "*st*term*.log"
        self.grep_i = "E 'TermPointToAmf=|TermPointToMme='"
        self.grep_v = ""
        self.output_file = "record_st_TermPointToCN.txt"
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.st2csv(grep_file)
        return csv_file

    def st_term_point_to_x2(self):
        self.grep_files = "*st*term*.log"
        self.grep_i = "E 'TermPointToGNB=|TermPointToENB=|TermPointToENodeB=|TermPointToGNodeB='"
        self.grep_v = ""
        self.output_file = "record_st_TermPointToX2.txt"
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.st2csv(grep_file)
        return csv_file

    def pmxet_interference_pwr(self):
        # grep_pmxet_InterferencePwr
        self.grep_files = "*pmxet*.log"
        self.grep_i = "E 'EUtranCellFDD=|EUtranCellTDD=|NRCellDU='"
        self.grep_v = ""
        self.output_file = "record_pmxet_InterferencePwr.txt"
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.interference_pwr2csv(grep_file)
        return csv_file

    def hgetc_plmn_id_list(self):
        self.grep_files = "*plmnidlist.log"
        self.grep_i = "E 'NRCellDU='"
        self.grep_v = ""
        self.output_file = "record_hgetc_plmnidlist.txt"
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.plmnidlist2csv(grep_file)
        return csv_file

    def hgetc_endc_allowed_plmn_list(self):
        self.grep_files = "*endcallowedplmnlist.log"
        self.grep_i = "E 'EUtranCellFDD=|EUtranCellTDD=|NRCellDU='"
        self.grep_v = ""
        self.output_file = "record_hgetc_endcallowedplmnlist.txt"
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.plmnlist2csv(grep_file)
        return csv_file

    def hgetc_active_plmn_list(self):
        self.grep_files = "*activeplmnlist.log"
        self.grep_i = "E 'EUtranCellFDD=|EUtranCellTDD=|NRCellDU='"
        self.grep_v = ""
        self.output_file = "record_hgetc_activeplmnlist.txt"
        grep_file = self.execute_grep()
        # file to CSV
        csv_file = grep2csv.plmnlist2csv(grep_file)
        return csv_file

    def hgetc_pci(self):
        self.grep_files = "*physicallayercellid.log"
        self.grep_i = "E 'EUtranCellFDD=|EUtranCellTDD=|NRCellDU='"
        self.grep_v = ""
        self.output_file = "record_hgetc_pci.txt"
        self.execute_grep()
        self.grep_files = "*nrpci.log"
        grep_file = self.execute_grep(over_write=False)
        # file to CSV
        csv_file = grep2csv.pci2csv(grep_file)
        return csv_file

    def invxc(self):
        log2csv = obj_log2csv.Log2Csv()
        log2csv.input_path = self.log_path
        log2csv.output_path = self.output_path
        # invxc to csv files
        file_list = log2csv.invxc2csv("_invxc.log")
        return file_list

    def llogl(self):
        log2csv = obj_log2csv.Log2Csv()
        log2csv.input_path = self.log_path
        log2csv.output_path = self.output_path
        # du crash log to csv files
        csv_file = log2csv.dullogl2csv("_llogl.log")
        return csv_file

    def lll(self):
        log2csv = obj_log2csv.Log2Csv()
        log2csv.input_path = self.log_path
        log2csv.output_path = self.output_path
        # du crash log to csv files
        csv_file = log2csv.dullogl2csv("_lll.log")
        return csv_file

    def lhrullogl(self):
        log2csv = obj_log2csv.Log2Csv()
        log2csv.input_path = self.log_path
        log2csv.output_path = self.output_path
        # ru crash log to csv files
        csv_file = log2csv.rullogl2csv("_lhrullogl.log")
        # ru crash log to csv files
        return csv_file

    def scg(self):
        log2csv = obj_log2csv.Log2Csv()
        log2csv.input_path = self.log_path
        log2csv.output_path = self.output_path
        # ru crash log to csv files
        csv_file = log2csv.scg2csv("_scg.log")
        # ru crash log to csv files
        return csv_file


if __name__ == '__main__':
    # test
    log = "/home/ejungwa/hcTool/log/20201119185901"
    # log_split(log)
    out = os.path.join(log, "temp1")
    obj_file.cleanup_dir(out)
    log_process = LogProcess()
    log_process.log_path = log
    log_process.output_path = out
    # log_process.altc()
    log_process.hgetc_pci()
