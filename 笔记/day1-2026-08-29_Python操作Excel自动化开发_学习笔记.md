---
type: knowledge
status: confirmed
area: Programming
source: file-verified
confidence: confirmed
privacy: private
created: 2026-08-29
updated: 2026-08-30
tags: [Python, pandas, Excel, DataFrame, Series, ExcelWriter, 自动化开发, 长期复习]
---

# Python操作Excel自动化开发｜学习笔记

## 0. 本节课真正的主线

本节课不是以 `openpyxl` 为主，而是用 `pandas` 完成“构造数据 → 分析/拆分数据 → 导出 Excel”的自动化流程。

核心链路：

```text
Python 数据
    ↓
pandas.DataFrame
    ↓
选择列 / 字符串处理 / 条件筛选 / 去重
    ↓
ExcelWriter + DataFrame.to_excel()
    ↓
一个原始表 + 多个分类工作表
```

本笔记依据今天 E 盘的练习文件整理：

- `E:\测试.py`：完整练习，创建 DataFrame，拆分“国家”字段，并按国家导出多个工作表。
- `E:\测试2.py`：练习字典创建 DataFrame、`apply(lambda)` 和字符串 `split`。
- `E:\自写.py`：独立改写练习，并暴露出 `ExcelWriter` 未关闭的问题。
- `E:\Untitled-1.py`：练习 `range()`、`len()` 和字符串按下标取字符。
- `E:\temp.xlsx`：`测试.py` 生成的 Excel 结果文件。
- `E:\type.xlsx`：当前为 0 字节，说明 `ExcelWriter` 尚未正确关闭或保存。

## 1. DataFrame：表格数据的核心对象

`DataFrame` 可以理解为 Python 中的二维表格，包含行、列和数据。

### 1.1 用二维列表创建

```python
import pandas as pd

df = pd.DataFrame(
    [
        ["2023", "美国/新加坡"],
        ["2024", "中国/韩国"],
        ["2025", "日本/德国"],
        ["2026", "中国/法国"],
    ],
    index=["a", "b", "c", "d"],
    columns=["年份", "国家"],
)
```

- 外层列表代表多行。
- 每个内层列表代表一行。
- `index` 指定行标签。
- `columns` 指定列名。
- 每一行的数据数量必须和列数量对应。

### 1.2 用字典创建

```python
df = pd.DataFrame(
    {
        "年份": [2023, 2024, 2025],
        "国家": ["c/中国", "a/美国", "u/英国"],
    },
    index=["A", "B", "C"],
)
```

字典的键是列名，值是整列数据。不同列的列表长度应保持一致。

## 2. 选择 Series 和 DataFrame

```python
df["年份"]
```

选择单列，返回 `Series`，相当于一维数据。

```python
df[["年份", "国家"]]
```

选择多列，返回 `DataFrame`，注意外层必须是双中括号。

```python
print(type(df["年份"]))
print(type(df[["年份", "国家"]]))
```

按条件筛选行：

```python
result = df[df["国家"].str.contains("中国")]
```

含义是：先判断“国家”列每一行是否包含“中国”，得到一组布尔值，再用这组布尔值筛选原表。

如果搜索内容是普通文本而不是正则表达式，建议写得更明确：

```python
result = df[df["国家"].str.contains("中国", regex=False, na=False)]
```

## 3. 字符串拆分：`split()`

今天的数据使用 `/` 分隔多个国家，例如：

```text
中国/韩国
```

字符串的 `split()` 会把一个字符串拆成列表：

```python
text = "中国/韩国"
print(text.split("/"))
# ['中国', '韩国']
```

取拆分后的第一个元素：

```python
print(text.split("/")[0])
# 中国
```

取拆分后的第二个元素：

```python
print(text.split("/")[1])
# 韩国
```

去除前后空格：

```python
print(text.split("/")[0].strip())
```

注意：下标从 `0` 开始。`split("/")[1]` 要求字符串确实包含 `/`，否则会产生 `IndexError`。

## 4. `apply()` 和 `lambda`：逐个处理一列

`apply()` 可以把一个函数应用到 Series 的每个元素。

```python
df["国家"].apply(lambda x: x.split("/")[1].strip())
```

逐步理解：

1. `df["国家"]` 取出“国家”这一列。
2. `apply()` 逐行取出该列中的一个单元格，放入变量 `x`。
3. `lambda x: ...` 对每个 `x` 执行同样的处理。
4. `x.split("/")[1]` 取 `/` 后面的国家。
5. `.strip()` 清理前后空格。

把处理结果保存为新列：

```python
df["国家2"] = df["国家"].apply(
    lambda x: x.split("/")[1].strip()
)
```

课堂中 `测试2.py` 的核心写法就是这个模式。

### 4.1 更稳妥的写法

如果某些单元格可能没有 `/`，不要直接使用 `[1]`：

```python
def get_second_country(value):
    if not isinstance(value, str):
        return None
    parts = [part.strip() for part in value.split("/")]
    return parts[1] if len(parts) > 1 else parts[0]


df["国家2"] = df["国家"].apply(get_second_country)
```

如果目标是拆成多列，`str.split(..., expand=True)` 更适合：

```python
countries = df["国家"].str.split("/", n=1, expand=True)
df["国家1"] = countries[0].str.strip()
df["国家2"] = countries[1].str.strip()
```

## 5. 用循环收集所有国家并去重

`测试.py` 中“国家”列每个单元格可能包含两个国家，因此需要两层循环：

```python
country = []

for value in df["国家"]:
    for item in value.split("/"):
        country.append(item.strip())
```

此时 `country` 可能是：

```python
["美国", "新加坡", "中国", "韩国", "日本", "德国", "中国", "法国"]
```

用 `set()` 去重：

```python
unique_countries = set(country)
```

`set` 的特点是元素不重复，但不保证原始顺序。如果希望保持首次出现顺序：

```python
unique_countries = list(dict.fromkeys(country))
```

注意：`df["国家"].unique()` 只能对完整单元格去重，例如“美国/新加坡”和“中国/韩国”是不同字符串，不能直接得到拆分后的单个国家。

## 6. 按国家筛选并导出多个工作表

基本导出逻辑：

```python
import pandas as pd

writer = pd.ExcelWriter("temp.xlsx")

df.to_excel(writer, sheet_name="sheet1")

for country_name in unique_countries:
    result = df[df["国家"].str.contains(country_name, regex=False, na=False)]
    result.to_excel(writer, sheet_name=country_name)

writer.close()
```

输出结果是：

- `sheet1`：完整原始数据。
- 每个国家一个工作表：只保留“国家”字段中包含该国家的行。

例如“中国”工作表会包含“韩国/中国”和“中国/法国”两行。

### 6.1 推荐使用上下文管理器

比手动 `close()` 更推荐：

```python
with pd.ExcelWriter("temp.xlsx") as writer:
    df.to_excel(writer, sheet_name="sheet1", index=False)

    for country_name in unique_countries:
        result = df[
            df["国家"].str.contains(
                country_name,
                regex=False,
                na=False,
            )
        ]
        result.to_excel(
            writer,
            sheet_name=country_name,
            index=False,
        )
```

离开 `with` 代码块时，写入器会自动完成保存和关闭，避免出现 `type.xlsx` 0 字节的问题。

### 6.2 `unique() + ==` 和 `contains()` 的选择

这两个写法解决的不是同一个问题：

| 写法 | 判断内容 | 适用数据 |
|---|---|---|
| `df["国家"] == i` | 整个单元格是否完全等于 `i` | 每个单元格只有一个国家 |
| `df["国家"].str.contains(i)` | 单元格文本中是否出现 `i` | 一个单元格可能有多个国家 |
| `df["国家"].unique()` | 这一列出现过哪些不重复的完整值 | 直接得到分类值，不负责拆分 |

单一国家数据可以直接套用“按年份拆分”的教程写法：

```python
for country_name in df["国家"].unique():
    result = df[df["国家"] == country_name]
    result.to_excel(writer, sheet_name=country_name)
```

例如单元格是 `"中国"`，`== "中国"` 能匹配；但单元格是 `"中国/日本"` 时，`== "中国"` 为 `False`，这时应使用 `contains()`：

```python
for country_name in ["中国", "美国", "日本"]:
    mask = df["国家"].str.contains(country_name, na=False)
    df[mask].to_excel(writer, sheet_name=country_name)
```

### 6.3 `contains()` 返回条件，`df[mask]` 才负责筛选

```python
mask = df["国家"].str.contains("中国", na=False)
result = df[mask]
```

执行结果可以分成两步：

```text
str.contains("中国") → True / False 的布尔 Series
df[mask]              → 保留 True 对应的行
```

因此下面这种写法逻辑错误：

```python
for i in df["国家"].str.contains("中国"):
    ...
```

这里的 `i` 依次是 `True`、`False`，不是国家名称。若写成 `for i in df[mask]`，遍历 DataFrame 默认拿到的是列名，也不是行数据。

## 7. `to_excel()` 的关键参数

```python
df.to_excel(
    writer,
    sheet_name="sheet1",
    index=False,
)
```

- 第一个参数：Excel 写入器或文件路径。
- `sheet_name`：工作表名称。
- `index=False`：不把 DataFrame 的行索引额外写入 Excel。

今天的 `测试.py` 没有设置 `index=False`，所以生成的 `temp.xlsx` 中会额外出现原 DataFrame 的索引列。是否保留索引，要根据业务需求决定。

## 8. 今天代码中的问题与改进

### 8.1 `ExcelWriter` 没有关闭

`自写.py` 中：

```python
list = pd.ExcelWriter("type.xlsx")
```

但后续没有 `to_excel()`，也没有 `list.close()`，因此 `E:\type.xlsx` 为 0 字节。

正确做法：

```python
with pd.ExcelWriter("type.xlsx") as writer:
    df.to_excel(writer, sheet_name="sheet1", index=False)
```

### 8.2 不要用 `list` 作为变量名

```python
list = pd.ExcelWriter("type.xlsx")
```

`list` 是 Python 内置类型名。变量名会遮蔽内置功能，建议改成 `writer`。

### 8.3 变量名拼写要准确

`自写.py` 中使用了 `county`，如果实际含义是国家集合，应统一为 `country` 或 `unique_countries`，避免后续读代码时混淆。

### 8.4 直接取 `[1]` 有数据风险

```python
x.split("/")[1]
```

该写法只适合确定每个值都包含 `/` 的数据。真实 Excel 中可能有空值、单个国家或格式异常，需要先检查长度。

### 8.5 `str.contains()` 是“包含”匹配

```python
df[df["国家"].str.contains(country_name)]
```

它判断某个国家名称是否出现在整段文本中，而不是判断单元格是否严格等于该国家。当前课堂数据中这是合理的，但遇到国家名存在包含关系时，需要更严格的拆分后匹配。

### 8.6 `set()` 不保证工作表顺序

如果希望导出的 Sheet 顺序稳定，使用：

```python
unique_countries = list(dict.fromkeys(country))
```

### 8.7 工作表名称也需要清洗

批量导出真实数据时，Sheet 名称不能包含 `: \ / ? * [ ]`，长度也不能过长。课堂里的国家名没有这个问题，但通用脚本需要加清洗逻辑。

## 9. 字符串下标、`len()` 和 `range()`

`Untitled-1.py` 练习了字符串遍历：

```python
i = "2024"

for index in range(len(i)):
    print(index)
```

输出下标：

```text
0
1
2
3
```

根据下标取字符：

```python
for index in range(len(i)):
    print(i[index])
```

输出字符：

```text
2
0
2
4
```

更直接的遍历方式是：

```python
for character in i:
    print(character)
```

记忆：`len(i)` 得到长度，`range(len(i))` 得到合法下标范围，`i[index]` 取对应位置的字符。

## 10. 一份可复用的完整模板

```python
import pandas as pd


def split_countries(value):
    if not isinstance(value, str):
        return []
    return [item.strip() for item in value.split("/") if item.strip()]


def export_by_country(output_path):
    df = pd.DataFrame(
        [
            ["2023", "美国/新加坡"],
            ["2024", "中国/韩国"],
            ["2025", "日本/德国"],
            ["2026", "中国/法国"],
        ],
        index=["a", "b", "c", "d"],
        columns=["年份", "国家"],
    )

    countries = []
    for value in df["国家"]:
        countries.extend(split_countries(value))

    unique_countries = list(dict.fromkeys(countries))

    with pd.ExcelWriter(output_path) as writer:
        df.to_excel(writer, sheet_name="sheet1", index=False)

        for country_name in unique_countries:
            mask = df["国家"].apply(
                lambda value: country_name in split_countries(value)
            )
            df[mask].to_excel(
                writer,
                sheet_name=country_name,
                index=False,
            )


if __name__ == "__main__":
    export_by_country("temp.xlsx")
```

这份模板把课堂代码中的关键知识串起来：

- `DataFrame` 构造。
- 遍历一列。
- `split()` 拆分字符串。
- `extend()` 扩展列表。
- `dict.fromkeys()` 保持顺序去重。
- `apply()` 生成布尔筛选条件。
- `ExcelWriter` 上下文管理器。
- `to_excel()` 输出多个 Sheet。

## 11. 复习清单

- [ ] 能用二维列表创建 `DataFrame`。
- [ ] 能用字典创建 `DataFrame`。
- [ ] 能区分 `df["列"]` 和 `df[["列1", "列2"]]` 的返回类型。
- [ ] 能用 `.str.contains()` 筛选包含指定文本的行。
- [ ] 能解释 `x.split("/")[0]` 和 `x.split("/")[1]`。
- [ ] 能用 `apply(lambda x: ...)` 对整列逐项处理。
- [ ] 能把多个单元格中的国家拆出来并去重。
- [ ] 能用 `pd.ExcelWriter` 和 `to_excel()` 输出多个工作表。
- [ ] 知道 `ExcelWriter` 必须关闭，优先使用 `with`。
- [ ] 知道 `index=False` 的作用。
- [ ] 能解释 `len()`、`range()` 和字符串下标。
- [ ] 能处理空值、没有分隔符和重复数据。

## 12. 长期复习口诀

```text
DataFrame 是表，Series 是列；
双中括号选多列，contains 做包含筛；
split 拆字符串，apply 逐项改；
set 能去重但无序，字典去重可保序；
Writer 要关闭，with 最稳妥；
to_excel 写工作表，index 是否保留要看需求。
```

## 13. 对话补充：从里到外理解一行代码

遇到嵌套表达式，不要整行硬背，按从里到外的顺序拆开：

```python
x.split("/")[0].strip()
```

等价于：

```python
parts = x.split("/")
first = parts[0]
cleaned = first.strip()
```

如果 `x = "中国"`，没有 `/` 也不会报错：

```python
"中国".split("/")
# ["中国"]

"中国".split("/")[0]
# "中国"
```

所以 `split()` 找不到分隔符时，会把整个字符串作为唯一元素返回；但直接访问不存在的第二个元素仍会报错：

```python
"中国".split("/")[1]
# IndexError
```

## 14. 对象、容器和 `[]`

“容器”是可以装其他数据的对象，不等于 `[]` 符号本身；“索引”也不等于所有 `[]` 操作。

| 对象 | 示例 | `[]` 的含义 |
|---|---|---|
| `list` | `["A", "B"]` | 按位置取值：`items[0]` |
| `tuple` | `("A", "B")` | 按位置取值 |
| `str` | `"Python"` | 按位置取字符：`text[0]` |
| `dict` | `{ "name": "Tom" }` | 按 key 取值：`person["name"]` |
| `set` | `{ "A", "B" }` | 无固定位置，不能用 `items[0]` |
| `DataFrame` | `df` | 可按列名、多列名或布尔条件选择 |

因此 `对象[...]` 更准确地理解为“用选择信息访问对象”：

```python
df["国家"]                 # 按列名
df[["年份", "国家"]]       # 按多个列名
df[mask]                    # 按每行 True/False
```

`True` 和 `[True, False, True]` 也不是一回事：前者是一个布尔值，后者是一组可与三行逐一对应的布尔条件。`df[True]` 通常会被理解为寻找列名 `True`，没有该列时会出现 `KeyError`；`df[[True, False, True]]` 才是按行筛选。

## 15. 对象类型决定可调用的方法

不是“纯文本不能用方法”，而是不同类型拥有不同方法：

```python
text = "中国/日本"
text.split("/")       # str 的方法

items = ["中国", "日本"]
items.append("美国")  # list 的方法

df.to_excel("result.xlsx")  # DataFrame 的方法
```

`to_excel()` 是 Pandas 的 `Series`/`DataFrame` 方法，不是 `str` 或 Python `list` 的方法。下面两者结果不同：

```python
[i]       # 把 i 整体放进一个列表，例如 ["2024"]
list(i)   # 把 i 逐个拆开，例如 ["2", "0", "2", "4"]
```

如果一定要把单个值写进 Excel，要先转换成 Pandas 对象：

```python
pd.Series([i]).to_excel("year.xlsx", index=False)
pd.DataFrame([i]).to_excel("year.xlsx", index=False)
```

但这只会保存单个年份值，不会保存该年份对应的完整数据行。按年份拆分的真正目标应是：

```python
data[data["year"] == i].to_excel(writer, sheet_name=str(i))
```

## 16. 函数、`return`、`lambda` 和 `apply`

### 16.1 函数基本结构

```python
def add(a, b):
    result = a + b
    return result


x = add(3, 5)
```

- 参数决定函数接收什么输入。
- `return` 决定函数把什么结果交给后续代码。
- `print()` 只是显示给人看，不等于返回值。
- 函数没有 `return` 时，调用结果自动是 `None`。

参数和返回值是两个独立维度，存在四种组合：有参数/无参数 × 有返回值/无返回值。

```python
def show(name):
    print(name)       # 有参数，无显式返回值，结果为 None


def get_number():
    return 100        # 无参数，有返回值
```

### 16.2 `lambda` 是匿名函数，`apply()` 负责批量调用

```python
def extract_year(value):
    return value.split("/")[0]


data["year"] = data["type"].apply(extract_year)
```

等价的一行写法：

```python
data["year"] = data["type"].apply(
    lambda value: value.split("/")[0]
)
```

准确分工：

```text
apply  → 对一列中的每个元素调用规则
lambda → 临时定义一条简单规则
def    → 定义可复用、可包含多行逻辑的函数
```

例如只提取“中国”电影的年份：

```python
def extract_china_year(value):
    if "中国" in value:
        return value.split("/")[0]
    return None


data["year"] = data["type"].apply(extract_china_year)
```

### 16.3 `.str` 是 Pandas 的字符串批处理接口

单个字符串可以直接调用：

```python
text.split("/")
```

但 `data["type"]` 是一整列 `Series`，不能直接写：

```python
data["type"].split("/")
```

应使用 Pandas 提供的 `.str`：

```python
data["year"] = data["type"].str.split("/").str[0].str.strip()
```

常用方法包括 `.str.split()`、`.str.strip()`、`.str.contains()`、`.str.replace()`、`.str.upper()` 和 `.str.len()`。简单的字符串处理优先考虑 `.str`；需要条件判断或多步自定义逻辑时使用 `apply()` + 普通函数/lambda。

## 17. `len()`、`range()`、逐行读取和循环变量

```python
len(data)
```

对 DataFrame 通常表示行数；对字符串表示字符数；对列表表示元素个数。

```python
for index in range(len(data)):
    print(data.iloc[index])
```

含义是从位置 `0` 到 `len(data) - 1`，逐行取出 DataFrame。也可以使用：

```python
for index, row in data.iterrows():
    print(row)
```

注意缩进决定执行范围：

```python
for country_name in ["美国", "中国", "日本"]:
    result = df[df["国家"].str.contains(country_name, na=False)]
    print(country_name)
```

`print()` 在循环内会打印三个国家；如果放在循环外，循环变量会保留最后一次的值，最后只打印“日本”。这不代表前两个国家没有处理。

## 18. 最终汇总：这节课应该形成的完整模型

### 18.1 业务目标

把一张包含“年份、国家”等字段的 Excel 表，按分类条件拆成多个工作表。

### 18.2 代码对象关系

```text
整张表
  df / data
    ↓ 取一列
一列 Series
  df["国家"] / data["type"]
    ↓ split、str、apply、contains
处理后的值或布尔 Series
    ↓ df[条件]
筛选后的 DataFrame
    ↓ to_excel()
Excel 工作表
```

### 18.3 按多国家拆分的主线

```text
原始 DataFrame
→ 遍历“国家”列
→ split("/") 拆出单个国家
→ set() 或 unique() 去重
→ 一个国家一个国家地循环
→ contains() 生成 True/False 条件
→ df[条件] 筛选完整行
→ to_excel() 写入对应 Sheet
```

### 18.4 看到嵌套代码时的五个问题

1. 当前对象是什么类型：`str`、`list`、`Series` 还是 `DataFrame`？
2. 当前 `[]` 是按位置、按 key、按列名，还是按布尔条件选择？
3. 当前方法是在拆分、去重、判断、筛选，还是导出？
4. 这一步返回的是单个值、一列、一行、布尔条件，还是一张表？
5. 下一层代码要拿这个返回结果做什么？

本节课最重要的代码是：

```python
df[df["国家"].str.contains(country_name, na=False)].to_excel(
    writer,
    sheet_name=country_name,
)
```

完整翻译：

```text
取“国家”列
→ 判断每一行是否包含当前国家
→ 得到 True/False
→ 用布尔条件筛选完整行
→ 将筛选结果写入当前国家的 Sheet
```

### 18.5 适合当前阶段的学习方式

采用“边做边问”，但给问题分级：

- 不弄懂就无法理解下一行：立即解决。
- 只是某个 API 不熟：先记录，继续主线。
- 与当前项目无关的底层延伸：暂时放下。

推荐流程：

```text
看 5～15 分钟
→ 自己敲代码
→ 记录具体疑问
→ 先解决核心逻辑
→ 关闭视频重新写
→ 再查漏补缺
```

现阶段的目标不是凭空想到所有方法，而是能说清楚“输入是什么、经过哪一步处理、输出是什么”。API 可以查，问题拆解能力才是长期能力。

## Related notes

- [[Python基础学习路线]]（待确认实际笔记名称）
- [[Excel数据处理与VOC分析]]（如后续建立该主题笔记）
