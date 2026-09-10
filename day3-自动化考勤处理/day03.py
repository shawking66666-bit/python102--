'''
迟到 早退： 
    5 < time > 10 20
    10 < time 50
只一次卡
    扣 20
不打卡
    扣1.5
调休
    当月天数够，不扣，不够扣1.5
'''
import xlrd

def rans(num):
    t_rs = [0,0,0,0]# 迟到5分  迟到10分 只打一次卡 旷工
    t = sheet.cell_value(0,1)
    all_time = t.split('\n') if len(t) != 0 else []
    count = len(all_time) 
    if count == 0:
        t_rs[3] += 1
    else:
        start = all_time[0]
        t_start = transforms(start)
        if count == 1:
            t_rs[2] += 1
            c = compare_time(t_start)
        else:
            pass

def statistics(c,t_rs):
    if c > 5 and c < 10:
        t_rs[0] += 1
    elif c >= 10:
        t_rs[1] += 1

def transforms(temp_time):
    hour,minute = temp_time.split(":")
    sum_minute = int(hour)*60 + int(minute)
    return[int(hour),int(minute),sum_minute]

def compare_time(temp_time):
    if temp_time[0] < 12:
        c = temp_time[2] - 9*60
    else:
        c = 18*60 - temp_time[2]
    return c if c > 0 else 0



if __name__ == "__main__":
    excel = xlrd.open_workbok('kq.xlsx')
    sheet = excel.sheet()[0]

    one_rs = rans(1)