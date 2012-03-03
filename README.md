# nose-unitfail

  Running tests with nose is great!  Extending unittest.TestCase and
  unittest2.TestCase and using their assert*() methods is great too!

  It's a shame, though, that nose's post-mortem debugging of assertion
  failures drops one into the assertion method's definition rather
  than the assertion call.  Sanity is achieved by hitting 'u' and
  'enter', but what if you're too lazy?

  nose-unitfail to the rescue!  Install this package and invoke nose thusly:

      nosetests --pdb-failure --with-unitfail

  Voila! TestCase.assert* failures will now debug from the assertion call.
