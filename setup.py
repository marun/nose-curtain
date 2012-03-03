# Copyright 2012 Maru Newby <mnewby@thesprawl.net>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from setuptools import setup, find_packages

version = "0.1"

setup(name="nose-unitfail",
      version=version,
      description="Removes the final unittest frame from the traceback used for post-mortem debugging nose failures",
      keywords="nose",
      author="Maru Newby",
      author_email="mnewby@thesprawl.net",
      url="https://github.com/marun/nose-unitfail",
      license="Apache Software License",
      packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
      install_requires=[
          "nose",
      ],
      entry_points={
          'nose.plugins': [
              'unitfail = noseunitfail:UnitFailureFormatter'
              ]
          }
      )
