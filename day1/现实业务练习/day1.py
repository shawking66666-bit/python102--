import pandas as pd

df = pd.DataFrame(
    [
        ["张三", "销售/运营"],
        ["李四", "技术"],
        ["王五", "销售/客服"],
        ["赵六", "技术/运营"]
    ],
    columns=["姓名", "部门"]
)
adm = []
list = pd.ExcelWriter("career.xlsx")
for i in df["部门"]:
    for z in i.split("/"):
       adm.append(z)
for i in set(adm):
    df[df["部门"].str.contains(i)].to_excel(list,sheet_name=i)



list.close()

