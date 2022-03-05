import traceback

def dump_exception(exception):
    print("Exception:")
    print(type(exception))
    print((exception.args,))
    print(exception)
    traceback.print_last()
