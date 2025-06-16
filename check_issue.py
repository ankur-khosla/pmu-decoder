from ab_translator.extract import translate
from ab_translator.data_structures import LOGAB_ACA, LOGAB_ACA_DEV, LOGAB_ACA_DATA, LOGAB_SOURCE, LOGAB_ACA_NORMAL, ACU_TRAN_ACA, ACU_BANKACCNUM  
from ctypes import sizeof

header_fields = [
    "headerSystemID",
    "headerBusinessDate",
    "headerActivityID",
    "headerEnquiryStatus",
    "headerActivityNature",
    "headerErrorCode",
    "headerMessageCode"
]

value_fields = [
    "oltp_id",
    "msg_order_no",
    "selling_date",
    "msg_size",
    "msg_code",
    "err_code",
    "bcs_trap_msg_code",
    "staff_no",
    "logical_term_no",
    "acct_no",
    "acct_file_file_no",
    "acct_file_block_no",
    "overflow_block_no",
    "offset_to_acct_unit",
    "ac_tran_no",
    "time_stamp",
    "last_log_seq",
    "msn",
    "ext_req_type",
    "prev_txn_catch_up",
    "bt_exception",
    "msg_to_other_system",
    "pre_logon_flag",
    "ext_req_timeout_flag",
    "late_reply_flag",
    "upd_bcsmsg_flag",
    "upd_rcvmsg_flag",
    "overflow_required_flag",
    "cb_local_acct_release_flag",
    "no_flush_acct_release_flag",
    "training_acct",
    "acct_sess_info_append",
    "source_type",
    "front_end_no",
    "v_term_no",
    "v_location_id",
    "d_cit_no",
    "d_pseudo_term_no",
    "d_frontend_no",
    "cit_type",
    "cbbt_centre_no",
    "cbbt_window_no",
    "cbbt_logical_term_no",
    "cbbt_system_no",
    "old_cb_centre_no",
    "old_cb_window_no",
    "old_cb_channel_no",
    "old_cb_system_no",
    "pol_file_no",
    "pol_offset_no",
    "mat_no",
    "batch_deposit",
    "call_seq",
    "opt_mode",
    "meeting_date",
    "meeting_loc",
    "meeting_day",
    "ttl_pay",
    "unit_bet",
    "ttl_cost",
    "sell_time",
    "bet_type",
    "cancel_flag",
    "allup_event_no",
    "allup_formula",
    "allup_pool_type1",
    "allup_race_no1",
    "allup_banker_flag1",
    "allup_field_flag1",
    "allup_multi_flag1",
    "allup_multi_banker_flag1",
    "allup_random_flag1",
    "allup_no_of_combination1",
    "allup_pay_factor1",
    "allup_pool_type2",
    "allup_race_no2",
    "allup_banker_flag2",
    "allup_field_flag2",
    "allup_multi_flag2",
    "allup_multi_banker_flag2",
    "allup_random_flag2",
    "allup_no_of_combination2",
    "allup_pay_factor2",
    "allup_pool_type3",
    "allup_race_no3",
    "allup_banker_flag3",
    "allup_field_flag3",
    "allup_multi_flag3",
    "allup_multi_banker_flag3",
    "allup_random_flag3",
    "allup_no_of_combination3",
    "allup_pay_factor3",
    "allup_pool_type4",
    "allup_race_no4",
    "allup_banker_flag4",
    "allup_field_flag4",
    "allup_multi_flag4",
    "allup_multi_banker_flag4",
    "allup_random_flag4",
    "allup_no_of_combination4",
    "allup_pay_factor4",
    "allup_pool_type5",
    "allup_race_no5",
    "allup_banker_flag5",
    "allup_field_flag5",
    "allup_multi_flag5",
    "allup_multi_banker_flag5",
    "allup_random_flag5",
    "allup_no_of_combination5",
    "allup_pay_factor5",
    "allup_pool_type6",
    "allup_race_no6",
    "allup_banker_flag6",
    "allup_field_flag6",
    "allup_multi_flag6",
    "allup_multi_banker_flag6",
    "allup_random_flag6",
    "allup_no_of_combination6",
    "allup_pay_factor6",
    "race_no",
    "banker_flag",
    "field_flag",
    "multiple_flag",
    "multi_banker_flag",
    "random_flag",
    "sb_selection",
    "no_banker_bitmap1",
    "no_banker_bitmap2",
    "no_banker_bitmap3",
    "bitmap1",
    "bitmap2",
    "bitmap3",
    "bitmap4",
    "bitmap5",
    "bitmap6",
    "cross_selling_flag",
    "flexi_bet_flag",
    "no_of_combinations",
    "is_anonymous_acc",
    "is_csc_card"
]


def compare_records(msg1: str, msg2: str):
    # 1. Split off headers
    h1 = msg1.split('@|@')
    h2 = msg2.split('@|@')
    vals1 = '@|@'.join(h1[len(header_fields):])
    vals2 = '@|@'.join(h2[len(header_fields):])
    # 2. Split payloads
    v1 = vals1.split('~|~')
    v2 = vals2.split('~|~')
    # 3. Find differences
    diffs = []
    for idx, (a, b) in enumerate(zip(v1, v2)):
        if a != b:
            diffs.append((value_fields[idx], a, b))
    return diffs


# expted_str = "20@|@20231123@|@8745594560@|@0@|@0@|@0@|@6@|@ACP01~|~0~|~23-Nov-2023~|~226~|~6~|~0~|~0~|~0~|~6853~|~10058801~|~0~|~0~|~0~|~0~|~532~|~23-Nov-2023 16:21:13~|~155659915~|~59~|~0~|~1~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~4~|~0~|~~|~0~|~0~|~0~|~0~|~~|~884~|~21~|~2~|~19~|~884~|~21~|~2~|~19~|~0~|~0~|~~|~0~|~5353278046~|~2~|~2023-11-23 00:00:00~|~6~|~5~|~0~|~10000~|~2400~|~23-Nov-2023 16:21:13~|~QTT~|~ ~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~1~|~0~|~0~|~1~|~0~|~1~|~1*01+03+10+13M~|~0~|~0~|~0~|~240A~|~0000~|~0000~|~0000~|~0000~|~0000~|~0~|~1~|~24~|~0~|~0"
# outout_str = "20@|@20231123@|@8745594560@|@0@|@0@|@0@|@6@|@ACP01~|~0~|~23-Nov-2023~|~226~|~6~|~0~|~0~|~0~|~6853~|~10058801~|~0~|~0~|~0~|~0~|~532~|~23-Nov-2023 16:21:13~|~155659915~|~59~|~0~|~1~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~4~|~0~|~~|~0~|~0~|~0~|~0~|~~|~884~|~21~|~2~|~19~|~884~|~21~|~2~|~19~|~0~|~0~|~~|~0~|~5353278046~|~0~|~2023-11-23 00:00:00~|~6~|~5~|~0~|~10000~|~2400~|~23-Nov-2023 16:21:13~|~QTT~|~ ~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~1~|~0~|~0~|~1~|~0~|~1~|~1*01+03+10+13M~|~0~|~0~|~0~|~240A~|~0000~|~0000~|~0000~|~0000~|~0000~|~0~|~1~|~24~|~0~|~0"

input_data = "14000000DC7A33018B1A4DB3000000000F6C0800000000000000000000010001001200000039BE105600000000011B0000000000004601080000002100000000CE000000704E99000000000000000000000000011B39BE10568A1A4DB3000000000600000013710300001600010001004120DC7A33010000000000000000000000000000000000000F6C08000000000071935D25000000000000CE0000000000000000000000FE1A270000000000000000000000000000000080FB0F560771935D25000000008108000000000000000000000100008108000013000000000000000032000000B8880000ABBD1056DC7A33011201080201DC7A33010306022200267432FD0B01000000000000000000000C02000000000000000400000000000000010000000000050D00517532FD0B01000000000000000000000C4C000000000000000000000000000000010000000000080300737632FD0B01000000000000000000000830000000000000000000000000000000010000000000"
expted_str = "20@|@20151004@|@3008174731@|@0@|@0@|@0@|@8@|@ACP01~|~0~|~04-Oct-2015~|~326~|~8~|~0~|~33~|~0~|~206~|~10047088~|~0~|~0~|~0~|~0~|~6913~|~04-Oct-2015 13:50:49~|~2147483647~|~6~|~0~|~1~|~0~|~0~|~0~|~0~|~0~|~1~|~0~|~0~|~0~|~0~|~0~|~0~|~19~|~0~|~~|~0~|~0~|~0~|~0~|~~|~881~|~22~|~1~|~1~|~881~|~22~|~1~|~1~|~0~|~0~|~~|~0~|~551951~|~0~|~6910~|~39~|~0~|~0~|~0~|~1~|~1~|~1~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~19~|~2015-10-04 00:00:00~|~0~|~1~|~18~|~50~|~35000~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~~|~0~|~~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~4-Oct-2015"
output_str = translate(input_data)

diffs = compare_records(expted_str, output_str)
for field, val1, val2 in diffs:
    print(f"{field}: '{val1}' ≠ '{val2}'")

print(expted_str)
print(output_str)

