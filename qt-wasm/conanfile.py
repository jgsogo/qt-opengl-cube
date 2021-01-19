#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This package is almost copied from qt/5.12.0@bincrafters/stable, it should be contributed there once Conan introduces webassembly
# TODO: Read https://forum.qt.io/topic/98802/error-while-installing-qt-5-12-0-version-for-webassembly-for-linux-fedora-as-virtual-machine/2

import configparser
import os
import shutil
import sys

from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration
from conans.model import Generator


class qt(Generator):
    @property
    def filename(self):
        return "qt.conf"

    @property
    def content(self):
        return "[Paths]\nPrefix = %s" % self.conanfile.deps_cpp_info["qt"].rootpath.replace("\\", "/")


def _getsubmodules():
    config = configparser.ConfigParser()
    config.read('qtmodules.conf')
    res = {}
    assert config.sections()
    for s in config.sections():
        section = str(s)
        assert section.startswith("submodule ")
        assert section.count('"') == 2
        modulename = section[section.find('"') + 1: section.rfind('"')]
        status = str(config.get(section, "status"))
        if status != "obsolete" and status != "ignore":
            res[modulename] = {"branch": str(config.get(section, "branch")), "status": status,
                                "path": str(config.get(section, "path")), "depends": []}
            if config.has_option(section, "depends"):
                res[modulename]["depends"] = [str(i) for i in config.get(section, "depends").split()]
    return res

_submodules = _getsubmodules()


class QtWasm(ConanFile):
    name = "qt-wasm"
    version = "5.12.0"
    exports = ["qtmodules.conf",]
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    options = dict({
        # "shared": [True, False],
        "commercial": [True, False],
        # "opengl": ["no", "es2", "desktop", "dynamic"],
        # "openssl": [True, False],
        # "GUI": [True, False],
        # "widgets": [True, False],
        # "device": "ANY",
        # "cross_compile": "ANY",
        # "config": "ANY",
    }, **{module: [True, False] for module in _submodules})

    default_options = dict({
        "commercial": False,
        "qtbase": True,},
        **{module: False for module in _submodules if module != "qtbase"})

    def config_options(self):
        for module in _submodules:
            if getattr(self.options, module):
                for req in _submodules[module]["depends"]:
                    setattr(self.options, req, True)

    def configure(self):
        assert QtWasm.version == _submodules['qtbase']['branch']
        # TODO: requires a unix host system: GNU/linux, macOS, or Windows subsystem for Linux
        pass

    def build_requirements(self):
        self.build_requires("emsdk/2.0.12")

    def source(self):
        url = "http://download.qt.io/official_releases/qt/{0}/{1}/single/qt-everywhere-src-{1}" \
            .format(self.version[:self.version.rfind('.')], self.version)
        if tools.os_info.is_windows:
            tools.get("%s.zip" % url, md5='66eaa8f2ad1b8a1867458187a31d0a88')
        elif sys.version_info.major >= 3:
            tools.get("%s.tar.xz" % url, md5='af569de3eb42da4457b0897e5759dc91')
        else:  # python 2 cannot deal with .xz archives
            self.run("wget -qO- %s.tar.xz | tar -xJ " % url)
        shutil.move("qt-everywhere-src-%s" % self.version, "qt5")

    def build(self):
        self.run("em++ --version")
        
        args = ["-confirm-license", "-silent", "-nomake examples", "-nomake tests",
                "-prefix", self.package_folder]

        if self.options.commercial:
            args.append("-commercial")
        else:
            args.append("-opensource")

        if self.settings.build_type == "Debug":
            args.append("-debug")
        elif self.settings.build_type == "Release":
            args.append("-release")
        elif self.settings.build_type == "RelWithDebInfo":
            args.append("-release")
            args.append("-force-debug-info")
        elif self.settings.build_type == "MinSizeRel":
            args.append("-release")
            args.append("-optimize-size")

        for module in _submodules:
            build_module = getattr(self.options, module)
            if not build_module and os.path.isdir(os.path.join(self.source_folder, 'qt5', _submodules[module]["path"])):
                args += ["-skip", module]

        args += ["-xplatform", "wasm-emscripten"]

        def _build(make):
            with tools.environment_append({"MAKEFLAGS": "j%d" % tools.cpu_count()}):
                self.run("%s/qt5/configure %s" % (self.source_folder, " ".join(args)))
                self.run(make)
                self.run("%s install" % make)

        _build("make")

        with open('qtbase/bin/qt.conf', 'w') as f:
            f.write('[Paths]\nPrefix = ..')

    def package(self):
        self.copy("bin/qt.conf", src="qtbase")

    def package_info(self):
        if self.settings.os == "Windows":
            self.env_info.path.append(os.path.join(self.package_folder, "bin"))
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))  # need qmake in path for consumers.
