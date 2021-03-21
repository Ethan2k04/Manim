import time
## 关于 类(class)和 方法(method) 的基础教学

# 井号("#")表示注释，不影响代码块的运行

class Shop:
    def __init__(self, shop_name):  #⬅️
        self.shop_name = shop_name  #这里的shop_name和上面的shop_name是同一个变量
        self.count = 0
        self.good_list = {"Bread": 5,
                          "Orange_juice": 5,
                          "Coffee": 5.5,
                          "Noodles": 6}
        self.request = None

    def welcome(self):
        print(f"Cashier: Welcome to {self.shop_name}")
        time.sleep(1)

    def ask_request(self):
        print("Cashier: What can I do for you?")
        self.request = input("Me: ")

    def print_good_list(self):
        print("##########")
        print("__________")
        print("Good List:")
        print("----------")
        for key, value in self.good_list.items():
            print(key + ": " + str(value) + " RMB ")
        print("##########")

    def purchase(self):
        item = input("What do you want?")
        self.count += self.good_list[item]

    def check(self):
        print("Cashier: Please wait.")
        for i in range(3):
            print("*")
            time.sleep(1)
        print(f"Cashier: The total is {self.count} RMB")


my_shop = Shop(shop_name="EIGHT ELEVEN")
my_shop.welcome()
while True:
    my_shop.ask_request()

    if my_shop.request == "buy":
        my_shop.print_good_list()
        my_shop.purchase()

    if my_shop.request == "check":
        my_shop.check()