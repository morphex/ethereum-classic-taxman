import traceback

def dump_exception(exception):
    print("Exception:")
    try:
        print(type(exception))
        print((exception.args,))
        print(exception)
        traceback.print_last()
    except:
        print("Exception during printing of exception")
