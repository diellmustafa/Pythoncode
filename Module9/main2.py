def add(x, y):
    return x + y


def concatenate(x, y):
    return str(x) + str(y)



def operate(operation, x, y):
    """

    :param This is an operation that needs to be performed:
    :param The first operand:
    :param The second operand:
    :return The result of the operation:
    """
    return operation(x, y)

result_sum = operate(add, 3, 5)
result_concatenate = operate(concatenate, 3, 5)
print("Result of sum", result_sum)
print("Result of concatenation", result_concatenate)