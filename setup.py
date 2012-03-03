from setuptools import setup, find_packages

version = "0.5"

setup(name="nose-unitfailure",
      version=version,
      description="Removes unittest traceback frame from failure post-mortem debugging",
      keywords="nose",
      author="Maru Newby",
      author_email="mnewby@internap.com",
      url="https://github.com/mnewby/nose-unitfailure",
      license="Apache Software License",
      packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
      install_requires=[
          "nose",
      ],
      entry_points={
          'nose.plugins': [
              'unitfailure = noseunitfailure:UnitFailureFormatter'
              ]
          }
      )
