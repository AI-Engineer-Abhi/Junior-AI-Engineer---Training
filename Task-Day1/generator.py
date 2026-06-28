# Generator

# Square only even numbers
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]

gen = (num**2 for row in matrix for num in row if num % 2 == 0)

print(list(gen))


##

def gen_func():
    for i in range(5):
        yield i ** 2
a = gen_func()

for value in a:
    print(value)
# print(next(a))
# print(next(a))
# print(next(a))
# print(next(a))
# print(next(a))