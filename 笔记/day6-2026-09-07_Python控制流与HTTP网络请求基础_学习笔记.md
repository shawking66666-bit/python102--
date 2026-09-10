---
type: knowledge
status: confirmed
area: Programming
source: file-verified
confidence: confirmed
privacy: private
created: 2026-09-07
updated: 2026-09-08
tags: [Python, try-except, break, continue, return, function, IPv4, DNS, HTTP, HTTPS, routing, VPN, requests]
---

# Python 控制流与 HTTP 网络请求基础｜Day6 学习笔记

## 0. 本节课的两条主线

Day6 包含两组互相关联的知识：

```text
Python 程序控制
├── return 与 print 的区别
├── try...except 的放置范围
├── break、continue、return
└── 普通代码、循环和函数的执行顺序

Python 网络请求基础
├── IPv4 与二进制
├── 域名、DNS 和 IP
├── 路由与 NAT
├── HTTP 与 HTTPS
└── VPN 与完整网页请求过程
```

本节对应的实际练习文件是：

- `day6/教务系统练习自己重新梳理.py`

这些网络知识会直接用于后续的 Python `requests`、爬虫和 API 调用。

## 1. 函数返回值与 print() 不一样

假设题目要求函数返回固定字符串：

```python
def hello():
    return "Hello, World!"
```

调用过程：

```python
result = hello()
print(result)
```

```text
调用 hello()
    ↓
进入 hello 函数
    ↓
执行 return "Hello, World!"
    ↓
函数结束并返回字符串
    ↓
result = "Hello, World!"
```

对比下面两个函数：

```python
def hello_1():
    return "Hello, World!"


def hello_2():
    print("Hello, World!")
```

```python
result_1 = hello_1()
result_2 = hello_2()

print(result_1)  # Hello, World!
print(result_2)  # None
```

- `return`：把结果交给函数调用处。
- `print()`：只把内容显示在屏幕上。
- 函数没有执行 `return` 时，默认返回 `None`。

如果测试代码是：

```python
assert hello() == "Hello, World!"
```

那么大小写、空格和标点都必须完全一致。`print()` 不是强制要求，因为测试程序会自行调用函数并检查返回值。

## 2. try...except 应该放在哪里

核心原则：

> `try` 只包住可能产生目标异常的最小代码范围。

成绩输入可能因为无法转换成整数而触发 `ValueError`：

```python
try:
    score = int(input("请输入成绩："))
except ValueError:
    print("成绩必须是整数")
```

这里真正可能产生目标异常的是：

```python
int(input("请输入成绩："))
```

不要把姓名输入、字典保存和成功提示等无关代码全部放进 `try`。范围太大会让我们难以判断究竟是哪一步发生了异常。

## 3. 为什么输入校验还需要 while True

单独使用 `try...except` 只能防止程序直接崩溃。如果输入错误后需要重新输入，还要加入循环：

```python
while True:
    try:
        score = int(input("请输入成绩："))
        break
    except ValueError:
        print("成绩必须是整数，请重新输入")

print(f"最终成绩：{score}")
```

输入过程：

```text
输入 "九十"
    ↓
int("九十") 转换失败
    ↓
触发 ValueError
    ↓
执行 except 并重新循环

输入 "90"
    ↓
int("90") 转换成功
    ↓
score = 90
    ↓
执行 break，离开输入循环
```

## 4. break 结束的是最近一层循环

教务系统可以同时存在外层菜单循环和内层输入循环：

```python
while True:  # 外层：菜单循环
    choice = input("请选择功能：")

    if choice == "1":
        while True:  # 内层：成绩输入循环
            try:
                score = int(input("请输入成绩："))
                break
            except ValueError:
                print("成绩必须是整数")

        print(f"录入成绩：{score}")
```

内层的 `break` 只结束内层成绩输入循环，不会结束外层菜单循环。

判断方法：

> 从 `break` 所在位置向外找，遇到的第一个循环就是它要结束的循环。

## 5. continue、break、return 的区别

| 关键字 | 作用范围 | 执行后去哪里 |
|---|---|---|
| `continue` | 当前一轮循环 | 回到循环开头，开始下一轮 |
| `break` | 最近一层循环 | 跳到这层循环下面 |
| `return` | 整个函数 | 回到函数调用位置 |

### 5.1 continue

```python
for number in range(5):
    if number == 2:
        continue
    print(number)
```

输出：

```text
0
1
3
4
```

当 `number == 2` 时，本轮后面的 `print()` 被跳过，但循环没有结束。

### 5.2 break

```python
for number in range(5):
    if number == 2:
        break
    print(number)

print("循环结束")
```

输出：

```text
0
1
循环结束
```

### 5.3 return

```python
def find_number():
    for number in range(5):
        if number == 2:
            return number
    print("循环正常结束")


result = find_number()
print(result)
```

执行 `return number` 后，循环和 `find_number()` 函数都会结束，函数后面的代码不会继续执行。

记忆方式：

```text
continue → 回到循环上面
break    → 跳到循环下面
return   → 回到函数调用处
```

## 6. 程序的实际执行顺序

程序不是完整地“从上往下运行，再从下往上返回”。更准确的模型是：

```text
普通代码：通常从上往下
函数调用：从调用位置进入函数
函数返回：回到原来的调用位置
循环执行：回到循环条件处
```

示例：

```python
def input_score():
    score = int(input("请输入成绩："))
    return score


print("程序开始")
chinese = input_score()
print(f"语文成绩：{chinese}")
print("程序结束")
```

执行顺序：

```text
1. 输出“程序开始”
2. 调用 input_score()
3. 进入 input_score 函数
4. 执行 input() 和 int()
5. 执行 return score
6. 回到 input_score() 的调用位置
7. 把返回值赋给 chinese
8. 输出语文成绩
9. 输出“程序结束”
```

多个函数互相调用时，可以概括为：

```text
调用过程：由外到内
返回过程：由内到外
```

## 7. 把重复的成绩输入封装成函数

```python
def input_score(subject):
    while True:
        try:
            score = int(input(f"请输入{subject}成绩："))
            return score
        except ValueError:
            print(f"{subject}成绩必须是整数，请重新输入")
```

调用：

```python
chinese = input_score("语文")
math = input_score("数学")
english = input_score("英语")
```

`subject` 让同一个函数能够处理不同科目。输入正确后，`return score` 会直接结束函数并把成绩交回调用位置，因此不需要再写 `break`。

## 8. Day6 的实际练习：独立重写教务系统

Day6 重新组织并写出了完整教务系统，包括：

- 嵌套字典保存学生和三科成绩。
- `while True` 维持菜单运行。
- `match...case` 分配七项功能。
- 添加前检查姓名是否重复。
- 修改、删除、查询前检查学生是否存在。
- `.items()` 遍历所有学生。
- 字典推导式提取各科成绩。
- `max()`、`min()`、`sum()` 和 `len()` 完成统计。
- 遍历数据找出并列最高分或最低分学生。
- `break` 退出系统，`continue` 返回菜单。

这代表学习状态正在从“看懂已有代码”过渡到“自己组织一个完整程序”。

当前代码仍直接使用：

```python
chinese = int(input("请输入学生语文成绩："))
```

输入 `九十`、`89.5` 或空内容时仍可能触发 `ValueError`。下一步可以把三科输入改成 `input_score(subject)`，先掌握输入校验，不急着同时进行大规模重构。

## 9. Python 发出网络请求时发生了什么

以后使用 Python：

```python
import requests

response = requests.get("https://www.baidu.com")
```

表面上只有一行请求代码，背后会经历：

```text
Python requests
    ↓
读取 URL 中的域名
    ↓
DNS 把域名解析成服务器 IP
    ↓
根据目标 IP 查找路由
    ↓
经过网关、NAT、运营商和互联网路由器
    ↓
与网站建立安全连接
    ↓
发送 HTTP 请求
    ↓
服务器处理并返回 HTTP 响应
    ↓
requests 得到 response
```

## 10. URL、域名、DNS 和 IP

以这个地址为例：

```text
https://www.baidu.com/s?wd=Python
```

可以拆成：

```text
https          → 协议
www.baidu.com  → 域名
/s             → 请求路径
?wd=Python     → 查询参数
```

四个概念的关系：

```text
域名 → 我想找谁
DNS  → 对方地址是什么
IP   → 数据发往哪个网络地址
VPN  → 数据经过哪条加密通道
```

域名不是 DNS。域名是方便人记忆的名称，DNS 是把名称查询成地址的系统，IP 是网络通信使用的地址。

域名和 IP 也不一定一一对应：

- 一个域名可以对应多个 IP。
- 多个域名可以共享一个 IP。
- IP 可能发生变化。
- 多台家庭设备可以通过 NAT 共用一个公网 IP。

域名通常按年注册和续费；DNS 服务常有免费方案；服务器托管是另一项服务和费用。

## 11. IPv4 为什么是四组八位

例如：

```text
192.168.1.12
```

IPv4 共有 32 个二进制位，分为四组：

```text
xxxxxxxx.xxxxxxxx.xxxxxxxx.xxxxxxxx
```

每组八位，因此总共是：

```text
8 × 4 = 32 位
```

八个位置对应的二进制位权为：

```text
128  64  32  16  8  4  2  1
```

二进制每向左移动一位，数值乘以 2。

### 11.1 把 132 转成二进制

```text
132 = 128 + 4

位权：128 64 32 16 8 4 2 1
取值：  1  0  0  0 0 1 0 0

132 = 10000100
```

### 11.2 把 12 转成二进制

```text
12 = 8 + 4

位权：128 64 32 16 8 4 2 1
取值：  0  0  0  0 1 1 0 0

12 = 00001100
```

八位全部为 `1` 时：

```text
128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 = 255
```

因此 IPv4 每组十进制数的范围是 `0～255`。

IP 更适合理解为网络范围内用于定位和通信的地址，而不是永远不变的“唯一身份证”。

## 12. 路由与 NAT

DNS 解决的是：

> 目标网站的 IP 是什么？

路由解决的是：

> 数据下一步应该往哪里发送？

```text
电脑
  ↓
默认网关／家用路由器
  ↓
运营商网络
  ↓
互联网中的多个路由器
  ↓
目标网站
```

路由器根据目标 IP 和路由表决定下一跳。路由不是给网站分配 IP，也不是把域名转换成 IP。

家庭电脑可能使用私有 IP：

```text
192.168.1.10
```

家用路由器会通过 NAT 把私有地址转换为家庭的公网出口地址：

```text
电脑私有 IP
    ↓ NAT
家庭公网 IP
    ↓
互联网
```

返回数据到达路由器后，路由器再把它交给发起请求的内网设备。

## 13. HTTP 请求与响应

HTTP 全称：

```text
Hypertext Transfer Protocol
超文本传输协议
```

它规定客户端和服务器如何交换请求与响应。

```python
response = requests.get("https://example.com")

print(response.status_code)
print(response.headers)
print(response.text)
```

数据方向：

```text
请求：Python 程序 → 服务器
响应：服务器 → Python 程序
```

一次请求通常包含请求方法、请求地址、请求头、请求参数，以及可能存在的请求体。

常见方法：

```text
GET     获取数据
POST    提交数据
PUT     整体修改数据
PATCH   部分修改数据
DELETE  删除数据
```

示例：

```python
response = requests.get(
    "https://example.com/search",
    params={"keyword": "Python"},
)
```

最终地址可能是：

```text
https://example.com/search?keyword=Python
```

常见响应状态码：

```text
200  请求成功
404  请求的资源不存在
500  服务器内部发生错误
```

## 14. HTTP 与 HTTPS 的区别

HTTPS 可以初步理解为：

```text
HTTP + 加密与身份验证
```

HTTPS 主要解决：

1. 防止通信内容被直接读取。
2. 防止传输内容被随意篡改。
3. 通过证书帮助客户端确认服务器身份。

常见端口：

```text
HTTP   → 80
HTTPS  → 443
```

端口可以暂时理解为服务器上的服务入口编号。

## 15. 浏览器搜索百度的完整过程

```text
1. 浏览器读取 www.baidu.com
2. DNS 查询百度入口 IP
3. 电脑根据目标 IP 查找路由
4. 数据发送给默认网关
5. 家用路由器执行 NAT
6. 数据经过运营商及多个路由器
7. 到达百度接入服务器或负载均衡
8. 建立 TCP 或 QUIC 连接
9. 建立 HTTPS 安全通信
10. 浏览器发送 HTTP 搜索请求
11. 百度后端搜索服务处理关键词
12. 百度返回 HTTP 响应
13. 浏览器解析并显示搜索结果
```

网页版百度不是把完整的百度搜索软件安装到本机，而是：

```text
浏览器运行网页前端代码
    ↓
向百度后端搜索服务发送请求
    ↓
服务器返回结果
    ↓
浏览器渲染结果
```

本机 IP 通常在设备联网时通过 DHCP 等机制获得；DNS 负责域名解析；网络层使用 IP 进行标识和跨网络转发。这三件事不能混为同一个步骤。

## 16. VPN 与 DNS

VPN 全称：

```text
Virtual Private Network
虚拟专用网络
```

它会在设备与 VPN 服务器之间建立加密通道：

```text
没有 VPN：
电脑 → 路由器 → 运营商 → 目标网站

使用 VPN：
电脑 → 加密通道 → VPN 服务器 → 目标网站
```

VPN 中配置 DNS 的常见原因：

- 让域名查询使用指定的 DNS 服务或经过指定通道。
- 减少 DNS 查询走到 VPN 通道外的情况。
- 解析公司或组织内部域名。
- 让解析结果与 VPN 所处的网络环境保持一致。

## 17. 网络知识与 Python 的关系

### 17.1 爬虫

```python
response = requests.get(url)
```

需要理解域名如何解析、HTTP 请求如何发送、状态码表示什么，以及为什么会出现 DNS、连接、SSL 或超时错误。

### 17.2 API 调用

```python
response = requests.post(api_url, json=data)
```

需要理解 URL、请求方法、请求头、参数、请求体和 HTTPS。

### 17.3 排查网络报错

```text
域名写对了吗
    ↓
DNS 解析成功了吗
    ↓
网络和路由通吗
    ↓
HTTPS 连接成功了吗
    ↓
HTTP 状态码是什么
    ↓
响应数据格式正确吗
```

以后调试爬虫或 API 时，应按照请求发生的层次定位问题，而不是看到所有错误都直接修改解析代码。

## 18. 当前掌握程度

### 已经理解

- `print()` 与 `return` 的职责不同。
- `break` 只结束最近的一层循环。
- `continue` 跳过本轮，`return` 结束整个函数。
- 普通代码、函数调用和循环具有不同的执行路径。
- 能够独立重新组织教务管理系统。
- 开始区分域名、DNS、IP、路由、HTTP、HTTPS 和 VPN。
- 能把网页访问过程与 Python `requests` 联系起来。

### 正在形成

- 根据目标异常决定 `try` 的最小范围。
- 用内层循环实现某一项输错后只重新输入该项。
- 把重复的成绩输入封装成函数。
- 从请求链路的不同层次判断网络错误。

### 下一步重点

- 给教务系统加入 `ValueError` 输入校验。
- 练习 `input_score(subject)` 函数。
- 继续追踪参数、局部变量、返回值和调用位置。
- 用一个真实的 `requests.get()` 示例观察 URL、状态码、响应头和响应正文。
- 通过小题巩固 IPv4 位权，例如把 `5 = 4 + 1` 写成八位二进制。

