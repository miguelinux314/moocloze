#!/usr/bin/env python3
"""Tools to generate moodle questions in XML/Cloze format.

The following workflow is proposed to populate a category of questions in a Moodle question bank:

1. Create a list of (related) Question instances.
2. Define a Quiz containing that list of questions.
3. Use that quiz's to_xml_file method to create a .xml file with the Moodle XML/Cloze format.
4. Create a category in your course question bank.
5. Import the XML file to your question bank (making sure the appropriate category is selected).

See https://docs.moodle.org/402/en/Embedded_Answers_(Cloze)_question_type for more information
on the Cloze question format.
"""
__author__ = "Miguel Hernández-Cabronero"
__since__ = "2023/10/01"

from dataclasses import dataclass as _dataclass
from typing import List as _List
import abc as _abc
import textwrap as _textwrap


@_dataclass
class Question:
    """One XML moodle question.
    """
    name: str
    contents: str

    def __str__(self):
        return _textwrap.dedent(f"""
    <question type="cloze">
        <name><text>{self.name}</text></name>
        <questiontext>
        <text><![CDATA[{self.contents}]]></text>
        </questiontext>
        <generalfeedback>
        <text></text>
        </generalfeedback>
        <shuffleanswers>1</shuffleanswers>
    </question>""").strip()


@_dataclass
class Quiz:
    """A set of moodle questions.
    """
    questions: _List[Question]

    def to_xml_file(self, output_path):
        with open(output_path, "w") as output_file:
            output_file.write(str(self) + "\n")

    def __str__(self):
        return ('<?xml version="1.0" encoding="UTF-8"?><quiz>\n' +
                "\n\n".join(str(q) for q in self.questions) +
                "\n\n</quiz>")


class Field(_abc.ABC):
    """Base class for cloze question fields. These can be used to include
    different type of expected user inputs in Question instances.
    """
    pass


@_dataclass
class Numerical(Field):
    """A single cloze numerical question field.
    """
    # Correct numerical value. Consider a non-zero tolerance for non-integer answers.
    answer: int
    # Absolute error tolerance. For instance, if the answer is 10 and tolerance is 0.05, any
    # value between 9.95 and 10.05 will be accepted as valid by the system
    tolerance: float = 0
    # If True, any non-zero tolerance will be displayed after the input field
    show_tolerance: bool = True
    # Weight given to the response in this field. Useful when more than one field is employed.
    weight: int = 1

    def __str__(self):
        s = f"{{{self.weight}:NUMERICAL:={self.answer}:{self.tolerance}}}"
        if self.show_tolerance and self.tolerance > 0:
            s += f" (\\(\\pm {self.tolerance}\\))"
        return s


@_dataclass
class Multiresponse(Field):
    """Multiple options with checkboxes, where none, some or all may be correct.
    """
    # List of answer strings that must be checked (correct)
    correct_answers: _List[str]
    # List of answer strings that must not be checked (incorrect)
    incorrect_answers: _List[str]
    # If True, answers are shown horizontally. Otherwise, vertically
    horizontal: bool = True
    # If True, answers are shuffled. Otherwise, they are displayed in alphabetical order
    shuffle: bool = True
    # Weight given to the response in this field. Useful when more than one field is employed.
    weight: int = 1

    def __str__(self):
        assert len(self.correct_answers) + len(self.incorrect_answers) > 0, \
            "At least one correct or incorrect answer must be specified"
        s = (f"{{{self.weight}:MULTIRESPONSE"
             f"{'_' if self.horizontal or self.shuffle else ''}"
             f"{'H' if self.horizontal else ''}"
             f"{'S' if self.shuffle else ''}"
             f":")
        text_correct_tuples = []
        text_correct_tuples += [(text, True) for text in self.correct_answers]
        text_correct_tuples += [(text, False) for text in self.incorrect_answers]
        if not self.shuffle:
            text_correct_tuples = sorted(text_correct_tuples)
        s += "~".join(f"{'=' if correct else ''}{text}" for text, correct in text_correct_tuples)
        s += "}"
        return s
