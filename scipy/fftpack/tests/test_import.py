"""Test possibility of patching fftpack with pyfftw.

No module source outside of scipy.fftpack should contain an import of
the form `from scipy.fftpack import ...`, so that a simple replacement
of scipy.fftpack by the corresponding fftw interface completely swaps
the two FFT implementations.

Because this simply inspects source files, we only need to run the test
on one version of Python.
"""


import sys
if sys.version_info >= (3, 4):
    from pathlib import Path
    import re
    from numpy.testing import TestCase, assert_, run_module_suite
    import scipy

    class TestFFTPackImport(TestCase):
        def test_fftpack_import(self):
            base = Path(scipy.__file__).parent
            regexp = r"\s*from.+\.fftpack import .*\n"
            for path in base.rglob("*.py"):
                if base / "fftpack" in path.parents:
                    continue
                with path.open() as file:
                    assert_(all(not re.fullmatch(regexp, line)
                                for line in file),
                            "{0} contains an import from fftpack".format(path))

    if __name__ == "__main__":
        run_module_suite(argv=sys.argv)
