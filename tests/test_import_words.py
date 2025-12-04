import unittest
import src.import_words as iw

class TestBasicTranslate(unittest.TestCase):
    def test_001_translate(self):
        test_words = ["你", "麻烦", "听话", "所以"]

        translated_words_dict = iw.get_words_dict(test_words)
        print(translated_words_dict)

        iw.get_definitions_from_dict(translated_words_dict)
        print(translated_words_dict)

        iw.get_pinyin_from_dict(translated_words_dict)
        print(translated_words_dict)

    def test_002_test_words_to_translated(self):
        test_words = ["你", "麻烦", "听话", "所以"]
        translated_words_dict = iw.words_to_translated_dict(test_words)
        print(translated_words_dict)