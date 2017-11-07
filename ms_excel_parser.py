#!/usr/bin/python2
import pyoo

class ExcelParseError(Exception):
    def __init__(self, val):
        self.value = val


def parse_specific_info(local_filepath, sheet_ind):    
    """get info for specific column"""
    dktop_obj = pyoo.LazyDesktop(your_server_ip, your_server_port)
    fd_xlses = dktop_obj.open_spreadsheet(local_filepath)
    try:
        one_sheet = fd_xlses.sheets[sheet_ind]
    except AttributeError:
        raise ExcelParseError("Specific sheet not exists or interrupted file content.")
        
    row_ind = 0
    col_ind = 2
    res = one_sheet[row_ind,col_ind].value
    if res.lower() != "ip":
        raise ExcelParseError("No found column called 'IP' or the Column must be indexed at three.") 

    res_list = []     
    max_empty = 10 #force quit if sequential ten values are empty
    while 1:
        res = one_sheet[row_ind+1,col_ind].value 
        if res.lower() != "eor" and max_empty > 0:
            #while loop termination condition
            if res != "":
                res_list.append(res)
            else:
                max_empty -= 1
            row_ind += 1
            continue
        else:
            break             
    fd_xlses.close()
    return res_list
    	

