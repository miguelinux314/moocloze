#!/usr/bin/env python3
"""Use the moocloze library to produce a set of questions in Cloze/XML format
ready to be imported into a Moodle category.
"""
__author__ = "Miguel Hernández Cabronero <miguel.hernandez@uab.cat>"
__date__ = "17/10/2023"

import moocloze


def generate_sample_quiz(output_path="example_quiz.xml"):
    questions = [moocloze.Question(
        name=f"How much is {i}+{i}",
        contents=f"What is the result of {i}+{i}? {moocloze.Numerical(i + i)}")
        for i in range(3)]

    quiz = moocloze.Quiz(questions)

    quiz.to_xml_file(output_path=output_path)


if __name__ == '__main__':
    generate_sample_quiz()
