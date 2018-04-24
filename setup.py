# Copyright (c) 2018 Stephen Bunn (stephen@bunn.io)
# MIT License <https://choosealicense.com/licenses/mit/>

import os
import sys
import codecs
import shutil
import setuptools

from bethesda_structs import __version__

INSTALL_REQUIRES = ["construct", "multidict", "attrs", "lz4"]
SETUP_REQUIRES = []
EXTRAS_REQUIRE = {
    "dev": [
        "ptpython",
        "flake8",
        "sphinx",
        "sphinx-autodoc-typehints",
        "pytest",
        "pytest-cov",
        "pytest-flake8",
        "pytest-sugar",
    ]
}


class UploadCommand(setuptools.Command):

    description = "Build and publish package"
    user_options = []

    @staticmethod
    def status(status):
        print("... {0}".format(status))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("removing previous builds")
            shutil.rmtree(
                os.path.join(os.path.abspath(os.path.dirname(__file__)), "dist")
            )
        except FileNotFoundError:
            pass

        self.status("building distribution")
        os.system("{0} setup.py sdist".format(sys.executable))

        self.status("uploading distribution")
        os.system("twine upload dist/*")

        self.status("pushing git tags")
        os.system("git tag v{0}".format(__version__.__version__))
        os.system("git push --tags")

        sys.exit()

long_description = ''
with codecs.open("README-PYPI.rst", encoding="utf-8") as fp:
    long_description = '\n' + fp.read()

setuptools.setup(
    name=__version__.__name__,
    version=__version__.__version__,
    description=__version__.__description__,
    long_description=long_description,
    url=__version__.__repo__,
    license=__version__.__license__,
    author=__version__.__author__,
    author_email=__version__.__contact__,
    install_requires=INSTALL_REQUIRES,
    setup_requires=SETUP_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    include_package_data=True,
    packages=setuptools.find_packages(exclude=["tests.*", "tests"]),
    keywords=["bethesda", "filetype", "structures", "archive", "python36", "construct"],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Developers",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Natural Language :: English",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Disassemblers",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Utilities",
    ],
    cmdclass={"upload": UploadCommand},
)
