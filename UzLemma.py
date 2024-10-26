import os


def read_all_pos_lemmas():
    # Read all lemmas of Part-of-speech from dictionary

    base_dir = os.path.dirname(os.path.abspath(__file__))

    global exceptions
    exceptions = list(open(os.path.join(base_dir, 'suzlar', 'istisnolar.txt'), 'r').read().split('\n'))

    global mFel, mOlmosh, mOt, mRavish, mSifat, mSon
    mFel = list(open(os.path.join(base_dir, 'suzlar', 'mustaqil__fel.txt'), 'r').read().split('\n'))
    mOlmosh = list(open(os.path.join(base_dir, 'suzlar', 'mustaqil__olmosh.txt'), 'r').read().split('\n'))
    mOt = list(open(os.path.join(base_dir, 'suzlar', 'mustaqil__ot.txt'), 'r').read().split('\n'))
    mRavish = list(open(os.path.join(base_dir, 'suzlar', 'mustaqil__ravish.txt'), 'r').read().split('\n'))
    mSifat = list(open(os.path.join(base_dir, 'suzlar', 'mustaqil__sifat.txt'), 'r').read().split('\n'))
    mSon = list(open(os.path.join(base_dir, 'suzlar', 'mustaqil__son.txt'), 'r').read().split('\n'))

    global oModal, oTaqlid, oUndov
    oModal = list(open(os.path.join(base_dir, 'suzlar', 'oraliq__modal.txt'), 'r').read().split('\n'))
    oTaqlid = list(open(os.path.join(base_dir, 'suzlar', 'oraliq__taqlid.txt'), 'r').read().split('\n'))
    oUndov = list(open(os.path.join(base_dir, 'suzlar', 'oraliq__undov.txt'), 'r').read().split('\n'))

    global yBoglovchi, yKomakchi, yYuklama
    yBoglovchi = list(open(os.path.join(base_dir, 'suzlar', 'yordamchi__boglovchi.txt'), 'r').read().split('\n'))
    yKomakchi = list(open(os.path.join(base_dir, 'suzlar', 'yordamchi__komakchi.txt'), 'r').read().split('\n'))
    yYuklama = list(open(os.path.join(base_dir, 'suzlar', 'yordamchi__yuklama.txt'), 'r').read().split('\n'))


def change_apostrophe(text):
    # Replace all apostrophe to unique apostrophe for uzbek o' and g' letters
    text = text.replace(chr(96), chr(39))  # ord("`") -> ord("'")
    text = text.replace(chr(699), chr(39))  # ord("ʻ") -> ord("'")
    text = text.replace(chr(700), chr(39))  # ord("ʼ") -> ord("'")
    text = text.replace(chr(8216), chr(39))  # ord("‘") -> ord("'")
    text = text.replace(chr(8217), chr(39))  # ord("’") -> ord("'")
    return text


def read_raw_text(raw_txt):
    # Read and prepare raw_text
    raw_txt = change_apostrophe(raw_txt)
    punctuations = '!"#$%&()*+,–./:;<=>?@[\\]^_`{|}~“”'
    for punc in punctuations:
        raw_txt = raw_txt.replace(punc, '')
    words = raw_txt.split()
    return words


def verb_suffix(suffixes):
    # Finding verb suffuxes
    verb_suffixes = [['di', 'moqda', 'adi', 'ma', 'mas'], #bulishli-bulishsiz
                     ['gan', 'r', 'ar', 'yotgan', 'ayotgan', 'ydigan', 'adigan', 'uvchi'], #sifatdosh
                     ['b', 'ib', 'gani', 'guncha', 'gach', 'gancha', 'a'], #ravishdosh
                     ['moq', 'mak', 'ish', 'uv'], #harakat_nomi
                     ['sa', 'moqchi'], #mayl
                     ['di', 'gan', 'b', 'ib', 'yap', 'moqda', 'yotir', 'ayotir', 'yotib', 'ayotib', 'y', 'ay', 'r', 'ar', 'ur', 'gusi', 'gay'] #zamon
                     ]
    k = 0
    for v_s in verb_suffixes:
        for suffix in v_s:
            if len(suffixes) >= len(suffix):
                tf = True
                for i in range(len(suffix)):
                    if suffix[i] != suffixes[i]:
                        tf = False
                if tf:
                    suffixes = suffixes[len(suffix):]
                    k += 1

    shaxs_son = ['k', 'man', 'san', 'siz', 'di', 'dilar', 'y', 'ay', 'ylik', 'aylik', 'gin', 'sin', 'sinlar']
    for ss in shaxs_son:
        if len(suffixes) >= len(ss) and suffixes.startswith(ss) and suffixes[len(ss):] == '':
            k += 1

    if k == 0:
        return False
    else:
        return True


def verb_lemma(word):
    # Finding a verb lemma
    pres = [pre for pre in mFel if pre.startswith(word[:2].lower())]
    lemma = ''
    suffix = True
    for pre in pres:
        if pre.split('\\')[0] == word:
            lemma = word
            break
        for i in range(2, len(word)):
            if i < len(pre):
                if pre[i] == '\\':
                    if len(pre.split('\\')[0]) >= len(lemma):
                        lemma = pre.split('\\')[0]
                        suffixes = word[i:]
                        suffix = verb_suffix(suffixes)
                        pre = pre[:i] + pre[i+1:]
                if word[i] != pre[i]:
                    break
    return lemma, suffix


def pos_suffix(suffixes):
    # Finding pos suffixes
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


def pos_lemma(word):
    # Finding pos lemmas
    pres = [pre for pre in mOlmosh if pre.startswith(word[:2])]
    pres.extend([pre for pre in mOt if pre.startswith(word[:2])])
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
                    suffix = pos_suffix(suffixes)
                    if i != len(pre) - 1:
                        pre = pre[:i] + pre[i + 1:]
                if word[i] != pre[i]:
                    break
    return lemma, suffix


def lemmatize(raw_txt):
    # Main method. Program start here

    # If raw_test is empty
    if raw_txt == '':
        return raw_txt

    # If raw_text is only numbers
    if raw_txt.isdigit():
        return raw_txt

    read_all_pos_lemmas()
    words = read_raw_text(raw_txt)
    lmd_txt = list()
    i = 0
    while i < len(words):
        if len(words[i]) < 3:
            lmd_txt.append(words[i].lower())
            i += 1
        else:
            if words[i].lower() in exceptions:
                lmd_txt.append(words[i].lower())
            else:
                if words[i].lower() in yYuklama:
                    lmd_txt.append(words[i].lower())
                elif words[i].lower() in yKomakchi:
                    lmd_txt.append(words[i].lower())
                elif words[i].lower() in yBoglovchi:
                    lmd_txt.append(words[i].lower())

                elif words[i].lower() in oUndov:
                    lmd_txt.append(words[i].lower())
                elif words[i].lower() in oModal:
                    lmd_txt.append(words[i].lower())
                elif words[i].lower() in oTaqlid:
                    lmd_txt.append(words[i].lower())

                else:
                    lemma, suffix = verb_lemma(words[i].lower())
                    if lemma != '' and suffix:
                        if i == len(words) - 1:
                            lmd_txt.append(f"{lemma}moq")
                        else:
                            kfsq = ['boshla', 'chiq', 'kel', 'ket', "ko'r", 'ol', 'tashla', 'tur', 'yur']
                            for k in kfsq:
                                if words[i + 1].lower().startswith(k):
                                    lmd_txt.append(f"{words[i]} {k}moq")
                                    i += 1
                                    break
                            else:
                                lmd_txt.append(f"{lemma}moq")
                    else:
                        lemma, suffix = pos_lemma(words[i].lower())
                        if lemma != '' and suffix:
                            lmd_txt.append(f'{lemma}')
                        else:
                            kelishiklar = ['ni', 'ning', 'ga', 'qa', 'da', 'dan', 'lar', 'mi', 'si', 'gi', 'imiz']
                            for k in kelishiklar:
                                if words[i].lower().endswith(k):
                                    lemma = words[i].lower().rstrip(k)
                                    lmd_txt.append(f'{lemma}')
                                    break
                            else:
                                lmd_txt.append(words[i].lower())
            i += 1
    string = ' '.join(lmd_txt)
    return string
