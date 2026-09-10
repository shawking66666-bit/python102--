#忽略“未知”并按国家拆 Sheet
import pandas as pd

df = pd.DataFrame([
    ["A公司", "中国/日本"],
    ["B公司", "美国"],
    ["C公司", "未知"],
    ["D公司", "中国/韩国"],
    ["E公司", "日本/美国"]
], columns=["公司", "国家"])
writer = pd.ExcelWriter("国家.xlsx")
l = []
for i in df["国家"]:
    for z in i.split("/"):
        #print(z)
        l.append(z)
l = set(l)
l = list(l)
print(l)
for i in l:
        if i == "未知":
             continue
        df[df["国家"].str.contains(i)].to_excel(writer,sheet_name = i)
writer.close()
    

