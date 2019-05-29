import synonyms
import jieba
import random
import os,sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

stopwords_path = os.path.join(curdir, './data/stopwords.txt')


stopwords = open(stopwords_path, mode='r').readlines()
stopwords = [word.strip() for word in stopwords]

import re
def get_only_chars(line):

    clean_line = ""

    line = line.replace("’", "")
    line = line.replace("'", "")
    line = line.replace("-", " ") #replace hyphens with spaces
    line = line.replace("\t", " ")
    line = line.replace("\n", " ")
    line = line.lower()

    for char in line:
        if char in 'qwertyuiopasdfghjklzxcvbnm ':
            clean_line += char
        else:
            clean_line += ' '

    clean_line = re.sub(' +',' ',clean_line) #delete extra spaces
    if clean_line[0] == ' ':
        clean_line = clean_line[1:]
    return clean_line


def get_one_syn_words(word, syn_score=0.7):
    syn_words = synonyms.nearby(word)
    syn_words = [syn_words[0][i] for i, score in enumerate(syn_words[1]) if score > syn_score]
    if len(syn_words) >= 1 and syn_words != []:
        if word in syn_words:
            syn_words.remove(word)
    if len(syn_words) == 0:
        return False
    return random.choice(syn_words)

def replace_synonym(words, n):
    new_words = words.copy()
    #不在停用词表中
    random_word_list = list(set([word for word in words if word not in stopwords]))


    random.shuffle(random_word_list)

    num_replaced = 0
    for random_word in random_word_list:
        synonym_word = get_one_syn_words(random_word)
        if synonym_word:
            new_words = [synonym_word if word == random_word else word for word in new_words]
        # print("replaced", random_word, "with", synonym)
            num_replaced += 1
        if num_replaced >= n:  # only replace up to n words
            break


    # this is stupid but we need it, trust me
    sentence = ' '.join(new_words)
    new_words = sentence.split(' ')

    return new_words

########################################################################
# Random deletion
# Randomly delete words from the sentence with probability p, new word is retain word
########################################################################

def random_deletion(words, p=0.3):
    #obviously, if there's only 3 word, don't delete it
    if len(words) < 2:
        return words

    #randomly delete words with probability p
    new_words = []
    for word in words:
        r = random.uniform(0, 1)
        if r > p:
            new_words.append(word)

    #if you end up deleting all words, just return a random word
    if len(new_words) == 0:
        rand_int = random.randint(0, len(words)-1)
        return [words[rand_int]]

    return new_words

########################################################################
# Random swap
# Randomly swap two words in the sentence n times, don't need delete stopwords
########################################################################

def random_swap(words, n=1):
    new_words = words.copy()
    for _ in range(n):
        new_words = swap_word(new_words)
    return new_words

def swap_word(new_words):
    random_idx_1 = random.randint(0, len(new_words)-1)
    random_idx_2 = random_idx_1
    counter = 0
    while random_idx_2 == random_idx_1:
        random_idx_2 = random.randint(0, len(new_words)-1)
        counter += 1
        if counter > 3:
            return new_words
    new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
    return new_words

########################################################################
# Random insertion
# Randomly insert n words into the sentence
########################################################################

def random_insertion(words, n=1):
    new_words = words.copy()
    for _ in range(n):
        add_word(new_words)
    return new_words

def add_word(new_words):
    syn_words = []
    counter = 0

    while syn_words and len(syn_words) < 1:
        random_word = new_words[random.randint(0, len(new_words)-1)]
        if random_word not in stopwords:  # 不在停用词表中
            syn_words = get_one_syn_words(random_word)
            counter += 1

            if counter >= 10:
                return
    if syn_words:
        random_synonym = syn_words
        random_idx = random.randint(0, len(new_words)-1)
        new_words.insert(random_idx, random_synonym)


########################################################################
# main data augmentation function
########################################################################

def data_expansion(sentence, alpha_sr=0.1, alpha_ri=0.1, alpha_rs=0.1, p_rd=0.2, num_aug=9):
    '''
    if you set alpha_ri and alpha_rs is 0 that means use linear classifier for it, and insensitive to word location

    :param sentence: input sentence text
    :param alpha_sr: Replace synonym control param. bigger means more words are Replace
    :param alpha_ri: Random insert. bigger means more words are Insert
    :param alpha_rs: Random swap. bigger means more words are swap
    :param p_rd: Random delete. bigger means more words are deleted
    :param num_aug: How many times do you repeat each method
    :return:
    '''
    # sentence = get_only_chars(sentence)
    # words = sentence.split(' ')
    words = jieba.lcut(sentence, cut_all=False)
    words = [word for word in words if word is not '']
    num_words = len(words)
    augmented_sentences = []

    if num_words > 0:
        num_new_per_technique = int(num_aug / 4) + 1
        n_sr = max(1, round(alpha_sr * num_words))
        n_ri = max(0, round(alpha_ri * num_words))
        n_rs = max(0, round(alpha_rs * num_words))

        # sr
        for _ in range(num_new_per_technique):
            a_words = replace_synonym(words, n_sr)
            augmented_sentences.append(''.join(a_words))

        # ri
        for _ in range(num_new_per_technique):
            a_words = random_insertion(words, n_ri)
            augmented_sentences.append(''.join(a_words))

        # rs
        for _ in range(num_new_per_technique):
            a_words = random_swap(words, n_rs)
            augmented_sentences.append(''.join(a_words))

        # rd
        for _ in range(num_new_per_technique):
            a_words = random_deletion(words, p_rd)
            augmented_sentences.append(''.join(a_words))

        # augmented_sentences = [sentence for sentence in augmented_sentences]
        random.shuffle(augmented_sentences)

        # trim so that we have the desired number of augmented sentences
        if num_aug >= 1:
            augmented_sentences = augmented_sentences[:num_aug]
        else:
            keep_prob = num_aug / len(augmented_sentences)
            augmented_sentences = [s for s in augmented_sentences if random.uniform(0, 1) < keep_prob]


    # append the original sentence
    augmented_sentences.append(sentence)
    augmented_sentences = list(set(augmented_sentences))  #del duplicate
    return augmented_sentences


if __name__ == '__main__':
    # random_insertion(jieba.lcut('如果你要一起去，哪有什么用呢？'),1)
    print(data_expansion('生活里的惬意，无需等到春暖花开', alpha_ri=0, alpha_rs=0))