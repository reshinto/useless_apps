ops = {
  "+": (lambda a, b: a + b),
  "-": (lambda a, b: a - b),
  "*": (lambda a, b: a * b),
  "/": (lambda a, b: a / b)
}

def eval(expression):
    tokens = expression.split()
    stack = []

    for token in tokens:
        if token in ops:
            arg2 = stack.pop()
            print(f"arg2: {arg2}")
            arg1 = stack.pop()
            print(f"arg1: {arg1}")
            result = ops[token](arg1, arg2)
            print(f"result: {result}")
            stack.append(result)
            print(f"token in ops stack {stack}")
        else:
            stack.append(int(token))
            print(f"token not in ops stack {stack}")
    return stack.pop()


print(eval("1 2 + "))
# (1 + 2) * 4
print(eval("4 1 2 + *"))
# (1+2) * 990 + 1000
print(eval("1000 990 1 2 + * +"))
