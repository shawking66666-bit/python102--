import pandas as pd
df = pd.DataFrame(
    [
        ["2021","韩国/中国","北京"],
        ["2018","法国/美国","华盛顿"],
        ["2025","新加坡/印度","悉尼"],
        ["2023","法国","巴黎"]
    ],
    index=["a","b","c","d"],
    columns=["年份","国家","城市"]
)

list = pd.ExcelWriter("type.xlsx")
county = []
#df["year"] = df["年份"].apply(lambda x:x.split("/")[0].strip())
df["c"] = df["国家"].apply(lambda x:x.split("/")[0].strip())

#for i in df["国家"].unique():
    #df[df["国家"]==i].to_excel(list,sheet_name=i)
print(df["c"])
#list.close()