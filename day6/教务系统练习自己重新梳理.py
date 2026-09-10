"""
基于现有知识开发一个教务管理系统

开发一个教务管理系统,在该系统中可以维护和管理学员的成绩信息,具体需求如下:

1. 添加学生信息:根据提示录入学生姓名、语文、数学、英语成绩,录入完成保存到系统中。

2. 修改学生信息:要求输入要修改的学生姓名,然后再提示输入语文、数学、英语成绩,输入完成后修改学员信息。

3. 删除学生信息:要求输入要删除的学生姓名,根据姓名删除学生信息。

4. 查询学生信息:要求输入要查询的学生姓名,根据姓名查询学生信息并输出。

5. 列出所有学生:遍历所有学生信息并输出。

6. 统计班级成绩:统计班级语文、数学、英语成绩的最高分、最低分、平均分,以及语文、数学、英语最高分和最低分的学
员姓名。

7. 退出系统。
数据格式：{"姓名":{"语文":成绩,"数学":成绩,"英语":成绩}}
"""

menu = """
###########   欢迎使用教务管理系统，请选择功能(1-7): ################
###########         1.添加学生信息                  ################
###########         2.修改学生信息                  ################
###########         3.删除学生信息                  ################
###########         4.查询学生信息                  ################
###########         5.列出所有学生                  ################
###########         6.统计班级成绩                  ################
###########         7.退出系统                      ################
"""
print(menu)
edu_system= {}
while True:
    choice = input("请选择你要的功能(1-7)：")
    match choice:
        case "1":
            name = input("请输入学生姓名：")
            if name in edu_system:
                print("该学生已存在，请重新添加")
                continue
            else:
                chinese = int(input("请输入学生语文成绩："))
                math = int(input("请输入学生数学成绩："))
                english = int(input("请输入学生英语成绩："))
                edu_system[name] = {"语文" : chinese, "数学" : math, "英语" : english}
                print(f"{name}学生信息添加成功")
        case "2":
            name = input("请输入要修改的学生姓名：")
            if name not in edu_system:
                print("未找到该学生，请重新输入")
                continue
            else:
                chinese = int(input("请输入学生语文成绩："))
                math = int(input("请输入学生数学成绩："))
                english = int(input("请输入学生英语成绩："))
                edu_system[name] = {"语文":chinese, "数学":math, "英语":english}
                print(f"{name}学生信息修改成功")
        case "3":
            name = input("请输入要删除的学生姓名：")
            if name not in edu_system:
                print("未找到要删除的学生信息，请重新输入")
                continue
            else:
                del edu_system[name]
                print(f"{name}学生信息删除成功")
        case "4":
            name = input("请输入要查找的学生姓名：")
            if name not in edu_system:
                print("未找到该学生的信息，请重新输入")
            else:
                print(f"{name}学生的语文成绩是：{edu_system[name]["语文"]}，数学成绩是：{edu_system[name]["数学"]}，英语成绩是：{edu_system[name]["英语"]}")
        case "5":
            if edu_system:
                for name, scores in edu_system.items():
                    print(f"{name}学生的语文成绩是{scores["语文"]}，数学成绩是{scores["数学"]}，英语成绩是{scores["英语"]}")
            else:
                print("列表为空，请先添加学生信息")
                continue
        case "6":
            if not edu_system:
                print("暂无学生信息")
                continue
            else:
                chinese_scores = {name:scores['语文'] for name, scores in edu_system.items()}
                math_scores = {name:scores['数学'] for name, scores in edu_system.items()}
                english_scores = {name:scores['英语'] for name, scores in edu_system.items()}
                chinese_avg = sum(chinese_scores.values())/len(chinese_scores)
                math_avg = sum(math_scores.values())/len(math_scores)
                english_avg = sum(english_scores.values())/len(english_scores)
    
                for name , scores in edu_system.items():
                    if scores["语文"] == max(chinese_scores.values()):
                        print(f"语文的最高分是{max(chinese_scores.values())}，学生姓名是{name}")
                    if scores["语文"] == min(chinese_scores.values()):
                        print(f"语文的最低分是{min(chinese_scores.values())}，学生姓名是{name}")
    
                for name , scores in edu_system.items():
                    if scores["数学"] == max(math_scores.values()):
                        print(f"数学的最高分是{max(math_scores.values())}，学生姓名是{name}")
                    if scores["数学"] == min(math_scores.values()):
                        print(f"数学的最低分是{min(math_scores.values())}，学生姓名是{name}")
    
                for name , scores in edu_system.items():
                    if scores["英语"] == max(english_scores.values()):
                        print(f"英语的最高分是{max(english_scores.values())}，学生姓名是{name}")
                    if scores["英语"] == min(english_scores.values()):
                        print(f"英语的最低分是{min(english_scores.values())}，学生姓名是{name}")
                print(f"语文平均分：{chinese_avg}")
                print(f"数学平均分：{math_avg}")
                print(f"英语平均分：{english_avg}")

        case "7":
            print("系统已退出")
            break
        case _:
            print("输入错误，请重新输入")

            