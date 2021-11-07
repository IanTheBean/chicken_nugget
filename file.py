class File:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, "r+") as file:
            contents = file.read()

        return contents

    def save(self, contents):
        with open(self.path, "r+") as file:
            file.truncate(0)
            file.write(contents)
