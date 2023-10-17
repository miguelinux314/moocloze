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
    answer: int
    weight: int = 1

    def __str__(self):
        return f"{{{self.weight}:NUMERICAL:={self.answer}}}"
