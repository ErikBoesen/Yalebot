class Module:
    DESCRIPTION = ""
    ARGC = 0
    def __init__(self):
        print("Loaded module %s." % self.__class__.__name__)
