# moocloze

Python library to populate Moodle question banks using a Cloze/XML format.

It aims to provide a functionality similar to that of [PyCloze](https://github.com/cghiaus/PyCloze), 
but reducing the necessity of specific knowledge about the 
Moodle XML or Cloze formats.

Contents:
* [Installation](#installation)
* [Minimal example](#minimal_example)
* [Creating questions and importing into moodle](#workflow)
* [Full example](#full_example)
* [References](#references)

## Installation <a id="installation"/>

The `moocloze` library is available as a pip package:

```bash
pip install moocloze
```

You can then import it as a normal package in any python code:

```python
import moocloze
```

## Minimal example <a id="minimal_example"/>

The following code ([download source](https://raw.githubusercontent.com/miguelinux314/moocloze/master/examples/generate_example_quiz.py?raw=true)) 

```python 
import moocloze

questions = [moocloze.Question(
    name=f"How much is {i}+{i}",
    contents=f"What is the result of {i}+{i}? "
             f"{moocloze.Numerical(i + i)}")
    for i in range(3)]

quiz = moocloze.Quiz(questions)

quiz.to_xml_file(output_path="example_quiz.xml")
``` 

generates a file in Cloze/XML format ([download XML file](https://raw.githubusercontent.com/miguelinux314/moocloze/master/doc/sample_quiz.xml))
that can be imported in Moodle. 
Once [imported](#workflow), 3 questions are added to the bank, one of which is shown next:

![Example output of a numerical question](https://github.com/miguelinux314/moocloze/blob/master/doc/example_0plus0_screenshot.png?raw=true)


## Creating questions and importing into Moodle <a id="workflow"/>

The following workflow is proposed to add questions to a Moodle category

* In your computer:

  1. Create a list of (related) Question instances.
     ```python
     import moocloze
     questions = [moocloze.Question(name="...", contents="..."), ...]
     ```
  2. Define a Quiz containing that list of questions.
     ```python
     quiz = moocloze.Quiz(questions)
     ```
  3. Use that quiz's to_xml_file method to create a .xml file with the Moodle XML/Cloze format.
     ```python
     quiz.to_xml_file("my_questions.xml") 
     ```

* In Moodle: 

  4. Go to your course's Question bank
     ![question bank](https://github.com/miguelinux314/moocloze/blob/master/doc/moodle_question_bank.png?raw=true)
  
  5. (Optional) Go to the question Categories page and add your category
     ![categories](https://github.com/miguelinux314/moocloze/blob/master/doc/moodle_categories.png?raw=true)
  
  6. Go to the question Import page, select the category where questions are to be imported 
     (here "Raw audio file size", shown under the "General" section), upload your xml file (e.g., "my_questions.xml" in
     the example below) and press "Import":
     ![import](https://github.com/miguelinux314/moocloze/blob/master/doc/moodle_import.png?raw=true)

  8. You will be shown a confirmation page. If no errors are found, 
     you are done!

## Full example <a id="full_example"/>

You can find a [complete example](https://raw.githubusercontent.com/miguelinux314/moocloze/master/examples/generate_all_fields.py?raw=true)
that produces a single question using all supported field (response) types:

* `moocloze.Numerical` (integers or floats, with arbitrary error tolerance)
* `moocloze.Multiresponse` (one or more valid options using checkboxes)
* `moocloze.Multichoice` (one valid option among several, using dropdown menus or radio buttons)
* `moocloze.ShortAnswer` (short text)

A screenshot of the question is shown next ([see full size](https://github.com/miguelinux314/moocloze/blob/master/doc/example_all_fields_screenshot.png?raw=true)):

![import](https://github.com/miguelinux314/moocloze/blob/master/doc/example_all_fields_screenshot.png?raw=true)

## References <a id="references"/>

* See https://docs.moodle.org/402/en/Embedded_Answers_(Cloze)_question_type for more information
  on the Cloze question format.

* Check out the [PyCloze library](https://github.com/cghiaus/PyCloze) 
  and specifically this [importing tutorial](https://github.com/cghiaus/PyCloze/blob/main/Tutorial_xml2moodle.md) 
  for more details about how to import your XML files into Moodle and loading them into a Quiz/Questionnaire.
