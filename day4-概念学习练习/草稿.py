e = set()
e.add(225)
#s = e.pop()
#print(e)
print(e)
print(type(e))


all_set = {
    student
    for student in football_set
    if student in basketball_set
    and student in french_set
    and student in art_set
}

print(f"同时选修四门课的学生：{all_set}")