#!/usr/bin/env python3.9

from collections import namedtuple
import re
import sys
from typing import List

import xigt.codecs.xigtxml
from xigt import XigtCorpus, Igt, Tier, Item, Metadata, Meta


class ExtractedGloss:

    def toIGT(self):
        orthographicWords = Tier(type="orthographicWords", id=f"{self.document}.s{self.sentence:02}.ow",
                                 items=[Item(id=f"{self.document}.s{self.sentence:02}.ow{wordID:02}", text=word)
                                        for (wordID, word) in enumerate(self.orthographicWords, start=1)])

        phoneticWordsAPA = Tier(type="phonemicWordsAPA", id=f"{self.document}.s{self.sentence:02}.pwa",
                                items=[Item(id=f"{self.document}.s{self.sentence:02}.pwa{wordID:02}", text=word)
                                       for (wordID, word) in enumerate(self.phonemicWordsAPA, start=1)])

        phoneticWordsIPA = Tier(type="phonemicWordsIPA", id=f"{self.document}.s{self.sentence:02}.pwi",
                                items=[Item(id=f"{self.document}.s{self.sentence:02}.pwi{wordID:02}", text=word)
                                       for (wordID, word) in enumerate(self.phonemicWordsIPA, start=1)])

        underlyingWordsAPA = Tier(type="underlyingWordsAPA", id=f"{self.document}.s{self.sentence:02}.uwa",
                                  items=[Item(id=f"{self.document}.s{self.sentence:02}.uwa{wordID:02}", text=word)
                                         for (wordID, word) in enumerate(self.underlyingWordsAPA, start=1)])

        underlyingWordsIPA = Tier(type="underlyingWordsIPA", id=f"{self.document}.s{self.sentence:02}.uwi",
                                  items=[Item(id=f"{self.document}.s{self.sentence:02}.uwi{wordID:02}", text=word)
                                         for (wordID, word) in enumerate(self.underlyingWordsIPA, start=1)])

        glossedWords = Tier(type="glossedWords", id=f"{self.document}.s{self.sentence:02}.gw",
                            items=[Item(id=f"{self.document}.s{self.sentence:02}.gw{wordID:02}", text=word)
                                   for (wordID, word) in enumerate(self.glossedWords, start=1)])

        engTranslation = Tier(type="engTranslation", id=f"{self.document}.s{self.sentence:02}.eng",
                              items=[Item(id=f"{self.document}.s{self.sentence:02}.eng01",
                                          text=self.engTranslationClose),
                                     Item(id=f"{self.document}.s{self.sentence:02}.eng02",
                                          text=self.engTranslationFree)],)

        return Igt(id=f"{self.document}.s{self.sentence:02}",
                   tiers=[orthographicWords,
                          phoneticWordsAPA, phoneticWordsIPA,
                          underlyingWordsAPA, underlyingWordsIPA,
                          glossedWords, engTranslation])
#                  tiers=[phoneticWords])

    def __init__(self, *, document: str, sentence: int, lines: [str]):
        if document == "I":
            self.document = "WaghiyiNagai2001.t01"
        elif document == "II":
            self.document = "WaghiyiNagai2001.t02"
        elif document == "III":
            self.document = "WaghiyiNagai2001.t03"
        elif document == "IV":
            self.document = "WaghiyiNagai2001.t04"
        elif document == "V":
            self.document = "WaghiyiNagai2001.t05"
        elif document == "VI":
            self.document = "WaghiyiNagai2001.t06"
        elif document == "VII":
            self.document = "WaghiyiNagai2001.t07"
        elif document == "VIII":
            self.document = "WaghiyiNagai2001.t08"
        elif document == "IX":
            self.document = "WaghiyiNagai2001.t09"
        elif document == "X":
            self.document = "WaghiyiNagai2001.t10"
        elif document == "XI":
            self.document = "WaghiyiNagai2001.t11"
        elif document == "XII":
            self.document = "WaghiyiNagai2001.t12"
        elif document == "XIII":
            self.document = "WaghiyiNagai2001.t13"
        elif document == "XIV":
            self.document = "WaghiyiNagai2001.t14"
        else:
            self.document: str = document
        self.engTranslationFree = ""
        self.sentence: int = sentence
        self.orthographicWords: List[str] = list()
        self.phonemicWordsAPA: List[str] = list()
        self.phonemicWordsIPA: List[str] = list()
        self.glossedWords: List[str] = list()
        self.underlyingWordsAPA: List[str] = list()
        self.underlyingWordsIPA: List[str] = list()
        underlyingWords = list()
        underlyingPattern = re.compile('<\s*')
        at_beginning = True
        while len(lines) > 3:
            if at_beginning:
                self.orthographicWords.extend(lines.pop(0).split()[1:])
                at_beginning = False
            else:
                self.orthographicWords.extend(lines.pop(0).split())
            self.phonemicWordsAPA.extend(lines.pop(0).split())
            self.glossedWords.extend(lines.pop(0).split())
            if lines[0]:
                if "<" in lines[0]:
                    underlyingWords.extend(underlyingPattern.sub('', lines.pop(0)).split())
                else:
                    print(f"ERROR:\t{self.document}.{self.sentence}\tNo < in line \"{lines[0]}\"")
                    sys.exit(-1)

            if not lines[0]:
                lines.pop(0)
        while len(lines) > 0:
            line = lines.pop(0)
            translation = None
            if line:
                if not translation:
                    translation = line
                    self.engTranslationClose = translation
                else:
                    print(f"ERROR:\tRedefining translation \"{self.engTranslationClose}\" to \"{translation}\"")
                    sys.exit(-1)
        for underlyingWord in underlyingWords:
            #firstLetters = underlyingWord[1:5]
            firstLetters = underlyingWord[0:3]
            start = len(self.underlyingWordsAPA)
            for phoneticWord in self.phonemicWordsAPA[start:]:  # str
                if phoneticWord.startswith(firstLetters):
                    self.underlyingWordsAPA.append(underlyingWord)
                    break
                else:
                    self.underlyingWordsAPA.append(None)
        while len(self.underlyingWordsAPA) < len(self.orthographicWords):
            self.underlyingWordsAPA.append('')
#        if not self.underlyingWords:
#            self.underlyingWords = [''] * len(self.orthographicWords)

        if not (len(self.orthographicWords) == len(self.phonemicWordsAPA) and
                len(self.orthographicWords) == len(self.glossedWords) and
                len(self.orthographicWords) == len(self.underlyingWordsAPA)):
            print(f"ERROR:\t{self.document}.{self.sentence}\tMismatch" +
                  f"\t{len(self.orthographicWords)}" +
                  f"\t{len(self.phonemicWordsAPA)}" +
                  f"\t{len(self.glossedWords)}" +
                  f"\t{len(self.underlyingWordsAPA)}")
            print(self.orthographicWords)
            print(self.phonemicWordsAPA)
            print(self.glossedWords)
            print(self.underlyingWordsAPA)
            sys.exit(-1)

        for i in range(len(self.phonemicWordsAPA)):
            if self.phonemicWordsAPA[i]:
                self.phonemicWordsIPA.append(replace(self.phonemicWordsAPA[i], ipa=True))
                self.phonemicWordsAPA[i] = replace(self.phonemicWordsAPA[i], ipa=False)

        for i in range(len(self.underlyingWordsAPA)):
            if self.underlyingWordsAPA[i]:
                self.underlyingWordsIPA.append(replace(self.underlyingWordsAPA[i], ipa=True))
                self.underlyingWordsAPA[i] = replace(self.underlyingWordsAPA[i], ipa=False)
            else:
                self.underlyingWordsIPA.append(None)

        # for word in self.orthographicWords:
        #    print(word)

    def __str__(self):
        # lines = '\n'.join(self.lines)
        return f"==============================\nSentence {self.document}.{self.sentence}\n"


def replace(s: str, ipa=False) -> str:
    central_vowel = "\u0259"                        # LATIN SMALL LETTER SCHWA

    voiceless_velar_fricative = "\u0078"            # LATIN SMALL LETTER X
    voiced_velar_fricative = "\u0263"               # LATIN SMALL LETTER GAMMA

    ipa_voiceless_uvular_fricative = "\u03C7"       # GREEK SMALL LETTER CHI
    ipa_voiced_uvular_fricative = "\u0281"          # LATIN LETTER SMALL CAPITAL INVERTED R

    apa_voiced_rhotic = "\u0072"                    # LATIN SMALL LETTER R
    ipa_voiced_rhotic = "\u027B"                    # LATIN SMALL LETTER TURNED R WITH HOOK
    ipa_voiceless_rhotic = "\u0282"                 # LATIN SMALL LETTER S WITH HOOK

    voiceless_lateral = "\u026C"                    # LATIN SMALL LETTER L WITH BELT

    labial_nasal = "\u006D"                         # LATIN SMALL LETTER M
    alveolar_nasal = "\u006E"                       # LATIN SMALL LETTER N
    velar_nasal = "\u014B"                          # LATIN SMALL LETTER ENG

    combining_dot_above = "\u0307"                  # COMBINING DOT ABOVE
    combining_dot_below = "\u0323"                  # COMBINING DOT BELOW
    combining_ring_above = "\u030A"                 # COMBINING RING ABOVE
    combining_ring_below = "\u0325"                 # COMBINING RING BELOW
    rounded = "\u02B7"                              # MODIFIER LETTER SMALL W
    result = str(s)

    # Schwa
    if True:
        result = result.replace("´", f"{central_vowel}")

    # Voiceless lateral
    if True:
        result = result.replace("¬", f"{voiceless_lateral}")

    # Voiceless rhotic
    if ipa:
        result = result.replace("r∞", f"{ipa_voiceless_rhotic}")
    else:
        result = result.replace("r∞", f"{apa_voiced_rhotic}{combining_ring_below}")

    # Voiced rhotic
    if ipa:
        # result = result.replace("r", f"{ipa_voiced_rhotic}")
        pass
    else:
        pass

    # Voiceless rounded velar  nasal
    if True:
        result = result.replace("N∞w", f"{velar_nasal}{combining_ring_above}{rounded}")

    # Voiceless         velar  nasal
    if True:
        result = result.replace("N∞", f"{velar_nasal}{combining_ring_above}")

    # Voiced    rounded velar  nasal
    if True:
        result = result.replace("Nw", f"{velar_nasal}{rounded}")

    # Voiced            velar  nasal
    if True:
        result = result.replace("N", f"{velar_nasal}")

    # Voiceless       alveolar nasal
    if True:
        result = result.replace("n∞", f"{alveolar_nasal}{combining_ring_below}")

    # Voiceless         labial nasal
    if True:
        result = result.replace("m∞", f"{labial_nasal}{combining_ring_below}")

    # Voiceless rounded uvular fricative
    if ipa:
        result = result.replace("x5w", f"{ipa_voiceless_uvular_fricative}{rounded}")
    else:
        result = result.replace("x5w", f"{voiceless_velar_fricative}{combining_dot_below}{rounded}")

    # Voiceless         uvular fricative
    if ipa:
        result = result.replace("x5",  f"{ipa_voiceless_uvular_fricative}")
    else:
        result = result.replace("x5",  f"{voiceless_velar_fricative}{combining_dot_below}")

    # Voiced    rounded uvular fricative
    if ipa:
        result = result.replace("V%w%", f"{ipa_voiced_uvular_fricative}{rounded}")
        result = result.replace("V%w",  f"{ipa_voiced_uvular_fricative}{rounded}")
    else:
        result = result.replace("V%w%",  f"{voiced_velar_fricative}{combining_dot_above}{rounded}")
        result = result.replace("V%w",   f"{voiced_velar_fricative}{combining_dot_above}{rounded}")

    # Voiced            uvular fricative
    if ipa:
        result = result.replace("V%", f"{ipa_voiced_uvular_fricative}")
    else:
        result = result.replace("V%",   f"{voiced_velar_fricative}{combining_dot_above}")

    # Voiceless rounded velar  fricative
    if True:
        result = result.replace("xw", f"{voiceless_velar_fricative}{rounded}")

    # Voiceless         velar  fricative
    if True:
        result = result.replace("x", f"{voiceless_velar_fricative}")

    # Voiced    rounded velar  fricative
    if True:
        result = result.replace("Vw", f"{voiced_velar_fricative}{rounded}")

    # Voiced            velar  fricative
    if True:
        result = result.replace("V", f"{voiced_velar_fricative}")

    return result


def extractGlosses(input_file: str) -> XigtCorpus:
    lines = [line.strip() for line in open(input_file, "rt")]
    docID = lines[0].split()[0].strip(".")
    Position = namedtuple('Position', ['document', 'sentence', 'start', 'end'])
    start_positions = [Position(document=docID, sentence=0, start=0, end=None)]

    for line_number, line in enumerate(lines):
        try:
            if line:
                sentence_number = int(line.split()[0].strip("."))
                position = Position(document=docID, sentence=sentence_number, start=line_number, end=None)
                start_positions.append(position)
        except ValueError:
            pass
    last_i = len(start_positions) - 1
    glosses = []
    for i in range(len(start_positions)):
        if i < last_i:
                glosses.append(ExtractedGloss(document=docID,
                                          sentence=start_positions[i].sentence,
                                          lines=lines[start_positions[i].start:start_positions[i+1].start]))
        else:
            glosses.append(ExtractedGloss(document=docID,
                                          sentence=start_positions[i].sentence,
                                          lines=lines[start_positions[i].start:]))

    ess = Meta(type="language",
               attributes={'name': 'St. Lawrence Island Yupik',
                           'iso-689-3': 'ess',
                           'tiers': 'essSentence ' +
                                    'orthographicWords ' +
                                    'phonemicWordsAPA ' +
                                    'phonemicWordsIPA ' +
                                    'underlyingWordsAPA ' +
                                    'underlyingWordsIPA'})

    eng = Meta(type="language",
               attributes={'iso-689-3': 'eng',
                           'name': 'English',
                           'tiers': 'engTranslation ' +
                                    'glossedWords'})

    speaker = Meta(type="author", text="Della Waghiyi")

    author = Meta(type="author", text="Kayo Nagai")

    book = Meta(type="source",
                id="WaghiyiNagai2001",
                text="Mrs. Della Waghiyi's St. Lawrence Island Yupik Texts " +
                     "with Grammatical Analysis by Kayo Nagai. " +
                     "Dec 2001. " +
                     "Endangered Languages of the Pacific Rim Publication Series A2-006. " +
                     "ISSN 1346-082X.")

    orthographicWordsComment = Meta(type="comment",
                                    text="The orthographicWords tier contains Yupik words " +
                                         "in the St. Lawrence Island Yupik orthography " +
                                         "with morpheme boundaries marked by dashes.")

    phonemicWordsAPAComment = Meta(type="comment",
                                   text="The phonemicWordsAPA tier contains Yupik words " +
                                        "represented using an Americanist phonetic alphabet (APA) notation " +
                                        "with morpheme boundaries marked by dashes.")

    phonemicWordsIPAComment = Meta(type="comment",
                                   text="The phonemicWordsIPA tier contains Yupik words " +
                                        "represented using the International Phonetic Alphabet (IPA) notation " +
                                        "with morpheme boundaries marked by dashes.")

    underlyingWordsAPAComment = Meta(type="comment",
                                     text="In some cases, an interlinear gloss in the text presents " +
                                          "an underlying lexical phonemic representation for a Yupik word " +
                                          "that differs from that presented in the phonemicWordsAPA tier. " +
                                          "In such cases, the underlyingWordsAPA tier contains such underlying forms " +
                                          "in APA notation with morpheme boundaries marked by dashes.")

    underlyingWordsIPAComment = Meta(type="comment",
                                     text="In some cases, an interlinear gloss in the text presents " +
                                          "an underlying lexical phonemic representation for a Yupik word " +
                                          "that differs from that presented in the phonemicWordsIPA tier. " +
                                          "In such cases, the underlyingWordsIPA tier contains such underlying forms " +
                                          "in IPA notation with morpheme boundaries marked by dashes.")

    version = Meta(type="version", text="0.0.3")

    return XigtCorpus(id="WaghiyiNagai2001", igts=[gloss.toIGT() for gloss in glosses],
                      metadata=[Metadata(metas=[ess, eng, speaker, author, book,
                                                orthographicWordsComment,
                                                phonemicWordsAPAComment, phonemicWordsIPAComment,
                                                underlyingWordsAPAComment, underlyingWordsIPAComment,
                                                version])])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage:\t{sys.argv[0]} in.txt")
        sys.exit(-1)
    else:
        results = extractGlosses(input_file=sys.argv[1])  # extract(input_file=sys.argv[1], output_file=sys.argv[2])
        xigt.codecs.xigtxml.dump(sys.stdout, results)
        # print(len(result))
        # for sentence in results:
        #     print(f"{sentence}\t{str(sentence.toIGT())}")
