from nltk.tokenize import word_tokenize
import os

'''
Export stop_words,pos_words,neg_words
'''


def preProcessing():
    dirStopWords = './StopWords'
    dirPosNeg = './MasterDictionary'
    stop_words = set()

    for filename in os.listdir(dirStopWords):
        if filename.endswith(".txt"):
            file_path = os.path.join(dirStopWords,filename)
            try:
                with open(file_path,'r') as file:
                    for line in file:
                        # tokenize
                        tokens = word_tokenize(line)
                        if tokens:
                            stop_words.add(tokens[0].lower())
            except UnicodeDecodeError as e:
                print(f"Error decoding: {e}")
                pass


    pos_words_file = os.path.join(dirPosNeg,'negative-words.txt')
    neg_words_file = os.path.join(dirPosNeg,'positive-words.txt')

    pos_words = dict()
    neg_words = dict()

    try:
        with open(pos_words_file,'r') as file:
            for line in file:
                tokens = word_tokenize(line)
                if tokens and tokens[0] not in stop_words:
                    pos_words[tokens[0].lower()] = 0
    except UnicodeDecodeError:
        pass

    try:
        with open(neg_words_file,'r') as file:
            for line in file:
                tokens = word_tokenize(line)
                if tokens and tokens[0] not in stop_words:
                # if tokens:
                    neg_words[tokens[0].lower()] = 0
    except UnicodeDecodeError:
        pass


    return stop_words, pos_words,neg_words