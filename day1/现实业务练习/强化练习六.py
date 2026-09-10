import pandas as pd

df = pd.DataFrame([
    ["张三", "Python/Excel", "北京"],
    ["李四", "Java", "上海"],
    ["王五", "Python/SQL", "北京"],
    ["赵六", "Excel/SQL", "广州"],
    ["孙七", "Python/Java", "上海"],
    ["周八", "Python", "北京"]
], columns=["姓名", "技能", "城市"])
writer = pd.ExcelWriter("北京员工技能.xlsx")
city = df[df["城市"] == "北京"]
print(city)
l = []
for i in city["技能"]:
    for z in i.split("/"):
        print(z)
        l.append(z)
print(l)
l = set(l)
l = list(l)
print(l)
for i in l:
    city[city["技能"].str.contains(i)].to_excel(writer,sheet_name=i)
writer.close()