import glob

from conan import ConanFile
from conan.tools.apple import is_apple_os
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import copy

__version__ = "1.2.1"


class Lanelet2Conan(ConanFile):
    name = "lanelet2"
    version = __version__

    # Optional metadata
    license = "BSD"
    url = "https://github.com/wu-vincent/lanelet2x"
    description = (
        "Your favorite map handling framework for automated driving, now standalone and with cross-platform support."
    )

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True]}
    default_options = {
        "shared": True,
        "fPIC": True,
        "boost/*:shared": True,
        "boost/*:without_python": False,
    }
    without_boost_components = [
        "chrono",
        "container",
        "context",
        "contract",
        "coroutine",
        "date_time",
        "exception",
        "fiber",
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
        "test",
        "thread",
        "timer",
        "type_erasure",
        "url",
        "wave",
    ]
    default_options.update((f"boost/*:without_{component}", True) for component in without_boost_components)

    project_libs = [
        "lanelet2_core",
        "lanelet2_io",
        "lanelet2_traffic_rules",
        "lanelet2_projection",
        "lanelet2_routing",
        "lanelet2_matching",
        "lanelet2_validation",
    ]

    exports_sources = ["CMakeLists.txt", "lanelet2_*/*"]

    def requirements(self):
        self.requires("boost/[>=1.75.0 <=1.81.0]")
        self.requires("eigen/3.4.0")
        self.requires("geographiclib/1.52")
        self.requires("pugixml/1.13")
        self.test_requires("gtest/1.14.0")

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

        rpath = self.source_path / "build" / "lib"
        for dep in self.dependencies.values():
            # for auditwheel, delocate and (or) delvewheel
            copy(self, "*.dylib*", dep.cpp_info.libdirs[0], str(rpath))
            copy(self, "*.so*", dep.cpp_info.libdirs[0], str(rpath))
            copy(self, "*.dll", dep.cpp_info.bindirs[0], str(rpath))

        if is_apple_os(self):
            for file_path in glob.glob(str(rpath / "libboost_*.dylib")):
                command = f'install_name_tool -add_rpath @loader_path "{file_path}"'
                self.run(command)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.test()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = []
        for lib in self.project_libs:
            lib_name = lib if self.options.shared else f"{lib}-static"
            self.cpp_info.components[lib].libs = [lib_name]
            self.cpp_info.components[lib].set_property("cmake_target_name", lib.replace("lanelet2_", "lanelet2::"))

        self.cpp_info.components["lanelet2_io"].requires = [
            "lanelet2_core",
        ]
        self.cpp_info.components["lanelet2_traffic_rules"].requires = [
            "lanelet2_core",
        ]
        self.cpp_info.components["lanelet2_projection"].requires = [
            "lanelet2_core",
            "lanelet2_io",
        ]
        self.cpp_info.components["lanelet2_routing"].requires = [
            "lanelet2_core",
            "lanelet2_traffic_rules",
        ]
        self.cpp_info.components["lanelet2_matching"].requires = [
            "lanelet2_core",
            "lanelet2_io",
            "lanelet2_projection",
            "lanelet2_traffic_rules",
        ]
        self.cpp_info.components["lanelet2_validation"].requires = [
            "lanelet2_core",
            "lanelet2_io",
            "lanelet2_projection",
            "lanelet2_traffic_rules",
            "lanelet2_routing",
        ]
