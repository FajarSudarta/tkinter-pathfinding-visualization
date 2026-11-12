
Variable = None
def Share_Func(Share):
    global Variable
    Variable = Share
    print(Variable)
    return Variable

def Read_Value():
    return Variable