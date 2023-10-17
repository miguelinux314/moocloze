#!/usr/bin/env python3
"""Usage example of the moocloze library.
"""
__author__ = "Miguel Hernández Cabronero <miguel.hernandez@uab.cat>"
__date__ = "17/10/2023"

import moocloze

def main():
    questions = [moocloze.Question(
        name=f"How much is {i}+{i}",
        contents=f"What is the result of {i}+{i}? {moocloze.Numerical(i+i)}")
        for i in range(3)]

    quiz = moocloze.Quiz(questions)

    quiz.to_xml_file(output_path="sample_quiz.xml")

if __name__ == '__main__':
    main()
