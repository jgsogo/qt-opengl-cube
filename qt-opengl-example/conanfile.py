from conans import ConanFile, tools


class Example(ConanFile):
    name = "example"
    version = "0.0"
    settings = "os", "compiler", "build_type", "arch"

    exports_sources = "app/*", "exe/*", "gl/*", "qt/*", "src/*", "*"

    def build(self):
        self.run("qmake --version")
        self.run("em++ --version")
        self.run("pwd")
        self.run("qmake")
        self.run("make")
