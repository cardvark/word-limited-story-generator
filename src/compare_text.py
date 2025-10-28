# from nltk.tokenize.stanford_segmenter import StanfordSegmenter
import jieba

def compare_cn_text(word_groups, output_text):
    # takes a dict of lists of words by group, compares output text against word groups.
    # returns a dict that includes
        # whether all words in output text are in the word_groups,
        # breakdown of counts of unique words represented in each group.
        # list of words that are not included in any group.

    # seg = StanfordSegmenter()
    # seg.default_config('zh')

    # word_segments = seg.segment(output_text)

    # jieba.enable_paddle()

    # extract word segments using jieba.
    word_segments = jieba.cut(output_text, cut_all=False)
    # print("/ ".join(word_segments)) 

    