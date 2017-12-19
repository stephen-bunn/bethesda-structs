# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import os
import sys
import shutil
import setuptools

import bethesda_structs.__version__ as PACKAGE

CURDIR = os.path.abspath(os.path.dirname(__file__))

INSTALL_REQUIRES = []
SETUP_REQUIRES = []
EXTRAS_REQUIRE = {
    'dev': [
        'ptpython',
        'flake8',
        'sphinx',
        'sphinx-autodoc-typehints',
        'sphinx-readable-theme',
        'pytest',
        'pytest-cov',
        'pytest-flake8',
    ]
}


class UploadCommand(setuptools.Command):

    description = 'Build and publish package'
    user_options = []

    @staticmethod
    def status(status):
        print(('... {status}').format(**locals()))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('removing previous builds')
            shutil.rmtree(os.path.join(CURDIR, 'dist'))
        except FileNotFoundError:
            pass

        self.status('building distribution')
        os.system(('{exe} setup.py sdist').format(exe=sys.executable))

        self.status('uploading distribution')
        os.system('twine upload dist/*')

        self.status('pushing git tags')
        os.system(('git tag v{ver}').format(ver=PACKAGE.__version__))
        os.system('git push --tags')

        sys.exit()


setuptools.setup(
    name=PACKAGE.__name__,
    version=PACKAGE.__version__,
    description=PACKAGE.__description__,
    long_description=open('README.rst', 'r').read(),
    url='https://github.com/stephen-bunn/bethesda-structs',
    license=PACKAGE.__license__,
    author=PACKAGE.__author__,
    author_email=PACKAGE.__contact__,
    packages=setuptools.find_packages(),
    install_requires=INSTALL_REQUIRES,
    setup_requires=SETUP_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    keywords=[
        'bethesda',
        'filetype',
        'structures',
        'archive',
        'python36',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Natural Language :: English',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Disassemblers',
        'Topic :: Software Development :: Pre-processors',
        'Topic :: Utilities',
    ],
    cmdclass={
        'upload': UploadCommand,
    },
)
