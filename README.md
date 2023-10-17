# moocloze

Python library to populate Moodle question banks using a Cloze/XML format.

## Example
The following code 

``` 
import moocloze

questions = [moocloze.Question(
                name=f"How much is {i}+{i}",
                contents=f"What is the result of {i}+{i}? {moocloze.Numerical(i+i)}")
                for i in range(2)]

quiz = moocloze.Quiz(questions)

quiz.to_xml_file(output_path="sample_quiz.xml")
```
produces

```
<?xml version="1.0" encoding="UTF-8"?><quiz>
<question type="cloze">
    <name><text>How much is 0+0?</text></name>
    <questiontext>
    <text><![CDATA[What is the result of 0+0? {1:NUMERICAL:=0}]]></text>
    </questiontext>
    <generalfeedback>
    <text></text>
    </generalfeedback>
    <shuffleanswers>1</shuffleanswers>
</question>

<question type="cloze">
    <name><text>How much is 1+1?</text></name>
    <questiontext>
    <text><![CDATA[What is the result of 1+1? {1:NUMERICAL:=2}]]></text>
    </questiontext>
    <generalfeedback>
    <text></text>
    </generalfeedback>
    <shuffleanswers>1</shuffleanswers>
</question>

</quiz>
```



## Proposed workflow

The following workflow is proposed to populate a category of questions in a Moodle question bank:

1. Create a list of (related) Question instances.
2. Define a Quiz containing that list of questions.
3. Use that quiz's to_xml_file method to create a .xml file with the Moodle XML/Cloze format.
4. Create a category in your course question bank.
5. Import the XML file to your question bank (Question Bank -> Import -> Moodle XML format -> upload -> import )
   making sure the appropriate category is selected.

See https://docs.moodle.org/402/en/Embedded_Answers_(Cloze)_question_type for more information
on the Cloze question format.
