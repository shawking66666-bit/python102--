---
type: knowledge
status: confirmed
area: Programming
source: file-verified
confidence: confirmed
privacy: private
created: 2026-09-01
updated: 2026-09-01
tags: [Python, pandas, Excel, DataFrame, Series, 布尔筛选, 课后练习, 错误复盘]
---

# day01课后练习

## 一、今天练习的定位

2026-08-31 的重点不是记忆新的 Pandas API，而是把前面学过的内容组合成业务流程，并检查自己能不能从需求推导代码。

今天的实际练习不是一道题，而是一组递进题：

```text
按技能分 Sheet
→ 按部门分 Sheet，并保留人数不少于 2 人的部门
→ 部门筛选 + 工资二次筛选
→ 忽略“未知”
→ 处理 contains() 的误匹配风险
→ 先筛北京员工，再按技能分 Sheet
→ 自己用 apply(lambda) 改写字段
```

因此，今天暴露的主要问题不是“完全不会写”，而是：看懂单行代码和独立组织完整流程之间还有差距。

## 二、根据实际文件还原的练习链路

本次核对了 `E:\python102项目\day1\现实业务练习` 中的 6 个强化练习脚本、`day1.py`、`自写.py`、`Untitled-1.py`，以及它们生成的 Excel 文件。

| 练习 | 业务要求 | 练到的模式 | 实际结果 |
|---|---|---|---|
| 强化练习一 | 员工按技能分 Sheet | `split()`、`append()`、`set()`、`contains()`、`to_excel()` | `员工技能.xlsx` 有 Java、Excel、Python、SQL 4 个 Sheet |
| 强化练习二 | 部门按 Sheet 输出，只保留人数不少于 2 人的部门 | 拆分部门、去重、`len(results)`、`if` | `部门列表.xlsx` 有技术、销售、运营 |
| 强化练习三 | 部门包含销售，且工资大于等于 10000 | 两个条件的先后组合 | 输出结果正确，但代码中的 `for i in l` 没有实际作用 |
| 强化练习四 | 忽略“未知”并按国家分 Sheet | `if`、`continue`、布尔筛选 | `国家.xlsx` 没有“未知” Sheet |
| 强化练习五 | 避免 `手机` 匹配到 `手机壳` | 精确拆分后的成员判断 | 目标未真正实现：输出只有“手机壳” Sheet，且包含 3 行 |
| 强化练习六 | 只处理北京员工，再按技能分 Sheet | 先筛城市，再拆技能和分 Sheet | `北京员工技能.xlsx` 有 Python、SQL、Excel 3 个 Sheet |
| 自写.py | 用 `apply(lambda)` 处理国家字段 | `Series.apply()`、`lambda`、字段赋值 | 能生成新列 `c`，但 `ExcelWriter` 变量命名和关闭方式有问题 |
| Untitled-1.py | 用下标遍历字符串 | `len()`、`range()`、字符串索引 | 能输出 `2024` 的下标和每个字符 |

## 三、今天必须建立的对象关系

```text
原始 DataFrame
    ↓ df["技能"]
一列 Series
    ↓ 遍历
单元格字符串 str，例如 "Python/Excel"
    ↓ split("/")
一个技能列表 list，例如 ["Python", "Excel"]
    ↓ append / extend
收集全部技能的 list
    ↓ set() 或顺序去重
不重复技能集合或列表
    ↓ 遍历一个技能
布尔 Series，例如 [True, False, True]
    ↓ df[mask]
筛选后的 DataFrame
    ↓ to_excel()
Excel 中的一个 Sheet
```

最重要的类型边界：

| 对象 | 示例 | 代表什么 | 常见操作 |
|---|---|---|---|
| `str` | `"Python/Excel"` | 一个单元格里的文本 | `split()`、`strip()`、下标取字符 |
| `list` | `["Python", "Excel"]` | 有顺序、可重复的一组值 | `append()`、`extend()`、遍历 |
| `set` | `{ "Python", "Excel" }` | 不重复的一组值 | 去重；不保证顺序 |
| `Series` | `df["技能"]` | DataFrame 的一列 | `.str`、`apply()`、比较运算 |
| 布尔 `Series` | `df["工资"] >= 10000` | 每一行对应一个 True/False | `df[mask]`、`.any()`、`.all()`、`.sum()` |
| `DataFrame` | `df` 或 `df[mask]` | 完整二维表 | 选列、筛行、`to_excel()` |

## 四、`df[]` 的三种核心用法

```python
df["城市"]
```

取单列，返回 `Series`。

```python
df[["姓名", "城市"]]
```

取多列，返回 `DataFrame`，因此需要双中括号。

```python
mask = df["城市"] == "北京"
city = df[mask]
```

先得到布尔 `Series`，再用它保留对应为 `True` 的行。

错误写法：

```python
df["国家" == i]
```

Python 会先计算普通字符串之间的比较：

```python
"国家" == i
```

结果是单个 `True` 或 `False`，整句可能变成 `df[False]`。这不是逐行比较。

正确写法：

```python
df[df["国家"] == i]
```

这里的 `df["国家"]` 才是整列数据，比较后才会得到逐行对应的布尔 `Series`。

判断口诀：

> 列名是普通字符串，`df["列名"]` 才是这一列的数据；比较符号要放在整列取出之后。

## 五、单个 bool、布尔 Series 与 if

```python
12000 >= 10000
```

返回一个单独的 `bool`：`True`。

```python
df["工资"] >= 10000
```

返回一列 True/False，整体类型仍是 `Series`。它可以用于：

```python
result = df[df["工资"] >= 10000]
```

但不能直接写：

```python
if df["工资"] >= 10000:
    ...
```

因为 `if` 需要一个最终的单个真假值。如果业务确实需要把整列汇总成一个判断，要明确规则：

```python
if (df["工资"] >= 10000).any():
    pass  # 至少一个人满足

if (df["工资"] >= 10000).all():
    pass  # 所有人满足

if (df["工资"] >= 10000).sum() >= 2:
    pass  # 满足人数至少为 2
```

`if` 和 `df[条件]` 的分工：

```text
if              → 控制代码是否执行
df[布尔条件]     → 筛选哪些行保留
```

## 六、循环变量不是历史数据

错误思路：

```python
for i in city["技能"]:
    for z in i.split("/"):
        print(z)

z = set(z)
```

`z` 每次只保存当前循环值，下一轮会覆盖上一轮。循环结束时，`z` 通常只是最后一次拿到的字符串；对它使用 `set(z)`，就会变成对字符去重。

正确思路：用列表保存每一次出现的值：

```python
skills = []

for value in city["技能"]:
    for skill in value.split("/"):
        skills.append(skill.strip())

unique_skills = list(dict.fromkeys(skills))
```

对象分工：

```text
value / skill → 当前值
skills        → 历史上收集到的全部值
unique_skills → 去重后准备循环输出的值
```

`split()` 也不是简单删除分隔符：

```python
"Python/Excel".split("/")
# ["Python", "Excel"]
```

## 七、`==`、`contains()` 与精确成员判断

```python
df["技能"] == "Python"
```

判断整个单元格是否完全等于 `Python`。`Python/Excel` 不会匹配。

```python
df["技能"].str.contains("Python", regex=False, na=False)
```

判断文本中是否出现 `Python`。`Python/Excel` 也会匹配。

当一个单元格是用 `/` 分隔的分类列表时，`contains()` 可能误匹配：

```text
手机/数码
手机
手机壳
```

如果业务要求“分类成员必须完全等于手机”，应先拆分，再判断成员：

```python
def split_items(value):
    if not isinstance(value, str):
        return []
    return [item.strip() for item in value.split("/") if item.strip()]


mask = df["类别"].apply(
    lambda value: "手机" in split_items(value)
)
result = df.loc[mask]
```

### 对强化练习五的实际纠正

原脚本虽然写了“解决 contains() 的误匹配”，但存在三个问题：

1. `for i in l` 中的 `i` 没有参与筛选条件。
2. 条件被硬编码为 `if "手机" in x`，每次都只筛选“手机”。
3. 结果却使用 `sheet_name=i` 输出，因此实际生成的 Sheet 名称与筛选内容不对应。

更接近题目目标的写法是：

```python
unique_categories = list(dict.fromkeys(
    category
    for value in df["类别"]
    for category in split_items(value)
))

with pd.ExcelWriter("商品类别.xlsx") as writer:
    for category in unique_categories:
        mask = df["类别"].apply(
            lambda value: category in split_items(value)
        )
        df.loc[mask].to_excel(
            writer,
            sheet_name=category,
            index=False,
        )
```

这段代码的关键不是“换一个字符串函数”，而是把复合分类先还原成成员列表，再做精确成员判断。

## 八、今天遗漏但必须补上的代码问题

### 1. 强化练习三的循环是多余的

原代码在 `for i in l` 内部始终执行：

```python
results = df[df["部门"].str.contains("销售")]
results[results["工资"] >= 10000].to_excel(
    writer,
    sheet_name="销售",
)
```

`i` 没有被使用，同一张 Sheet 会被重复写入。正确的业务逻辑只需要一次组合条件：

```python
mask = (
    df["部门"].str.contains("销售", regex=False, na=False)
    & df["工资"].ge(10000)
)

with pd.ExcelWriter("销售工资列表.xlsx") as writer:
    df.loc[mask].to_excel(
        writer,
        sheet_name="销售",
        index=False,
    )
```

### 2. `ExcelWriter` 优先使用 `with`

练习中多次写成：

```python
writer = pd.ExcelWriter("result.xlsx")
...
writer.close()
```

这在正确执行到最后一行时可以工作，但中途报错或忘记关闭时，文件可能不完整。推荐：

```python
with pd.ExcelWriter("result.xlsx") as writer:
    df.to_excel(writer, sheet_name="data", index=False)
```

离开 `with` 代码块时会自动保存并关闭。

### 3. 不要使用 `list` 作为变量名

`day1.py` 和 `自写.py` 中出现了：

```python
list = pd.ExcelWriter("career.xlsx")
```

`list` 是 Python 内置类型名。应改为：

```python
writer = pd.ExcelWriter("career.xlsx")
```

同理，`l`、`i`、`z` 在短练习中可以暂用，但正式代码应使用 `skills`、`category`、`unique_categories` 等能表达含义的名字。

### 4. `set()` 去重不保证 Sheet 顺序

```python
unique_skills = set(skills)
```

可以去重，但导出顺序不稳定。想保持首次出现顺序时使用：

```python
unique_skills = list(dict.fromkeys(skills))
```

### 5. `contains()` 应明确匹配规则

文本搜索建议至少写：

```python
df["部门"].str.contains(
    "销售",
    regex=False,
    na=False,
)
```

`regex=False` 表示按普通文本匹配；`na=False` 避免空值产生空判断结果。若分类存在包含关系，仅加这两个参数仍不能解决业务误匹配，仍需使用拆分后的成员判断。

### 6. `len()` 不是统计 True 的数量

```python
mask = df["工资"] >= 10000
len(mask)
```

得到的是条件序列的长度，也就是行数，不是满足条件的人数。统计 True 的数量使用：

```python
mask.sum()
```

而 `len(df.loc[mask])` 表示筛选后剩余的行数，二者在结果上可能相同，但含义不同。

## 九、`apply()`、`lambda` 与 `.str` 的边界

`自写.py` 中的代码：

```python
df["c"] = df["国家"].apply(
    lambda x: x.split("/")[0].strip()
)
```

执行顺序是：

```text
df["国家"]       → 取出一列 Series
apply(...)       → 逐个取出单元格
lambda x         → 当前单元格字符串
x.split("/")     → 得到 list
[0]              → 取第一个元素
strip()          → 清理空格
df["c"] = ...    → 把每行结果保存成新列
```

如果只是整列的简单字符串处理，也可以使用 Pandas 的 `.str`：

```python
df["国家首项"] = df["国家"].str.split("/").str[0].str.strip()
```

记忆：

```text
.str     → Pandas 对整列做常见字符串操作
apply    → 对整列逐项调用规则
lambda   → 临时写一条简单规则
def      → 规则较长或需要复用时定义函数
```

## 十、完整业务模板：北京员工按技能分 Sheet

```python
import pandas as pd


def split_items(value):
    if not isinstance(value, str):
        return []
    return [item.strip() for item in value.split("/") if item.strip()]


city = df.loc[df["城市"].eq("北京")].copy()

skills = []
for value in city["技能"]:
    skills.extend(split_items(value))

unique_skills = list(dict.fromkeys(skills))

with pd.ExcelWriter("北京员工技能.xlsx") as writer:
    for skill in unique_skills:
        mask = city["技能"].apply(
            lambda value: skill in split_items(value)
        )
        city.loc[mask].to_excel(
            writer,
            sheet_name=skill,
            index=False,
        )
```

固定翻译：

```text
业务需求
→ 先筛北京
→ 取北京员工的技能列
→ 拆分复合技能
→ 收集并去重
→ 遍历每个技能
→ 生成逐行布尔条件
→ 筛选完整员工行
→ 写入对应 Sheet
```

## 十一、下次写代码的固定流程

遇到任何类似题目，先写中文步骤，再写代码：

1. 明确原始输入是什么：DataFrame、Series、单元格字符串还是列表。
2. 明确业务筛选条件：完全相等、文本包含，还是拆分后的成员完全匹配。
3. 先写出中间对象名称：`city`、`skills`、`unique_skills`、`mask`、`result`。
4. 每完成一步打印一次类型和内容：`type(value)`、`print(value)`。
5. 最后再输出 Excel，并优先使用 `with pd.ExcelWriter(...)`。

遇到嵌套表达式时，从里到外拆：

```python
x.split("/")[0].strip()
```

等价于：

```python
parts = x.split("/")
first = parts[0]
cleaned = first.strip()
```

每次问自己：

1. 当前对象是什么类型？
2. 这一层方法接收什么输入？
3. 这一层返回什么结果？
4. `[]` 是取位置、取 key、选列，还是按布尔条件筛行？
5. 下一行拿到的是单个值、一列、一组条件，还是完整表格？

## 十二、复习清单与下次练习

- [ ] 能区分 `df["列"]`、`df[["列1", "列2"]]`、`df[mask]`。
- [ ] 能解释单个 `bool` 和布尔 `Series` 的区别。
- [ ] 能说明 `if` 控制流程，`df[条件]` 筛选数据。
- [ ] 能用 `split()` 拆分复合字段，并用列表保存历史数据。
- [ ] 能解释为什么 `set("Python")` 是按字符去重。
- [ ] 能区分 `==`、`contains()` 和拆分后的精确成员判断。
- [ ] 能使用 `mask.sum()` 统计满足条件的行数。
- [ ] 能使用 `apply(lambda)` 给 DataFrame 增加新列。
- [ ] 能用 `with pd.ExcelWriter(...)` 导出多个 Sheet。
- [ ] 能说明 `index=False` 是否保留 DataFrame 索引列。
- [ ] 能解释 `len()`、`range()` 和字符串下标。
- [ ] 能指出强化练习三的多余循环和强化练习五的未完成修复。

下次不看答案完成：

> 从员工表中筛选上海员工，再按照技能拆成不同 Sheet。

完成后再增加一个要求：只输出至少有 2 名上海员工掌握的技能。这样可以继续练习“先筛选城市 → 拆技能 → 统计人数 → 再导出”的组合逻辑。

## Related notes

- `E:\python102项目\笔记\day1-2026-08-29_Python操作Excel自动化开发_学习笔记.md`
- `E:\python102项目\笔记\day2-2026-08-31_Python爬取小说_学习笔记.md`
