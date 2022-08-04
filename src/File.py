import ast


class File:
    filename = ''
    encoding = 'utf-8'
    file = None
    current_mode = ''
    root_path = '../'

    def __init__(self, filename: str):
        self.filename = self.root_path + filename

    def write(self, content: str):
        self.open_file('w+')
        self.file.write(content)

    def open_file(self, mode):
        if self.file is None or self.current_mode != mode:
            if self.file is not None:
                self.file.close()
            self.file = open(self.filename, mode, encoding=self.encoding)

    def append(self, content: str):
        self.open_file('a')
        self.file.write(content)

    def append_line(self, content):
        self.append(content + '\n')

    def read(self):
        self.open_file('r')
        return self.file.read()

    def read_literal_eval(self):
        content = self.read()
        if not content:
            raise ValueError('Файл ' + self.filename + 'пустой')

        return ast.literal_eval(content)

    def get_filename(self) -> str:
        return self.filename

    def __del__(self):
        if self.file is not None:
            self.file.close()

