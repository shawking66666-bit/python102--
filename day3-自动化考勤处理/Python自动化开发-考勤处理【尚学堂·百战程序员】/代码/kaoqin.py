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
import xlrd     # pip install xlrd 操作excel的工具
def rans(num):  # 判断有多少违规记录
    t_rs = [0,0,0,0]  # 迟到5分  迟到10分 只打一次卡 旷工
    for j in range(1,32):
        t = sheet.cell_value(num,j)
        all_time = t.split('\n') if len(t) !=0 else []
        count = len(all_time)
        # print(all_time)
        if count == 0 : # 没有打卡
            t_rs[3] += 1 # 记录一次旷工
        else: # 已经打卡
            start = all_time[0]
            t_start = tranforms(start)
            if count == 1: #只打了一次卡
                t_rs[2] +=1 # 记录一次只打一次卡
                c = compare_time(t_start)
            else:  # 打了多次卡
                end = all_time[-1]
                t_end = tranforms(end)
                if t_end[0]- t_start[0] < 4:
                    t_rs[2] +=1 # 记录一次只打一次卡
                    if t_end[0] < 12: # 判断多次打卡是不是上午 
                        c = compare_time(t_start)
                    else:
                        c = compare_time(t_end)
                    statistics(c,t_rs)
                else:
                    a = compare_time(t_start)
                    p = compare_time(t_end)
                    statistics(a,t_rs)
                    statistics(p,t_rs)
    return t_rs
def statistics(c,t_rs):
    if c > 5 and c < 10:
        t_rs[0] += 1
    elif c>= 10:
        t_rs[1] +=1
def tranforms(tmp_time): # 处理时间
    hour,minute = tmp_time.split(':')
    sum_minute = int(hour)*60 +int(minute)
    return [int(hour),int(minute),sum_minute]
def compare_time(tmp_time): # 判断是否有迟到或早退
    if tmp_time[0] < 12: # 签到
        c = tmp_time[2] - 9*60
    else: # 签退
        c = 18*60 - tmp_time[2]
    return c if c > 0 else 0
# 读取数据
if __name__ == "__main__":
    excel = xlrd.open_workbook('kq.xlsx')
    sheet = excel.sheets()[0]
    for i in range(1,sheet.nrows):
        # print(sheet.cell_value(i,0))
        one_rs = rans(i)
        print({'姓名':sheet.cell_value(i,0),'迟到5分钟':one_rs[0],'迟到10分钟':one_rs[1],'只打一次卡':one_rs[2],'旷工':one_rs[3]})
