import pandas as pd
df = pd.DataFrame(
    [
        ["2023","美国/新加坡"],
        ["2024","中国/韩国"],
        ["2025","日本/德国"],
        ["2026","中国/法国"]
    ],
    index=["a","b","c","d"],
    columns=["年份","国家"]
)

temp = pd.ExcelWriter("temp.xlsx")
df.to_excel(temp,sheet_name="sheet1")
country = []
#for i in df["国家"].str.contains("中国"):
for i in df["国家"]:
   for z in i.split("/"):
      country.append(z)
for i in set(country):
   df[df["国家"].str.contains(i)].to_excel(temp,sheet_name= i)
   print(i)
temp.close()
#print(df[x])


#print(df[["年份","国家"]])


#print(type(df["年份"]))
#print(type(df[["年份","国家"]]))
#print(df[[True,True,True]])

