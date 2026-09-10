#筛选出：
#部门中包含 "销售"，并且工资 >= 10000
import pandas as pd

df = pd.DataFrame([
    ["张三", "销售/运营", 12000],
    ["李四", "技术", 15000],
    ["王五", "销售/客服", 8000],
    ["赵六", "技术/运营", 18000],
    ["孙七", "销售", 16000]
], columns=["姓名", "部门", "工资"])
writer = pd.ExcelWriter("销售工资列表.xlsx")
l = []
for i in df["部门"]:
    for z in i.split("/"):
        #print(z)
        l.append(z)
l = set(l)
#print(l)
for i in l:
    results = df[df["部门"].str.contains("销售")]
    print(results)
    
    results[results["工资"] >= 10000].to_excel(writer,sheet_name="销售")
        
writer.close()
