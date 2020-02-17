import unittest
import tool_script

class ToolScript(unittest.TestCase):

    def test_get_punctuation_for_regex(self):
        test_punc = ['\.', '/', '\?', '\-', '"', ',', '\\b']
        punc_str = tool_script.get_punctuation_for_regex(test_punc)
        expected_punc_str = '\.|/|\?|\-|"|,|\\b'
        self.assertEqual(punc_str, expected_punc_str)

if __name__ == '__main__':
    unittest.main()
    