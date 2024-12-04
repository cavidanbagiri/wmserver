
class Point(float):

    def __new__(cls, x):
        print('Creating an instance ...')
        # instance = super().__new__(cls, x**2)
        # return instance
        return super().__new__(cls, x**2)

    # def __init__(self, x, y):
    #     print('init calling')
    #     self.x = x
    #     self.y = y

    # def __str__(self):
    #     return f'{self.x} {self.y}'



p1 = Point(10)
print(p1)

# p2 = object.__new__(Point) # Step 1
# p2.__init__(10,20)         # Step 2
# print(p2)
