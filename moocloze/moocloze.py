#!/usr/bin/env python3
"""Tools to generate moodle questions in XML/Cloze format.

https://github.com/miguelinux314/moocloze

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

import random as _random
from dataclasses import dataclass as _dataclass
from typing import List as _List
from typing import Union as _Union
from pathlib import Path as _Path
import abc as _abc
import textwrap as _textwrap
import enum as _enum


@_dataclass
class Question:
    """One XML moodle question.
    """
    # Question title
    name: str
    # Question main text
    contents: str

    def to_xml_file(self, output_path: _Union[str | _Path]):
        """Save this question as a single-element Quiz in Moodle XML format, which can be
        directly imported.

        See the `moocloze.Quiz` class to save multiple questions into a single XML file.
        """
        Quiz([self]).to_xml_file(output_path=output_path)

    def __str__(self) -> str:
        """Get a string that represents this question in Moodle XML/Cloze format. Note that this
        output cannot be directly impoted by Moodle; you need to use Question.to_xml_file or
        Quiz.to_xml_file to include all necessary tags.
        """
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
    """A set of one or more questions.
    """
    # List of one or more questions comprising this quiz
    questions: _List[Question]

    def to_xml_file(self, output_path: _Union[str | _Path]):
        """Save this quiz (list of one or more questions) into Moodle Cloze/XML format.
        """
        if not self.questions:
            raise ValueError("At least one question is needed.")

        with open(output_path, "w") as output_file:
            output_file.write(str(self) + "\n")

    def __str__(self) -> str:
        """Return a string with all of this quiz's questions in Cloze/XML format, which that can
        be directly imported in Moodle.
        """
        return ('<?xml version="1.0" encoding="UTF-8"?><quiz>\n' +
                "\n\n".join(str(q) for q in self.questions) +
                "\n\n</quiz>")


class Field(_abc.ABC):
    """Base class for cloze question fields. These can be used to include different type of
    expected user inputs in Question instances.
    """

    def __str__(self) -> str:
        """Get a string that represents this field and can be embedded in the contents of a Cloze
        Question.
        """
        raise NotImplementedError


@_dataclass
class Numerical(Field):
    """A single Cloze numerical question field.
    """
    # Correct numerical value. Consider a non-zero tolerance for non-integer answers.
    answer: _Union[int | float]
    # Absolute error tolerance. For instance, if the answer is 10 and tolerance is 0.05, any
    # value between 9.95 and 10.05 will be accepted as valid by the system
    tolerance: float = 0
    # If True, any non-zero tolerance will be displayed after the input field
    show_tolerance: bool = True
    # Weight given to the response in this field. Useful when more than one field is employed.
    weight: int = 1

    def __str__(self) -> str:
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

    def __str__(self) -> str:
        self.correct_answers = [str(s) for s in self.correct_answers]
        self.incorrect_answers = [str(s) for s in self.incorrect_answers]

        if not self.correct_answers:
            raise ValueError("At least one valid correct answer is required by Moodle. "
                             "None provided.")
        s = (f"{{{self.weight}:MULTIRESPONSE"
             f"{'_' if self.horizontal or self.shuffle else ''}"
             f"{'H' if self.horizontal else ''}"
             f"{'S' if self.shuffle else ''}"
             f":")
        text_correct_tuples = [(text, True) for text in self.correct_answers]
        text_correct_tuples += [(text, False) for text in self.incorrect_answers]
        if not self.shuffle:
            text_correct_tuples = sorted(text_correct_tuples)
        s += "~".join(f"{'=' if correct else ''}{text}" for text, correct in text_correct_tuples)
        s += "}"
        return s


@_dataclass
class Multichoice(Field):
    """Multiple options, where only one is valid. Displayed as a dropdown or as a row of
    radio buttons depending on the parameters. If shuffle is not selected, answers
    are displayed in alphabetical order.
    """

    class DisplayMode(_enum.Enum):
        """Available display modes for the Multichoice field.
        """
        DROPDOWN = _enum.auto()
        HORIZONTAL_BUTTONS = _enum.auto()
        VERTICAL_BUTTONS = _enum.auto()

    # Correct answer that the user is expected to select
    correct_answer: str
    # Incorrect answers that are also shown but should not be selected by the user.
    # At least one incorrect answer is needed.
    incorrect_answers: _List[str]
    # Display orientation. Can be a dropdown menu or a horizontal or vertical radio buttons
    display_mode: DisplayMode = DisplayMode.DROPDOWN
    # If shuffle is False, options are displayed in alphabetical order.
    # Otherwise, their order is random
    shuffle: bool = False
    # Weight given to the response in this field. Useful when more than one field is employed.
    weight: int = 1

    def __str__(self):
        if not self.incorrect_answers:
            raise ValueError("At least one incorrect answer is needed")

        display_str = ""
        if self.display_mode == self.DisplayMode.HORIZONTAL_BUTTONS:
            display_str += "H"
        if self.display_mode == self.DisplayMode.VERTICAL_BUTTONS:
            display_str += "V"
        if self.shuffle:
            display_str += "S"
        if display_str:
            display_str = f"_{display_str}"

        self.correct_answer = str(self.correct_answer)
        self.incorrect_answers = [str(s) for s in self.incorrect_answers]
        text_correct_tuples = [(self.correct_answer, True)]
        text_correct_tuples += ((t, False) for t in self.incorrect_answers)
        if self.shuffle:
            _random.shuffle(text_correct_tuples)
        else:
            text_correct_tuples = sorted(text_correct_tuples)
        option_str = "~".join(f"{'=' if correct else ''}{text}"
                              for text, correct in text_correct_tuples)
        return f"{{{self.weight}:MULTICHOICE{display_str}:{option_str}}}"


@_dataclass
class ShortAnswer(Field):
    """Single short answer text.
    """
    # Exact expected answer
    answer: str
    # Weight given to the response in this field. Useful when more than one field is employed.
    weight: int = 1

    def __str__(self):
        return f"{{{self.weight}:SHORTANSWER:={self.answer}}}"
