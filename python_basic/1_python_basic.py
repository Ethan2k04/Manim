#1 变量、函数和类

words = "python是世界上最好的编程语言"
print(words)

#变量名     #变量
teacher = "1+1=?"
student = "2"

#函数
print(teacher)
print(student)

#字符串、整形（整数）、列表、布尔 都是变量
num_1 = 100
num_2 = 900
result = num_1 + num_2
print(result)

#a += b 等价于 a(新变量) = a(旧变量，被新变量覆盖) + b
a = 0
while a <= 10:
    print(a)
    a += 1

#列表
list_a = [666, "manim", words]
print(list_a)
#?
print(list_a[0])
print(list_a[1])
print(list_a[2])
#for语句
list_b = [1, 2, 3, 4, 5, 6]
for i in list_b:
    print(i)

#输入函数 input
your_name = input("What's your name:")
print("Hello" + your_name + "welcomes to ManimLaboratory")

#布尔 就是True(真)和假(False) if语句
print("How about our headmaster")
fat = True
thin = False
smart = True
if fat:
    print("He is fat.")
if thin:
    print("He is thin")
if smart:
    print("He is smart")

#结合if语句和布尔值以及input函数

