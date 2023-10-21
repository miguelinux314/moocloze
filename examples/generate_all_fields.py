#!/usr/bin/env python3
"""Use the moocloze library to produce a single question that employs all supported fields.
"""
__author__ = "Miguel Hernández-Cabronero"
__since__ = "2023/10/21"

import moocloze
import math


def generate_question_all_fields(output_path="question_with_all_fields.xml"):
    question = moocloze.Question(
        name="Question testing all supported Cloze fields",
        contents=("This is a question testing all supported Cloze fields.<br/>"
                  "<ul>"

                  "<li><strong>moocloze.Numerical</strong>: expect integer or decimal values.<br/>"
                  "Here, exactly 10 is expected, and any other value will be considered wrong: "
                  f"{moocloze.Numerical(10)}.<br/>"
                  "In the next box, the value of \\(\\pi\\) is expected, with a tolerance of 0.0001: "
                  f"{moocloze.Numerical(math.pi, tolerance=0.0001)}. The message displaying "
                  "error tolerance can be disabled at will</li>"

                  "<li><strong>moocloze.Multiresponse</strong>: provide 1 or more options, "
                  "of which at least 1 must be correct. The user must check only those that are "
                  "correct.<br/>"
                  "Here, the user is expected to check out numbers and not letters: " +
                  str(moocloze.Multiresponse(correct_answers=[0, 1, 123],
                                             incorrect_answers=["a", "b"])) +
                  "<br/>The same question can be shown vertically and/or without "
                  "shuffling the options: " +
                  str(moocloze.Multiresponse(correct_answers=[0, 1, 123],
                                             incorrect_answers=["a", "b"],
                                             horizontal=False,
                                             shuffle=False)) +
                  "<br/>You can use the `shuffle` parameter to provide a random or lexicographic "
                  "order of options."
                  "</li>"

                  "<li><strong>moocloze.Multichoice</strong>: provide 1 correct option "
                  "and any number of incorrect options. The user must select the correct one. "
                  "Different display modes are possible. In all the following, the negative "
                  "value must be selected:<br/>As a dropdown menu (default): " +
                  str(moocloze.Multichoice(
                      correct_answer=-1,
                      incorrect_answers=[0, 5, 10])) +
                  "<br/>As a vertical set of radio buttons: " +
                  str(moocloze.Multichoice(
                      correct_answer=-1,
                      incorrect_answers=[0, 5, 10],
                      display_mode=moocloze.Multichoice.DisplayMode.VERTICAL_BUTTONS)) +
                  "<br/>As a horizontal set of radio buttons: " +
                  str(moocloze.Multichoice(
                      correct_answer=-1,
                      incorrect_answers=[0, 5, 10],
                      display_mode=moocloze.Multichoice.DisplayMode.HORIZONTAL_BUTTONS)) +
                  "<br/>You can also use the `shuffle` parameter to provide a random or "
                  "lexicographic order of options." +
                  "</li>"

                  "<li><strong>moocloze.ShortAnswer</strong>: expect a specific string from "
                  "the user. For instance, the human's best friend is expected as the input: "
                  f"{moocloze.ShortAnswer('book')}."
                  "</li>"
                  "</ul>"

                  "Note that all fields admit a `weight` parameter that determines its relative "
                  "value within the question they are displayed. For instance the following "
                  "one is 10 times as important as any of the others: " +
                  str(moocloze.Multichoice(correct_answer='choose me',
                                           incorrect_answers=['do not choose me'],
                                           weight=10)))
    )

    moocloze.Quiz([question]).to_xml_file(output_path=output_path)


if __name__ == "__main__":
    generate_question_all_fields()
