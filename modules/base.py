class Module:
    DESCRIPTION = ""
    ARGC = 0
    ACCESS_TOKEN = os.environ["GROUPME_ACCESS_TOKEN"]
    def __init__(self):
        print("Loaded module %s." % self.__class__.__name__)
