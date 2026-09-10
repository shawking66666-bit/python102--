import pandas as pd

df = pd.DataFrame([
    ["张三", "销售/运营"],
    ["李四", "技术"],
    ["王五", "销售/客服"],
    ["赵六", "技术/运营"],
    ["孙七", "销售"],
    ["周八", "法务"]
], columns=["姓名", "部门"])
#print(df)
writer = pd.ExcelWriter("部门列表.xlsx")
adm = []
for i in df["部门"]:
    for z in i.split("/"):
        #print(z)
        adm.append(z)
adm = set(adm)      
#print(adm)
for i in adm:
    results = df[df["部门"].str.contains(i)]
    if len(results) >= 2:
        results.to_excel(writer,sheet_name=i)

writer.close()
