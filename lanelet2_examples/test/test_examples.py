import os
import subprocess
import sys
import unittest


class Lanelet2ExamplesTestCase(unittest.TestCase):
    def test_run_py_examples(self):
        scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
        examples = [os.path.join(scripts_dir, o) for o in os.listdir(scripts_dir) if o.endswith(".py")]
        for example in examples:
            print("Running " + example)
            result = subprocess.call([sys.executable, example])
            self.assertEqual(result, 0, "Failed to execute {}".format(example))


if __name__ == "__main__":
    unittest.main()
