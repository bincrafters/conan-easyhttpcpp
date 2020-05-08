from conans import ConanFile, CMake, tools
import os


class EasyhttpcppConan(ConanFile):
    name = "easyhttpcpp"
    description = "A cross-platform HTTP client library with a focus on usability and speed"
    topics = ("conan", "easyhttpcpp", "http")
    url = "https://github.com/bincrafters/conan-easyhttpcpp"
    homepage = "https://github.com/sony/easyhttpcpp"
    license = "MIT"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    _cmake = None

    def requirements(self):
        if self.settings.os == 'Windows':
            self.requires.add('poco/1.10.0')
        else:
            self.requires.add('openssl/1.1.1f')
            self.requires.add('poco/1.10.0')

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)
            self._cmake.definitions["FORCE_SHAREDLIB"] = self.options.shared
            self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
