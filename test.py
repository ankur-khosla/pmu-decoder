from ctypes import sizeof
from data_structures import LOGAB_HDR, PAYLOAD_HDR, LOGAB, PAYLOAD_HDR_SIZE, LOGAB_DATA


# input_data = "14000000D3B334010029470902000000428A143F01000000000000000005001C001E0000002C0A5F6500000000CC000000000000002C0A5F6500000000D3B33401ED000600000000B0650300E90600002C45F2000000000000000000000000CC002C0A5F65FE284709020000004F6E000005000000009B5F140000000120D3B33401000000000000000000009210190001000000428A143F0100000000000000000000000000E906000000000000000000000000000000000000010000FE0500000500000000000000001E0000007017000000000000D3B334010400080505D3B334010201FC8FAEA41E01000000000000000000000F0000000000004000000000000020040000000000000000000000000000000000000000000000000000000000000000000000000000010000"

input_data = "14000000D3B334013E274709020000003A8A143F01000000000000000005001A001E000000D6095F6500000000B800000000000000D6095F6500000000D3B33401D200060000000032610300CB160000A444F2000000000000000000000000B800D6095F653C27470902000000444200000500000000915F140000000120D3B3340100000000000000000000D79F1900010000003A8A143F0100000000000000000000000000CB160000000000000000000000000000000000000100002A0C00000500000000000000008C0A0080B01E040000000000D3B334010900080505D3B3340102020190AEA41E01000000000000000000000F0F0E000000FEFF000000000000FEFF000000000000FE1F000000000000"

hex_data = bytes.fromhex(input_data)
print(hex_data)

print("============================= PAYLOAD HEADER =============================")

pHdr = PAYLOAD_HDR.from_buffer_copy(hex_data)
print(f"system_id: {pHdr.system_id}")
print(f"business_date: {pHdr.business_date}")
print(f"activity_id: {pHdr.activity_id}")
print(f"cust_session_id: {pHdr.cust_session_id}")
print(f"enquiry_status: {pHdr.enquiry_status}")
print(f"activity_nature: {pHdr.activity_nature}")
print(f"sequence_num: {pHdr.sequence_num}")
print(f"activity_total_num: {pHdr.activity_total_num}")
print(f"extra_data_len: {pHdr.extra_data_len}")

print("============================= LOGAB HDR =============================")

log_header = LOGAB_HDR.from_buffer_copy(hex_data, PAYLOAD_HDR_SIZE + pHdr.extra_data_len)

print(f"sizew: {log_header.sizew}")
print(f"codewu: {log_header.codewu}")
print(f"errorwu: {log_header.errorwu}")
print(f"trapcodebu: {log_header.trapcodebu}")
print(f"stafflu: {log_header.stafflu}")
print(f"ltnlu: {log_header.ltnlu}")
print(f"acclu: {log_header.acclu}")
print(f"filebu: {log_header.filebu}")
print(f"blocklu: {log_header.blocklu}")
print(f"overflowlu: {log_header.overflowlu}")
print(f"offwu: {log_header.offwu}")
print(f"tranwu: {log_header.tranwu}")
print(f"timelu: {log_header.timelu}")
print(f"lgslu: {log_header.lgslu}")
print(f"msnlu: {log_header.msnlu}")
print(f"source.srcTypebu: {log_header.source.srcTypebu}")
# Check source type before accessing union fields
if log_header.source.srcTypebu == 1:  # LOGAB_SRC_VOICE
    print(f"source.data.voice.febu: {log_header.source.data.voice.febu}")
elif log_header.source.srcTypebu == 2:  # LOGAB_SRC_CIT
    print(f"source.data.did.citlu: {log_header.source.data.did.citlu}")
print(f"extSysTypebu: {log_header.extSysTypebu}")
print(f"catchup1: {log_header.catchup1}")
print(f"btexc1: {log_header.btexc1}")
print(f"othsys1: {log_header.othsys1}")
print(f"prelog1: {log_header.prelog1}")
print(f"timeout1: {log_header.timeout1}")
print(f"laterpy1: {log_header.laterpy1}")
print(f"bcsmsg1: {log_header.bcsmsg1}")
print(f"rcvmsg1: {log_header.rcvmsg1}")
print(f"overflow1: {log_header.overflow1}")
print(f"escRel1: {log_header.escRel1}")
print(f"noFlush1: {log_header.noFlush1}")
print(f"train1: {log_header.train1}")
print(f"sessionInfo1: {log_header.sessionInfo1}")
print(f"uptacc1: {log_header.uptacc1}")
print(f"anonymous1: {log_header.anonymous1}")
print(f"unused_bit: {log_header.unused_bit}")
print(f"bizdatelu: {log_header.bizdatelu}")
print(f"ticketTypewu: {log_header.ticketTypewu}")
print(f"activityIdd: {log_header.activityIdd}")
print(f"termSessIdd: {log_header.termSessIdd}")
print(f"custSessIdd: {log_header.custSessIdd}")
print(f"txnidd: {log_header.txnidd}")
print(f"txnCodewu: {log_header.txnCodewu}")
print(f"globalltnlu: {log_header.globalltnlu}")
print(f"canceltxnidd: {log_header.canceltxnidd}")


print("============================= LOGAB DATA =============================")
LOGAB_SIZE = sizeof(LOGAB)
offset = PAYLOAD_HDR_SIZE + pHdr.extra_data_len
chunk = hex_data[offset:]
chunk = chunk.ljust(LOGAB_SIZE, b'\x00')

logMsg = LOGAB.from_buffer_copy(chunk)
logData = logMsg.data

# top‐level flags
print(f"logData.bt.rac.crossSellFl: {logData.bt.rac.crossSellFl}")
print(f"logData.bt.rac.tran.bet.csctrn: {logData.bt.rac.tran.bet.csctrn}")

# header fields
print(f"logData.bt.rac.tran.bet.d.hdr.bettypebu: {logData.bt.rac.tran.bet.d.hdr.bettypebu}")
print(f"logData.bt.rac.tran.bet.d.hdr.costlu: {logData.bt.rac.tran.bet.d.hdr.costlu}")
print(f"logData.bt.rac.tran.bet.d.hdr.sellTime: {logData.bt.rac.tran.bet.d.hdr.sellTime}")
print(f"logData.bt.rac.tran.bet.d.hdr.totdu: {logData.bt.rac.tran.bet.d.hdr.totdu}")

# padding combos
print(f"logData.bt.rac.tran.bet.d.hdr.betinvcomb.flexi.flexibet: {logData.bt.rac.tran.bet.d.hdr.betinvcomb.flexi.flexibet}")
print(f"logData.bt.rac.tran.bet.d.hdr.betinvcomb.flexi.baseinv: {logData.bt.rac.tran.bet.d.hdr.betinvcomb.flexi.baseinv}")

# var.a fields
print(f"logData.bt.rac.tran.bet.d.var.a.evtbu: {logData.bt.rac.tran.bet.d.var.a.evtbu}")
print(f"logData.bt.rac.tran.bet.d.var.a.fmlbu: {logData.bt.rac.tran.bet.d.var.a.fmlbu}")
print(f"logData.bt.rac.tran.bet.d.var.a.md: {logData.bt.rac.tran.bet.d.var.a.md}")
print(f"logData.bt.rac.tran.bet.d.var.a.loc: {logData.bt.rac.tran.bet.d.var.a.loc}")
print(f"logData.bt.rac.tran.bet.d.var.a.day: {logData.bt.rac.tran.bet.d.var.a.day}")


# print(f"headerSize: {log_data.hdr.sizew}")
# print(f"sizew: {log_data.hdr.sizew}")
# print(f"codewu: {log_data.hdr.codewu}")
# print(f"errorwu: {log_data.hdr.errorwu}")
# print(f"trapcodebu: {log_data.hdr.trapcodebu}")
# print(f"stafflu: {log_data.hdr.stafflu}")
# print(f"ltnlu: {log_data.hdr.ltnlu}")
# print(f"acclu: {log_data.hdr.acclu}")
# print(f"filebu: {log_data.hdr.filebu}")
# print(f"blocklu: {log_data.hdr.blocklu}")
# print(f"overflowlu: {log_data.hdr.overflowlu}")
# print(f"offwu: {log_data.hdr.offwu}")
# print(f"tranwu: {log_data.hdr.tranwu}")
# print(f"timelu: {log_data.hdr.timelu}")
# print(f"lgslu: {log_data.hdr.lgslu}")
# print(f"msnlu: {log_data.hdr.msnlu}")
# print(f"source.srcTypebu: {log_data.hdr.source.srcTypebu}")
# # Check source type before accessing union fields
# if log_data.hdr.source.srcTypebu == 1:  # LOGAB_SRC_VOICE
#     print(f"source.data.voice.febu: {log_data.hdr.source.data.voice.febu}")
# elif log_data.hdr.source.srcTypebu == 2:  # LOGAB_SRC_CIT
#     print(f"source.data.did.citlu: {log_data.hdr.source.data.did.citlu}")
# print(f"extSysTypebu: {log_data.hdr.extSysTypebu}")
# print(f"catchup1: {log_data.hdr.catchup1}")
# print(f"btexc1: {log_data.hdr.btexc1}")
# print(f"othsys1: {log_data.hdr.othsys1}")
# print(f"prelog1: {log_data.hdr.prelog1}")
# print(f"timeout1: {log_data.hdr.timeout1}")
# print(f"laterpy1: {log_data.hdr.laterpy1}")
# print(f"bcsmsg1: {log_data.hdr.bcsmsg1}")
# print(f"rcvmsg1: {log_data.hdr.rcvmsg1}")
# print(f"overflow1: {log_data.hdr.overflow1}")
# print(f"escRel1: {log_data.hdr.escRel1}")
# print(f"noFlush1: {log_data.hdr.noFlush1}")
# print(f"train1: {log_data.hdr.train1}")
# print(f"sessionInfo1: {log_data.hdr.sessionInfo1}")
# print(f"uptacc1: {log_data.hdr.uptacc1}")
# print(f"anonymous1: {log_data.hdr.anonymous1}")
# print(f"unused_bit: {log_data.hdr.unused_bit}")
# print(f"bizdatelu: {log_data.hdr.bizdatelu}")
# print(f"ticketTypewu: {log_data.hdr.ticketTypewu}")
# print(f"activityIdd: {log_data.hdr.activityIdd}")
# print(f"termSessIdd: {log_data.hdr.termSessIdd}")
# print(f"custSessIdd: {log_data.hdr.custSessIdd}")
# print(f"txnidd: {log_data.hdr.txnidd}")
# print(f"txnCodewu: {log_data.hdr.txnCodewu}")
# print(f"globalltnlu: {log_data.hdr.globalltnlu}")
# print(f"canceltxnidd: {log_data.hdr.canceltxnidd}")

# payload_hdr_tmp = PAYLOAD_HDR()
# print(sizeof(payload_hdr_tmp))

# logheader_tmp = LOGAB_HDR()
# print(sizeof(logheader_tmp))

# logdata_tmp = LOGAB_DATA()
# print(sizeof(logdata_tmp))