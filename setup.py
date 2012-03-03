from setuptools import setup, find_packages

version = "0.5"

setup(name="nose-unitfail",
      version=version,
      description="Removes the final unittest frame from the traceback used for  post-mortem debugging nose failures",
      keywords="nose",
      author="Maru Newby",
      author_email="mnewby@internap.com",
      url="https://github.com/mnewby/nose-unitfail",
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
