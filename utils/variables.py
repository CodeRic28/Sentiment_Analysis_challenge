from .preProcess import preProcessing
from nltk.tokenize import word_tokenize, sent_tokenize
import os

'''
    Export ANALYSIS_METRICS
'''

stop_words, pos_words, neg_words = preProcessing()

dir_output_art = './output_articles'
SMALL = 0.000001

# Calculate Polarity Score Function
def calculatePolarity(positive_score,negative_score):
    return (positive_score - negative_score) / ((positive_score + negative_score) + SMALL)

# Calculate Subjective score
def calculateSubjectivity(positive_score,negative_score):
    return (positive_score + negative_score) / ((len(pos_words) + len(neg_words)) + SMALL)

def analyticsMetrics(dir='./output_articles'):
    ANALYSIS_METRICS = []
    for filename in os.listdir(dir):
        total_words = 0
        n_chars = 0

        # Initializing Variables
        POSITIVE_SCORE = NEGATIVE_SCORE = POLARITY_SCORE = SUBJECTIVITY_SCORE = \
            FOG_INDEX = AVERAGE_SENTENCE_LENGTH = PCT_COMPLEX_WORDS = AVG_WORDS_PER_SENT = COMPLEX_WORDS = \
            CLEAN_WORDS = SYLLABLE_PER_WORD = PERS_PRONOUNS = AVG_WORD_LEN = 0

        if filename.endswith(".txt"):
            file_path = os.path.join(dir, filename)

            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        # tokenize
                        tokens = word_tokenize(line)
                        sent_tokens = sent_tokenize(line)

                        vowels = set('aeiou')
                        punc = set('!?.,')
                        pronouns = ['I','we','my','ours','us']
                        vowel_count = 0
                        for token in tokens:
                            if token[0].lower() not in stop_words:
                                total_words += 1
                                if char not in punc:
                                    CLEAN_WORDS+=1
                            if token in pos_words:
                                pos_words[token] += 1
                                POSITIVE_SCORE += 1
                            if token in neg_words:
                                neg_words[token] += 1
                                NEGATIVE_SCORE += 1
                            for char in token[0].lower():
                                if char in vowels:
                                    vowel_count+=1
                                    if not token[0].endswith('es') and not token[0].endswith('ed'):
                                        SYLLABLE_PER_WORD+=1
                                if(vowel_count >2):
                                    COMPLEX_WORDS += 1
                            if token[0] in pronouns:
                                PERS_PRONOUNS+=1
                            n_chars += len(token[0])
                    if(len(sent_tokens) != 0 and total_words!=0):
                        AVERAGE_SENTENCE_LENGTH = total_words/len(sent_tokens)
                        PCT_COMPLEX_WORDS = COMPLEX_WORDS/total_words
                        AVG_WORD_LEN = n_chars / total_words
                        AVG_WORDS_PER_SENT = total_words / len(sent_tokens)
                    FOG_INDEX = 0.4 * (AVERAGE_SENTENCE_LENGTH + PCT_COMPLEX_WORDS)
            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")
            POLARITY_SCORE = calculatePolarity(POSITIVE_SCORE,NEGATIVE_SCORE)
            SUBJECTIVE_SCORE = calculateSubjectivity(POSITIVE_SCORE,NEGATIVE_SCORE)

            ANALYSIS_METRICS.append([POSITIVE_SCORE,NEGATIVE_SCORE,round(POLARITY_SCORE,2),
                                     round(SUBJECTIVE_SCORE,2),round(AVERAGE_SENTENCE_LENGTH,2),
                                     round(PCT_COMPLEX_WORDS,2),round(FOG_INDEX,2),round(AVG_WORDS_PER_SENT,2),
                                     COMPLEX_WORDS,CLEAN_WORDS,SYLLABLE_PER_WORD,PERS_PRONOUNS,round(AVG_WORD_LEN,2)])

    return ANALYSIS_METRICS
