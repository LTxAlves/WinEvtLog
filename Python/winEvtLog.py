from multiprocessing import connection
from matplotlib.pyplot import connect
import win32evtlog
import pyodbc

def DBConnect():
    # Some other example server values are
    # server = 'localhost\sqlexpress' # for a named instance
    # server = 'myserver,port' # to specify an alternate port
    server = 'tcp:myserver.database.windows.net'
    database = 'mydb'
    username = 'myusername'
    password = 'mypassword'

    # connect to SQL Server
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn


def DBStoreEntry(conn: pyodbc.Connection, event):
    cursor = conn.cursor()

    # sample insert query
    count = cursor.execute("""
    INSERT INTO schema.table (category, timeStamp, Source, EventID, EventType, EventData)) 
    VALUES (?,?,?,?,?,?))""",
    event.EventCategory, event.TimeGenerated, event.SourceName, event.EventID, event.EventType, str(event.StringInserts)).rowcount
    conn.commit()
    print('Rows inserted: ' + str(count))

def GetAllEventLogs():
    server = 'localhost' # name of the target computer to get event logs
    logtype = 'System' # type of event log to get (System, Application, Security, or Setup)
    hand = win32evtlog.OpenEventLog(server, logtype)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ

    eventTypes = {1: 'Error', 2: 'Warning', 4: 'Information'}

    # cnxn = DBConnect()

    # keep reading event logs until we've read them all
    while True:
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if events:
            for event in events:
                if event.EventType == win32evtlog.EVENTLOG_WARNING_TYPE or event.EventType == win32evtlog.EVENTLOG_ERROR_TYPE: # get only desired event types
                    # DBStoreEntry(cnxn, event) # store event in database
                    print(f'Event Category: {event.EventCategory}')
                    print(f'\tTime Generated: {event.TimeGenerated}')
                    print(f'\tSource Name: {event.SourceName}')
                    print(f'\tEvent ID: {event.EventID}')
                    print(f'\tEvent Type: {eventTypes[event.EventType]}')
                    data = event.StringInserts
                    if data:
                        print('\tEvent Data:')
                        for msg in data:
                            if msg:
                                print('\t\t' + msg)
        else:
            break

if __name__ == '__main__':
    GetAllEventLogs()

# import sys
# import pywintypes
# import win32evtlog

# INFINITE = 0xFFFFFFFF
# EVTLOG_READ_BUF_LEN_MAX = 0x7FFFF


# def get_record_data(eventlog_record):
#     ret = dict()
#     for key in dir(eventlog_record):
#         if 'A' < key[0] < 'Z':
#             ret[key] = getattr(eventlog_record, key)
#     return ret


# def get_eventlogs(source_name="Application", buf_size=EVTLOG_READ_BUF_LEN_MAX, backwards=True):
#     ret = list()
#     evt_log = win32evtlog.OpenEventLog(None, source_name)
#     read_flags = win32evtlog.EVENTLOG_SEQUENTIAL_READ
#     if backwards:
#         read_flags |= win32evtlog.EVENTLOG_BACKWARDS_READ
#     else:
#         read_flags |= win32evtlog.EVENTLOG_FORWARDS_READ
#     offset = 0
#     eventlog_records = win32evtlog.ReadEventLog(evt_log, read_flags, offset, buf_size)
#     while eventlog_records:
#         ret.extend(eventlog_records)
#         offset += len(eventlog_records)
#         eventlog_records = win32evtlog.ReadEventLog(evt_log, read_flags, offset, buf_size)
#     win32evtlog.CloseEventLog(evt_log)
#     return ret


# def get_events_xmls(channel_name="Application", events_batch_num=100, backwards=True):
#     ret = list()
#     flags = win32evtlog.EvtQueryChannelPath
#     if backwards:
#         flags |= win32evtlog.EvtQueryReverseDirection
#     try:
#         query_results = win32evtlog.EvtQuery(channel_name, flags, None, None)
#     except pywintypes.error as e:
#         print(e)
#         return ret
#     events = win32evtlog.EvtNext(query_results, events_batch_num, INFINITE, 0)
#     while events:
#         for event in events:
#             ret.append(win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml))
#         events = win32evtlog.EvtNext(query_results, events_batch_num, INFINITE, 0)
#     return ret


# def main():
#     import sys, os
#     from collections import OrderedDict
#     standard_log_names = ["Application", "System", "Security"]
#     source_channel_dict = OrderedDict()

#     for item in standard_log_names:
#         source_channel_dict[item] = item

#     for item in ["Windows Powershell"]: # !!! This works on my machine (96 events)
#         source_channel_dict[item] = item

#     for source, channel in source_channel_dict.items():
#         print(source, channel)
#         logs = get_eventlogs(source_name=source)
#         xmls = get_events_xmls(channel_name=channel)
#         print("\n", get_record_data(logs[0]))
#         print(xmls[0])
#         print("\n", get_record_data(logs[-1]))
#         print(xmls[-1])
#         print(len(logs))
#         print(len(xmls))

# if __name__ == "__main__":
#     print("Python {:s} on {:s}\n".format(sys.version, sys.platform))
#     main()