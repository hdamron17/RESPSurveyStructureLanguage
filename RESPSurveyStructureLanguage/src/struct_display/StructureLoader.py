'''
Created on Jun 23, 2016

@author: ei-student
'''

import xml.dom.minidom as parser
import string
import re
# import Tkinter as tk

class Survey(object):
    def __init__(self, fileName, customFormat=None, defaultFormat="DefaultQuestionFormat.xml"):
        self.docTree = parser.parse(fileName).documentElement
        self.questionFormatTree = parser.parse(defaultFormat).documentElement
        self.customFormatTree = parser.parse(customFormat).documentElement if (customFormat != None) else None
        scriptType = self.docTree.getElementsByTagName("script-default")[0].firstChild.data
        if(scriptType == None): 
            # JavaScript will be default in later implementations
            scriptType = "text/javascript"
        imports(self.docTree, scriptType)
        functions(self.docTree, scriptType)
        scripts(self.docTree, scriptType)
        self.languages = languages(self.docTree)
        self.questionTree = questions(self.docTree, order='linear')
        global variables
        variables = dict()
        variables['beans'] = 5
        print(variables)
        
    def __repr__(self):
        return "{Survey %s, %s" % (self.languages, self.questionTree)
        
class Question(object):
    # prereq and relevance are passed as strings to be evaluated multiple times
    def __init__(self, text, prereq, relevanceStr):
        self.text = text
        self.response = None
        self.prereq = prereq
        self.relevanceStr = relevanceStr
        
    def answer(self, answer):
        self.response = answer
        
    def filled(self):
        return self.response != None
    
    def relevance(self):
        if eval(self.prereq):
            return eval(self.relevanceStr)
        else:
            return -1
        
    def __repr__(self):
        return "(%s : %s)" (self.text, self.response)
    
        
class QuestionBlock(object):
    def __init__(self, order="linear"):
        self.questions = []
        self.order = order
    
    def add(self, question):
        self.questions.append(question)
    
    def __repr__(self):
        return "%s" % self.questions
    
# Uses insertion sort algorithm using recalculated relevance
def sortByRelevance(questionList):
    relevances = []
    for question in questionList:
        relevances.append(question.relevance())
    for i in range(0, len(questionList)):
        newIndex = i
        while newIndex > 0 and relevances[newIndex] > relevances[newIndex-1]:
            newIndex -= 1
        if newIndex != i:
            moveRelevance = relevances.pop(i)
            moveQuestion = questionList.pop(i)
            relevances.insert(newIndex, moveRelevance)
            questionList.insert(newIndex, moveQuestion)
    return questionList, relevances

def runScript(scriptElement, scriptType):
    assert scriptType == "python", "Scripting has not been enabled"
    script = scriptElement.firstChild.data
    whitespace = re.search("^\s*", script).group().lstrip("\r\n")
    
    script = string.replace(script, "\n%s" % whitespace, "\n")
    exec(script)
    
def imports(root, scriptType):
    assert scriptType == "python", "Scripting has not been enabled"
    imports = root.getElementsByTagName("import")
    for item in imports:
        namespace = item.getAttribute("name")
        if(namespace):
            exec("global {1}\nimport {0} as {1}".format(item.firstChild.data, namespace))
        else:
            exec("global {0}\nimport {0}".format(item.firstChild.data))
            
def scripts(root, scriptType):
    assert scriptType == "python", "Scripting has not been enabled"
    scripts = root.getElementsByTagName("script")
    for item in scripts:
        runScript(item, scriptType)
        
def functions(root, scriptType):
    assert scriptType == "python", "Scripting has not been enabled"
    functs = root.getElementsByTagName("funct")
    for item in functs:
        name = item.getAttribute("id")
        script = "def %s(" % name
        for param in item.getElementsByTagName("param")[:-1]:
            script = "%s%s, " % (script, param.firstChild.data)
        script = "%s%s):\n" % (script, item.getElementsByTagName("param")[-1].firstChild.data)
        body = "\n%s" % item.getElementsByTagName("body")[0].firstChild.data
        
        whitespace = re.search("^\s*", body).group().lstrip("\r\n")
        body = string.replace(body, "\n%s" % whitespace, "\n\t")
        
        script = "%s%s" % (script, body.rstrip())
        exec(script, globals())
        
        
def languages(root):
    languages = root.getElementsByTagName("languages")[0].getElementsByTagName("language")
    langs = []
    for item in languages:
        langs.append(item.firstChild.data)
    return langs

def questions(root, order="linear", lang=None):
    print("Loading %s" % root.getAttribute("id"))
    questions = QuestionBlock()
    for element in root.getElementsByTagName("*"):
        # TODO find a more efficient way to do this because this is dumb
        if element.parentNode == root:
            print(questions)
            if element.tagName == "question": 
                print("Adding question")
                questions.add(Question(element.getElementsByTagName("text"), 
                                       element.getElementsByTagName("prereq"), 
                                       element.getElementsByTagName("relevance")))
                print("")
            if element.tagName == "block":
                print("Adding block")
                print("|%s|" % element.getElementsByTagName("question"))
                newBlock = questions(element, element.getAttribute("order"), element.getAttribute("lang"))
                print(newBlock)
                questions.add(newBlock)
                print("")
    return questions
    
def switch(value, dictionary, default=None):
    for item in dictionary:
        if value == item:
            return dictionary[item]
    return default

if __name__ == '__main__':
    example = Survey("file.xml")
    raw_input("Press enter to terminate...")
    print(example)