
b:int = 5
def test(a, b):
    c = a + b
    print("Hello World")
    return c

a:int = 4
print(f"Hello {a}")
print(a)

if b > a:
    print("b is greater than a")
elif b == a:
    print("a is equal to b")

else:
    print("b is less than a")

arr:list = [1,2,3,4]
for i in arr:
    print(f"{arr[i-1]} nth place")

print(len(arr))

for i in range(len(arr)):
    print(arr[i])

a = 4
b = 5

while a < b:
    print("a is less than b")
    a += 1

# function to add to variables
def subtraction_to_numbers(a, b):
    return a + b

# method overloading 
def add_numbers(*args):
    return sum(args)
add_numbers(1,2,3,5)

def add_numbers(a, b):
    arr = []
    arr.append(a)
    arr.append(b)
    return sum(arr)

add_numbers(1,2)