# Pay no attention to that man behind the curtain!

  Running tests with nose is great!  Extending unittest.TestCase and
  unittest2.TestCase and using their assert*() methods is nifty!
  Using mocking tools is fun!

  It's a shame, though, that nose's post-mortem debugging drops one
  into the assertion or mocking method's definition rather than the
  originating call.  Sanity is achieved by executing 'u' a bunch of
  times in pdb, but what if you're too lazy?

  nose-curtain to the rescue!  Install this plugin and invoke nose thusly:

      nosetests --pdb --pdb-failure --with-curtain

  Voila! Failures and errors that were triggered by a testing library
  will now debug from the call rather than the library.

# What?

  Given the following test code:

      class TestFoo(unittest2.TestCase):

          def test_foo(self):
              self.assertFalse(True)

  And executing the test with:

      nosetests --pdb-failure

  Nose will start a post-mortem debugging session when it encounters
  the assertion failure.  Without this plugin, the active stackframe
  will be at unittest2/case.py's assertFalse method, which is not the
  source of the failure.  With the plugin, the active stackframe will
  be at test_foo as one would expect.

# I still don't get it

    Not so fast. NOT SO FAST! I'll have to give the matter a little
    thought. Go away and come back tomorrow.

# Installation

      pip install -e git+git://github.com/marun/nose-curtain.git#egg=nose-curtain

# Configuration

  The plugin filters tracebacks whose fully qualified filenames end
  with any of a list of ignored filenames.  By default, the following
  filenames are ignored:

      mox.py
      unittest.py
      unittest2/case.py

  The list of ignored filenames can be overriden by providing a value to
  curtain-filenames, either on the command line:

      nosetests --pdb --pdb-failure --with-curtain --curtain-filenames=mox.py,unitest.py,unittest2/case.py

  or in a config file like ~/.noserc:

      [nosetests]
      curtain-filenames=mox.py,unittest.py,unittest2/case.py
