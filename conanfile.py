from conan import ConanFile


class Lanelet2Conan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps"

    def requirements(self):
        self.requires("boost/[>=1.75.0 <=1.81.0]")
        self.requires("eigen/3.4.0")
        self.requires("geographiclib/1.52")
        self.requires("pugixml/1.13")
        self.requires("gtest/1.14.0")

    def build_requirements(self):
        # self.tool_requires("cmake/3.22.6")
        pass
