import os

from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.cmake import CMake, cmake_layout


class Lanelet2ExampleConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def layout(self):
        cmake_layout(self)

    def _is_executable(self, file_path):
        if self.settings.os == "Windows":
            return file_path.endswith(".exe")
        else:
            return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

    def test(self):
        if can_run(self):
            bindir = os.path.join(self.cpp.build.bindir)
            for file in os.listdir(bindir):
                full_path = os.path.join(bindir, file)
                if self._is_executable(full_path):
                    cmd = full_path if self.settings.os == "Windows" else "./" + file
                    self.run(cmd, env="conanrun")
