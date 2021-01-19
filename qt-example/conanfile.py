from conans import ConanFile, tools


class Example(ConanFile):
    name = "example"
    version = "0.0"

    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "*.cpp", "*.h", "*.pro"

    def build(self):
        self.run("qmake --version")
        self.run("qmake")
        self.run("make")


