class Logger:

    def __init__(self, name: str):
        self.name: str = name

    def console_log(self, message: str):
        print('<{0}> {1}'.format(self.name, message))
