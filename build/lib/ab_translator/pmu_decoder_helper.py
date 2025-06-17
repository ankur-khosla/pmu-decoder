from pyspark.sql.types import *
from pyspark.sql import Row
from datetime import datetime
from pyspark.sql.functions import udf
from ab_translator.extract import translate

class MessageParser:
    # Class-level constants
    header_fields = [
        "headerSystemID", "headerBusinessDate", "headerActivityID", "headerEnquiryStatus",
        "headerActivityNature", "headerErrorCode", "headerMessageCode",
    ]
    error_fields = ["is_error", "error_details"]
    value_fields = [
        "oltp_id", "msg_order_no", "selling_date", "msg_size", "msg_code", "err_code", "bcs_trap_msg_code",
        "staff_no", "logical_term_no", "acct_no", "acct_file_file_no", "acct_file_block_no", "overflow_block_no",
        "offset_to_acct_unit", "ac_tran_no", "time_stamp", "last_log_seq", "msn", "ext_req_type", "prev_txn_catch_up",
        "bt_exception", "msg_to_other_system", "pre_logon_flag", "ext_req_timeout_flag", "late_reply_flag",
        "upd_bcsmsg_flag", "upd_rcvmsg_flag", "overflow_required_flag", "cb_local_acct_release_flag",
        "no_flush_acct_release_flag", "training_acct", "acct_sess_info_append", "source_type", "front_end_no",
        "v_term_no", "v_location_id", "d_cit_no", "d_pseudo_term_no", "d_frontend_no", "cit_type", "cbbt_centre_no",
        "cbbt_window_no", "cbbt_logical_term_no", "cbbt_system_no", "old_cb_centre_no", "old_cb_window_no",
        "old_cb_channel_no", "old_cb_system_no", "pol_file_no", "pol_offset_no", "mat_no", "batch_deposit",
        "call_seq", "opt_mode", "meeting_date", "meeting_loc", "meeting_day", "ttl_pay", "unit_bet", "ttl_cost",
        "sell_time", "bet_type", "cancel_flag", "allup_event_no", "allup_formula", "allup_pool_type1",
        "allup_race_no1", "allup_banker_flag1", "allup_field_flag1", "allup_multi_flag1", "allup_multi_banker_flag1",
        "allup_random_flag1", "allup_no_of_combination1", "allup_pay_factor1", "allup_pool_type2", "allup_race_no2",
        "allup_banker_flag2", "allup_field_flag2", "allup_multi_flag2", "allup_multi_banker_flag2",
        "allup_random_flag2", "allup_no_of_combination2", "allup_pay_factor2", "allup_pool_type3", "allup_race_no3",
        "allup_banker_flag3", "allup_field_flag3", "allup_multi_flag3", "allup_multi_banker_flag3",
        "allup_random_flag3", "allup_no_of_combination3", "allup_pay_factor3", "allup_pool_type4", "allup_race_no4",
        "allup_banker_flag4", "allup_field_flag4", "allup_multi_flag4", "allup_multi_banker_flag4",
        "allup_random_flag4", "allup_no_of_combination4", "allup_pay_factor4", "allup_pool_type5", "allup_race_no5",
        "allup_banker_flag5", "allup_field_flag5", "allup_multi_flag5", "allup_multi_banker_flag5",
        "allup_random_flag5", "allup_no_of_combination5", "allup_pay_factor5", "allup_pool_type6", "allup_race_no6",
        "allup_banker_flag6", "allup_field_flag6", "allup_multi_flag6", "allup_multi_banker_flag6",
        "allup_random_flag6", "allup_no_of_combination6", "allup_pay_factor6", "race_no", "banker_flag", "field_flag",
        "multiple_flag", "multi_banker_flag", "random_flag", "sb_selection", "no_banker_bitmap1", "no_banker_bitmap2",
        "no_banker_bitmap3", "bitmap1", "bitmap2", "bitmap3", "bitmap4", "bitmap5", "bitmap6", "cross_selling_flag",
        "flexi_bet_flag", "no_of_combinations", "is_anonymous_acc", "is_csc_card",
    ]

    value_fields_cancel = ["oltp_id", "msg_order_no", "selling_date", "msg_size", "msg_code", "err_code", "bcs_trap_msg_code", "staff_no", "logical_term_no", "acct_no", "acct_file_file_no", "acct_file_block_no", "overflow_block_no", "offset_to_acct_unit", "ac_tran_no", "time_stamp", "last_log_seq", "msn", "ext_req_type", "prev_txn_catch_up", "bt_exception", "msg_to_other_system", "pre_logon_flag", "ext_req_timeout_flag", "late_reply_flag", "upd_bcsmsg_flag", "upd_rcvmsg_flag", "overflow_required_flag", "cb_local_acct_release_flag", "no_flush_acct_release_flag", "training_acct", "acct_sess_info_append", "source_type", "front_end_no", "v_term_no", "v_location_id", "d_cit_no", "d_pseudo_term_no", "d_frontend_no", "cit_type", "cbbt_centre_no", "cbbt_window_no", "cbbt_logical_term_no", "cbbt_system_no", "old_cb_centre_no", "old_cb_window_no", "old_cb_channel_no", "old_cb_system_no", "pol_file_no", "pol_offset_no", "mat_no", "batch_deposit", "call_seq", "opt_mode", "trnx_cancel", "cancel_txn_code", "acct_file_file_no2", "acct_file_block_no2", "offset_to_acct_unit2", "cancel_on_other_unit", "cancel_earlier_call", "cancel_by_tsn", "ltry_idx", "ltry_err_selection", "ltry_offset_no", "ltry_sell_src", "ltry_draw_year", "ltry_draw_no", "ltry_draw_type", "ltry_unit_bet", "ltry_ttl_cost", "meet_idx", "meet_err_race_no", "meet_err_selection", "meet_bet_offset_in_file", "meet_sell_src", "meet_date", "meet_loc", "meet_day", "meet_type", "meet_unit_bet", "meet_ttl_cost", "withdraw_amt", "withdraw_service_chrg", "withdraw_type", "withdraw_activated_by", "withdraw_src_type", "withdraw_cancel_flag", "sb_sell_src", "unit_bet", "total_cost", "sb_selling_time", "sb_bet_type", "dep_holdtime", "dep_amt", "dep_service_chrg", "dep_type", "dep_withholdable_flag", "dep_cancel_flag", "dep_reverse_flag", "dep_deposit_src", "multi_draw_flag", "no_of_draw_selected", "no_of_draw_remain", "can_prev_day_flag", "org_msg_business_date"]

    string_fields = {
        "headerBusinessDate", "oltp_id", "v_term_no", "cit_type", "mat_no", "meeting_loc", "meeting_day", "bet_type", "cancel_flag",
        "allup_formula", "allup_pool_type1", "allup_race_no1", "allup_pool_type2", "allup_race_no2",
        "allup_pool_type3", "allup_race_no3", "allup_pool_type4", "allup_race_no4", "allup_pool_type5",
        "allup_race_no5", "allup_pool_type6", "allup_race_no6", "race_no", "sb_selection", "bitmap1", "bitmap2",
        "bitmap3", "bitmap4", "bitmap5", "bitmap6"
    }

    timestamp_fields = {
        "selling_date", "time_stamp", "meeting_date", "sell_time", "meet_date", "sb_selling_time", "dep_holdtime", "org_msg_business_date"
    }

    decimal_fields = {
        "ttl_pay", "ttl_cost", "allup_pay_factor1", "allup_pay_factor2", "allup_pay_factor3", "allup_pay_factor4",
        "allup_pay_factor5", "allup_pay_factor6", "ltry_unit_bet", "ltry_ttl_cost", "meet_unit_bet", "meet_ttl_cost", "withdraw_amt", "withdraw_service_chrg", "total_cost", "dep_amt", "dep_service_chrg"
    }

    @staticmethod
    def safe_cast_string(val):
        if val is None:
            return None
        v = val.strip()
        return v if v else None

    @staticmethod
    def safe_cast_long(val):
        try:
            if val is None or val.strip() in ["", "~|~"]:
                return None
            return int(val)
        except:
            return None

    @staticmethod
    def safe_cast_decimal(val):
        try:
            if val is None or val.strip() in ["", "~|~"]:
                return None
            return float(val)
        except:
            return None

    @staticmethod
    def safe_cast_timestamp(val):
        if val is None:
            return None
        val = val.strip()
        if val in ["", "~|~"]:
            return None
        for fmt in ("%d-%b-%Y", "%d-%b-%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(val, fmt)
            except:
                continue
        return None

    @staticmethod
    def translate_message_pmu(message):
        try:
            decoded_message = translate(message)
            return (decoded_message, False, None)
        except Exception as e:
            return ("@|@", True, str(e))
    
    @classmethod
    def parse(cls, message: str, is_cancel: bool = False) -> Row:
        decoded_message_tuple = cls.translate_message_pmu(message)
        errors = [decoded_message_tuple[1], decoded_message_tuple[2]]
        parts = decoded_message_tuple[0].split("@|@")
        header_values = parts[:7] + [None] * (7 - len(parts)) if len(parts) < 7 else parts[:7]
        value_string = "@|@".join(parts[7:]) if len(parts) > 7 else ""
        value_values = value_string.split("~|~") if value_string else []
        value_flds = cls.value_fields if not is_cancel else cls.value_fields_cancel

        # Cast headers
        header_casted = [
            cls.safe_cast_long(header_values[0]),
            cls.safe_cast_string(header_values[1]),
            cls.safe_cast_long(header_values[2]),
            cls.safe_cast_long(header_values[3]),
            cls.safe_cast_long(header_values[4]),
            cls.safe_cast_long(header_values[5]),
            cls.safe_cast_long(header_values[6]),
        ]

        casted_values = []
        for i, field in enumerate(value_flds):
            val = value_values[i] if i < len(value_values) else None
            if field in cls.string_fields:
                casted_values.append(cls.safe_cast_string(val))
            elif field in cls.timestamp_fields:
                casted_values.append(cls.safe_cast_timestamp(val))
            elif field in cls.decimal_fields:
                casted_values.append(cls.safe_cast_decimal(val))
            else:
                casted_values.append(cls.safe_cast_long(val))

        while len(casted_values) < len(value_flds):
            casted_values.append(None)

        return Row(
            headerFields=dict(zip(cls.header_fields, header_casted)),
            errorFields=dict(zip(cls.error_fields, errors)),
            valueFields=dict(zip(cls.value_fields, casted_values))
        )

    @classmethod
    def get_udf(cls, is_cancel: bool = False):
        # Create schema for header
        header_struct = StructType([
            StructField(name, StringType() if name in cls.string_fields else LongType(), True)
            for name in cls.header_fields
        ])
        value_flds = cls.value_fields if not is_cancel else cls.value_fields_cancel
        value_struct_fields = []
        for name in value_flds:
            if name in cls.string_fields:
                value_struct_fields.append(StructField(name, StringType(), True))
            elif name in cls.timestamp_fields:
                value_struct_fields.append(StructField(name, TimestampType(), True))
            elif name in cls.decimal_fields:
                value_struct_fields.append(StructField(name, DoubleType(), True))
            else:
                value_struct_fields.append(StructField(name, LongType(), True))
        errors = StructType([
            StructField("is_error", BooleanType(), nullable=False),
            StructField("error_details", StringType(), nullable=True)
        ])

        full_schema = StructType([
            StructField("headerFields", header_struct, True),
            StructField("errors", errors, True),
            StructField("valueFields", StructType(value_struct_fields), True),
        ])

        return udf(cls.parse, full_schema)