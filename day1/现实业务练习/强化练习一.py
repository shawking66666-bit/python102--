import pandas as pd

df = pd.DataFrame([
    ["张三", "Python/Excel"],
    ["李四", "Java"],
    ["王五", "Python/SQL"],
    ["赵六", "Excel/SQL"],
    ["孙七", "Python/Java"]
], columns=["姓名", "技能"])
writer =pd.ExcelWriter("员工技能.xlsx")
l=[]




for i in df["技能"]:
    for z in i.split("/"):
       # print(z)
        l.append(z)
l = set(l)
print(l)

for i in l:
    df[df["技能"].str.contains(i)].to_excel(writer,sheet_name = i)

writer.close()
