import unittest

if __name__ == "__main__":
    suite = unittest.TestLoader().discover(".")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)