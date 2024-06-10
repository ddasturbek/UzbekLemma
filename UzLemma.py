# Read all Part-of-speech lemmas other than verb and noun
mOlmosh = list(open('suzlar/mustaqil__olmosh.txt', 'r').read().split('\n'))
mRavish = list(open('suzlar/mustaqil__ravish.txt', 'r').read().split('\n'))
mSifat = list(open('suzlar/mustaqil__sifat.txt', 'r').read().split('\n'))
mSon = list(open('suzlar/mustaqil__son.txt', 'r').read().split('\n'))

oModal = list(open('suzlar/oraliq__modal.txt', 'r').read().split('\n'))
oTaqlid = list(open('suzlar/oraliq__taqlid.txt', 'r').read().split('\n'))
oUndov = list(open('suzlar/oraliq__undov.txt', 'r').read().split('\n'))

yBoglovchi = list(open('suzlar/yordamchi__boglovchi.txt', 'r').read().split('\n'))
yKomakchi = list(open('suzlar/yordamchi__komakchi.txt', 'r').read().split('\n'))
yYuklama = list(open('suzlar/yordamchi__yuklama.txt', 'r').read().split('\n'))


def change_apostrophe(text):
    # Replace all apos. to unique apos.
    text = text.replace(chr(96), chr(39))  # ord("`") -> ord("'")
    text = text.replace(chr(699), chr(39))  # ord("ʻ") -> ord("'")
    text = text.replace(chr(700), chr(39))  # ord("ʼ") -> ord("'")
    text = text.replace(chr(8216), chr(39))  # ord("‘") -> ord("'")
    text = text.replace(chr(8217), chr(39))  # ord("’") -> ord("'")
    return text


def read_raw_text():
    # Read raw_text and prepare
    raw_txt = open('corpus.txt', 'r', encoding='utf-8-sig').read()
    raw_txt = change_apostrophe(raw_txt)
    punctuations = '!"#$%&()*+,–./:;<=>?@[\]^_`{|}~“”'
    for punc in punctuations:
        raw_txt = raw_txt.replace(punc, '')
    words = raw_txt.split()
    return words


# Create txt file for save results
fw = open('results.txt', 'w+', encoding='utf-8')


def find_suffix(suffixes):
    # Find suffixes from word
    # son = ['ta', 'tadan', 'tacha', 'ov', 'ovi', 'ovlab', 'ovlashib', 'ovlon', 'ala', 'larcha', 'lar', 'lab', 'nchi', 'inchi']
    # ravish = ['roq']
    # sifat = ['roq', 'ish', "g'ish", 'mtir', 'imtir', 'gina']
    # olmosh_ot = ['ni', 'n', 'i', 'ning', 'ka', 'ga', 'qa', 'da', 'dan']

    pos_suffixes = [['ta', 'tadan', 'tacha', 'ov', 'ovi', 'ovlab', 'ovlashib', 'ovlon', 'ala', 'larcha', 'lar', 'lab', 'nchi', 'inchi'],
                    ['roq'],
                    ['roq', 'ish', "g'ish", 'mtir', 'imtir', 'gina'],
                    ['ni', 'n', 'i', 'ning', 'ka', 'ga', 'qa', 'da', 'dan'],
                    ['dir'],
                    ['mi']]
    k = 0
    for p_s in pos_suffixes:
        for suffix in p_s:
            if len(suffixes) >= len(suffix):
                tf = True
                for i in range(len(suffix)):
                    if suffix[i] != suffixes[i]:
                        tf = False
                if tf:
                    suffixes = suffixes[len(suffix):]
                    k += 1

    if k == 0:
        return False
    else:
        return True


def find_lemma(word):
    # Find lemma using our new model (algorithm)
    pres = [pre for pre in mOlmosh if pre.startswith(word[:2])]
    pres.extend([pre for pre in mRavish if pre.startswith(word[:2])])
    pres.extend([pre for pre in mSifat if pre.startswith(word[:2])])
    pres.extend([pre for pre in mSon if pre.startswith(word[:2])])
    lemma = ''
    suffix = True
    for pre in pres:
        if pre.split('\\')[0] == word:
            lemma = word
            break
        for i in range(2, len(word)):
            if i < len(pre):
                if pre[i] == '\\' and len(pre.split('\\')[0]) >= len(lemma):
                    lemma = pre.split('\\')[0]
                    suffixes = word[i:]
                    suffix = find_suffix(suffixes)
                    if i != len(pre) - 1:
                        pre = pre[:i] + pre[i + 1:]
                if word[i] != pre[i]:
                    break
    return lemma, suffix


if __name__ == '__main__':
    # Main method. Program start here
    words = read_raw_text()
    exceptions = list(open('suzlar/istisnolar.txt', 'r').read().split('\n'))
    count_lemma = i = 0
    while i < len(words):
        if len(words[i]) == 1:
            one_word_lemma = ['a', 'e', 'i', 'o', 'u']
            if words[i].lower() in one_word_lemma:
                fw.write(f"1 {words[i]} - {words[i].lower()}\n")
                count_lemma += 1
            else:
                fw.write(f"0 {words[i]}\n")
            i += 1
        elif len(words[i]) == 2:
            two_word_lemma = ['ah', 'ba', 'bu', 'eh', 'ey', 'ha', 'he', 'ie', 'ma', 'me', 'na', 'ne', 'oh', 'oq', 'oz',
                              'to', 'uh', 'uv', 'va', 'yo']
            if words[i].lower() in two_word_lemma:
                fw.write(f"1 {words[i]} - {words[i].lower()}\n")
                count_lemma += 1
            else:
                fw.write(f"0 {words[i]}\n")
            i += 1
        else:
            if words[i].lower() in exceptions:
                fw.write(f"1 {words[i]} - {words[i].lower()}\n")
                count_lemma += 1
            else:
                if words[i].lower() in yYuklama:
                    fw.write(f"1 {words[i]} - {words[i].lower()}\n")
                    count_lemma += 1
                elif words[i].lower() in yKomakchi:
                    fw.write(f"1 {words[i]} - {words[i].lower()}\n")
                    count_lemma += 1
                elif words[i].lower() in yBoglovchi:
                    fw.write(f"1 {words[i]} - {words[i].lower()}\n")
                    count_lemma += 1
                elif words[i].lower() in oUndov:
                    fw.write(f"1 {words[i]} - {words[i].lower()}\n")
                    count_lemma += 1
                elif words[i].lower() in oModal:
                    fw.write(f"1 {words[i]} - {words[i].lower()}\n")
                    count_lemma += 1
                elif words[i].lower() in oTaqlid:
                    fw.write(f"1 {words[i]} - {words[i].lower()}\n")
                    count_lemma += 1
                else:
                    lemma, suffix = find_lemma(words[i].lower())
                    if lemma != '' and suffix:
                        fw.write(f"1 {words[i]} - {lemma}\n")
                        count_lemma += 1
                    else:
                        fw.write(f"0 {words[i]}\n")
            i += 1
    fw.write(f"\nNumber of lemmas: {count_lemma}")
    fw.close()
