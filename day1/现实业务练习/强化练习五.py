#解决 contains() 的误匹配
import pandas as pd

df = pd.DataFrame([
    ["商品A", "手机/数码"],
    ["商品B", "手机"],
    ["商品C", "电脑/数码"],
    ["商品D", "电脑"],
    ["商品E", "手机壳"]
], columns=["商品", "类别"])
writer = pd.ExcelWriter("商品类别.xlsx")
l = []
for i in df["类别"]:
    for z in i.split("/"):
        l.append(z)
l = set(l)
l = list(l)
#print(l)
for i in l:
    rows = []
    for index in df.index:
        x = df.loc[index,"类别"]
        if "手机" in x:
            rows.append(index)
result = df.loc[rows]
result.to_excel(writer, sheet_name=i, index=False)

writer.close()