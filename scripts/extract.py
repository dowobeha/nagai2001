#!/usr/bin/env python3.9

from collections import namedtuple
import re
import sys
from typing import List


class ExtractedGloss:

    def __init__(self, *, document: str, sentence: int, lines: [str]):
        self.document: str = document
        self.sentence: int = sentence
        self.orthographicWords: List[str] = list()
        self.phoneticWords: List[str] = list()
        self.glossedWords: List[str] = list()
        self.underlyingWords: List[str] = list()
        underlyingWords = list()
        underlyingPattern = re.compile('<\s*')
        at_beginning = True
        while len(lines) > 3:
            if at_beginning:
                self.orthographicWords.extend(lines.pop(0).split()[1:])
                at_beginning = False
            else:
                self.orthographicWords.extend(lines.pop(0).split())
            self.phoneticWords.extend(lines.pop(0).split())
            self.glossedWords.extend(lines.pop(0).split())
            if lines[0]:
                if "<" in lines[0]:
                    underlyingWords.extend(underlyingPattern.sub("<", lines.pop(0)).split())
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
                    self.freeTranslation = translation
                else:
                    print(f"ERROR:\tRedefining translation \"{self.freeTranslation}\" to \"{translation}\"")
                    sys.exit(-1)
        for underlyingWord in underlyingWords:
            firstLetters = underlyingWord[1:5]
            start = len(self.underlyingWords)
            for phoneticWord in self.phoneticWords[start:]:  # str
                if phoneticWord.startswith(firstLetters):
                    self.underlyingWords.append(underlyingWord)
                else:
                    self.underlyingWords.append("")
        if not self.underlyingWords:
            self.underlyingWords = [''] * len(self.orthographicWords)

        if not (len(self.orthographicWords) == len(self.phoneticWords) and
                len(self.orthographicWords) == len(self.glossedWords) and
                len(self.orthographicWords) == len(self.underlyingWords)):
            print(f"ERROR:\t{self.document}.{self.sentence}\tMismatch" +
                  f"\t{len(self.orthographicWords)}" +
                  f"\t{len(self.phoneticWords)}" +
                  f"\t{len(self.glossedWords)}" +
                  f"\t{len(self.underlyingWords)}")
            print(self.orthographicWords)
            print(self.phoneticWords)
            print(self.glossedWords)
            print(self.underlyingWords)
            sys.exit(-1)

        for word in self.orthographicWords:
            print(word)

    def __str__(self):
        # lines = '\n'.join(self.lines)
        return f"==============================\nSentence {self.document}.{self.sentence}\n"


def extractGlosses(input_file: str) -> [ExtractedGloss]:
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
    return glosses


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage:\t{sys.argv[0]} in.txt")
        sys.exit(-1)
    else:
        result = extractGlosses(input_file=sys.argv[1])  # extract(input_file=sys.argv[1], output_file=sys.argv[2])
        # print(len(result))
