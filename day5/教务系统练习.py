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

数据格式：["姓名":{"语文":成绩,"数学":成绩,"英语":成绩}]
"""

print(menu)
edu_system = {}
while True:      
    
    choice = input("请输入要执行的操作(1-7): ")
    match choice:
        case "1":
            name = input ("请输入学生姓名:")
            chinese = int(input("请输入语文成绩:"))
            math = int(input("请输入数学成绩:"))
            english = int(input("请输入英语成绩:"))
            if name in edu_system:
                print(f"{name}已存在，请重新输入")
                continue
            else:
                edu_system[name] = {"语文": chinese, "数学": math, "英语": english}
                print(f"{name}的成绩已添加成功")

        case "2":
            name = input("请输入要修改的学生姓名:")
            if name in edu_system:
                chinese = int(input("请输入语文成绩:"))
                math = int(input("请输入数学成绩:"))
                english = int(input("请输入英语成绩:"))
                edu_system[name] = {"语文": chinese, "数学": math, "英语": english}#数据格式：["姓名":{"语文":成绩,"数学":成绩,"英语":成绩}]
                print(f"{name}的成绩已修改成功")
            else:
                print(f"{name}不存在，请重新输入")

        case "3":
            name = input("请输入要删除的学生姓名:")
            if name in edu_system:
                del edu_system[name]
                print(f"{name}的成绩已删除成功")
            else:
                print(f"{name}不存在，请重新输入")

        case "4":
            name = input("请输入要查询的学生姓名:")
            if name in edu_system:
                print(f"{name}的语文成绩是{edu_system[name]['语文']},数学成绩是{edu_system[name]['数学']},英语成绩是{edu_system[name]['英语']}")
            else:
                print(f"{name}不存在，请重新输入")

        case "5":
            for name, scores in edu_system.items():
                print(f"{name}的语文成绩是{scores['语文']},数学成绩是{scores['数学']},英语成绩是{scores['英语']}")

        case "6":
            if not edu_system:
                print("目前没有学生信息，请先添加学生")
                continue
            
            #数据格式：["姓名":{"语文":成绩,"数学":成绩,"英语":成绩}]
            
            chinese_scores = {name: scores['语文'] for name, scores in edu_system.items()}
            print(f"语文最高分是:{int(max(chinese_scores.values()))}")
            print(f"语文最低分是:{int(min(chinese_scores.values()))}")
            print(f"语文平均分是:{float(sum(chinese_scores.values())/len(chinese_scores.values())):.2f}")

            for name, score in chinese_scores.items():
                if score == max(chinese_scores.values()):
                    print(f"语文最高分学生：{name}")

                if score == min(chinese_scores.values()):
                    print(f"语文最低分学生：{name}")
            
            math_scores = {name: scores['数学'] for name, scores in edu_system.items()}
            print(f"数学最高分是:{int(max(math_scores.values()))}")
            print(f"数学最低分是:{int(min(math_scores.values()))}")
            print(f"数学平均分是:{float(sum(math_scores.values())/len(math_scores.values())):.2f}")

            for name, score in math_scores.items():
                if score == max(math_scores.values()):
                    print(f"数学最高分学生：{name}")

                if score == min(math_scores.values()):
                    print(f"数学最低分学生：{name}")

            english_scores = {name: scores['英语'] for name, scores in edu_system.items()}
            print(f"英语最高分是:{int(max(english_scores.values()))}")
            print(f"英语最低分是:{int(min(english_scores.values()))}")
            print(f"英语平均分是:{float(sum(english_scores.values())/len(english_scores.values())):.2f}")

            for name, score in english_scores.items():
                if score == max(english_scores.values()):
                    print(f"英语最高分学生：{name}")

                if score == min(english_scores.values()):
                    print(f"英语最低分学生：{name}")

        case "7":
            print("退出系统")
            break

        case _:
            print("输入错误，请重新输入")