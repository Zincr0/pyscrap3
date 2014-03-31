#Copyright 2012 Daniel Osvaldo Mondaca Seguel
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
import os
from setuptools import setup
from setuptools import find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    scripts=["bin/wscrap3", "bin/wscrap3.3"],
    name="pyscrap3",
    version="0.0.6",
    author="Daniel Mondaca",
    author_email="daniel@analitic.cl",
    description=("micro framework for web scraping"),
    license = "Apache 2.0 License",
    keywords = "web scraping",
    url = "https://github.com/Zincr0/pyscrap3",
    include_package_data = True,
    packages = find_packages('.'),
    install_requires = ["mr.bob"],
    long_description=read("README.txt"),
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",

    ],
)
