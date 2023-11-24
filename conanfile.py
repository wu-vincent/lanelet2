from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import copy

from lanelet2_python.src.lanelet2 import __version__


class Lanelet2Conan(ConanFile):
    name = "lanelet2x"
    version = __version__

    # Optional metadata
    license = "BSD"
    url = "https://github.com/wu-vincent/lanelet2"
    description = (
        "Your favorite map handling framework for automated driving, now standalone and with cross-platform support."
    )

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True]}
    default_options = {
        "shared": False,
        "fPIC": True,
        "boost/*:shared": True,
        "boost/*:without_python": False,
    }
    without_boost_components = [
        "atomic",
        "chrono",
        "container",
        "context",
        "contract",
        "coroutine",
        "date_time",
        "exception",
        "fiber",
        "filesystem",
        "graph",
        "iostreams",
        "json",
        "locale",
        "log",
        "math",
        "mpi",
        "nowide",
        "random",
        "regex",
        "stacktrace",
        "system",
        "test",
        "thread",
        "timer",
        "type_erasure",
        "url",
        "wave",
    ]
    default_options.update((f"boost/*:without_{component}", True) for component in without_boost_components)

    proj_list = [
        "lanelet2_core",
        "lanelet2_io",
        "lanelet2_matching",
        "lanelet2_projection",
        "lanelet2_traffic_rules",
        "lanelet2_routing",
        "lanelet2_validation",
    ]

    exports_sources = ["CMakeLists.txt"] + [f"{proj}/*" for proj in proj_list]

    def requirements(self):
        self.requires("boost/[>=1.75.0 <=1.81.0]")
        self.requires("eigen/3.4.0")
        self.requires("geographiclib/1.52")
        self.requires("pugixml/1.13")
        self.requires("gtest/1.14.0")

    def build_requirements(self):
        pass
        # self.tool_requires("cmake/3.27.7")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

        for dep in self.dependencies.values():
            # for auditwheel, delocate and (or) delvewheel
            copy(self, "*.dylib*", dep.cpp_info.libdirs[0], str(self.build_path / "lib"))
            copy(self, "*.so*", dep.cpp_info.libdirs[0], str(self.build_path / "lib"))
            copy(self, "*.dll", dep.cpp_info.bindirs[0], str(self.build_path / "lib"))

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = list(reversed(self.proj_list))
