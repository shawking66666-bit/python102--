import pandas as pd
df = pd.DataFrame(
    {
        "年份": [2023, 2024, 2025],
        "国家": ["c/中国", "a/美国", "u/英国"],
    },
    index = ["A", "B", "C"]
)
df["c"]=df["国家"].apply(lambda x: x.split('/')[1].strip())

#x=df["国家"].str.contains("中国")

print(df)