import unittest
import os


def run_tests():
    loader = unittest.TestLoader()

    current_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir=current_dir, pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)


if __name__ == '__main__':
    run_tests()
