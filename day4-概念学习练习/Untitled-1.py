

list1 = (

("S001","王林",85,92,78),
("S002","李慕婉",92,88,95),
("S003","十三",78,85,82),
("S004","曾牛",88,79,91),
("S005","周轶",95,96,89),
("S006","王卓",76,82,77),
("S007","红蝶",89,91,94),
("S008","徐立国",75,69,82),
("S009","许木",86,89,98),
("S010","适天",66,59,72)

)

#for s in list1:
   # total = sum([s[2], s[3], s[4]])
    #print(f"{s[1]}的总分是{total}")






every_total_score = [sum(student[row] for row in (2, 3, 4)) for student in list1]
for index, i in enumerate(list1):
    print(f"{i[1]}的总分是{every_total_score[index]}")


for i ,z in zip(every_total_score, list1):
    
    print(f"{z[1]}的成绩是{i}")