import asyncio
from dataclasses import dataclass
from googletrans import Translator
import pinyin as pyn

@dataclass
class TranslatedWord:
    translation: str
    pinyin: str


def words_to_translated_dict(words: list[str]) -> dict[str, TranslatedWord]:
    translated_words_dict = get_words_dict(words)
    get_definitions_from_dict(translated_words_dict)
    get_pinyin_from_dict(translated_words_dict)
    return translated_words_dict


def get_words_dict(words: list[str]) -> dict[str,TranslatedWord]:
    output_dict = {}
    for word in words:
        output_dict[word] = TranslatedWord(None, None)
    return output_dict


def get_definitions_from_dict(translated_words_dict):
    # output_list = []

    words = [trans for trans in translated_words_dict]

    async def translate_bulk():
        async with Translator() as translator:
            translations = await translator.translate(words, src='zh-cn', dest='en')
            for translation in translations:
                # print(translation.origin, translation.text, translation.pronunciation)
                english_trans = translation.text
                chinese_word = translation.origin
                translated_words_dict[chinese_word].translation = english_trans
                
    asyncio.run(translate_bulk())

    return translated_words_dict


def get_pinyin_from_dict(translated_words_dict):
    for word, translated in translated_words_dict.items():
        pinyin = pyn.get(word)
        translated.pinyin = pinyin

    return translated_words_dict