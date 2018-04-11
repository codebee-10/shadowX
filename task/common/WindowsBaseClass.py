import win32pdh, string, win32api


def procids():
    # 获得 进程名，进程Id 元组的列表
    junk, instances = win32pdh.EnumObjectItems(None, None, 'process', win32pdh.PERF_DETAIL_WIZARD)
    proc_ids = []
    proc_dict = {}
    for instance in instances:
        if instance in proc_dict:
            proc_dict[instance] = proc_dict[instance] + 1
        else:
            proc_dict[instance] = 0
    for instance, max_instances in proc_dict.items():
        for inum in range(max_instances+1):
            hq = win32pdh.OpenQuery()  # initializes the query handle
            path = win32pdh.MakeCounterPath((None, 'process', instance, None, inum, 'ID Process'))
            counter_handle = win32pdh.AddCounter(hq, path)
            win32pdh.CollectQueryData(hq)  # collects data for the counter
            type, val = win32pdh.GetFormattedCounterValue(counter_handle, win32pdh.PDH_FMT_LONG)
            proc_ids.append((instance, str(val)))
            win32pdh.CloseQuery(hq)

    proc_ids.sort()
    return proc_ids


if __name__ == '__main__':
    print(procids())

