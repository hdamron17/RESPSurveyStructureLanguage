'''
Created on Jun 23, 2016

@author: ei-student
'''

import xml.dom.minidom as parser
import xml.etree.ElementTree as ET
import re
# import Tkinter as tk

from struct_base.QuestionsList import QuestionBlock, Question

class DepricatedSurvey(object):
    "Depreciated survey from using XML with DOM"
    
    def __init__(self, fileName, customFormat=None, defaultFormat="DefaultQuestionFormat.xml"):
        "Constructor for depricated survey"
        
        self.docTree = parser.parse(fileName).documentElement
        # TODO change questionFormatTree and CustomFormatTree to load modules from path instead of XML files
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
        
class Survey(object):
    "Survey class to house the XML structure of the document for processing"
    
    def __init__(self, fileName, customFormat=None, defaultFormat="DefaultQuestionFormat.xml"):
        """Loads the XML document into the structure along with custom questions and the default questions
        
        :param fileName: absolute or relative path to the question structure (with .ssl extension)
        :param customFormat: path to """
        
        self.docTree = ET.parse(fileName).getroot()
        self.questionFormatTree = ET.parse(defaultFormat).getroot()
        self.customFormatTree = ET.parse(customFormat) if (customFormat != None) else None
        self.scriptType = self.docTree.find("script-default")
        if(self.scriptType == None):
            # JavaScript will be default in later implementations
            self.scriptTyp = "text/javascript"
        self.languages = languages(self.docTree)
        self.questionTree = questions(self.docTree, order="linear")
        
    def __repr__(self):
        return "{Survey %s, %s" % (self.languages, self.questionTree)
    
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
    
    script = script.replace("\n%s" % whitespace, "\n")
    exec(script) # @UndefinedVariable
    
def imports(root, scriptType):
    assert scriptType == "python", "Scripting has not been enabled"
    imports = root.getElementsByTagName("import")
    for item in imports:
        namespace = item.getAttribute("name")
        if(namespace):
            exec("global {1}\nimport {0} as {1}".format(item.firstChild.data, namespace)) # @UndefinedVariable
        else:
            exec("global {0}\nimport {0}".format(item.firstChild.data)) # @UndefinedVariable
            
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
        body = body.replace("\n%s" % whitespace, "\n\t")
        
        script = "%s%s" % (script, body.rstrip())
        exec(script, globals()) # @UndefinedVariable
        
        
# def languages(root):
#     languages = root.getElementsByTagName("languages")[0].getElementsByTagName("language")
#     langs = []
#     for item in languages:
#         langs.append(item.firstChild.data)
#     return langs

def languages(root):
    languages = root.find("languages")
    return languages.findall("language")

# def questions(root, order="linear", lang=None):
#     print("Loading %s" % root.getAttribute("id"))
#     questions = QuestionBlock()
#     for element in root.getElementsByTagName("*"):
#         # TODO find a more efficient way to do this because this is dumb
#         if element.parentNode == root:
#             print(questions)
#             if element.tagName == "question": 
#                 print("Adding question")
#                 questions.add(Question(element.getElementsByTagName("text"), 
#                                        element.getElementsByTagName("prereq"), 
#                                        element.getElementsByTagName("relevance")))
#                 print("")
#             if element.tagName == "block":
#                 print("Adding block")
#                 print("|%s|" % element.getElementsByTagName("question"))
#                 newBlock = questions(element, element.getAttribute("order"), element.getAttribute("lang"))
#                 print(newBlock)
#                 questions.add(newBlock)
#                 print("")
#     return questions

def questions(root, order="linear", lang=None):
    print("Loading %s" % root.attrib['id'])
    block = QuestionBlock(order, lang)
    for element in root:
        if(element.tag == "question"):
            prereqs = element.findall("prereq")
            prereq = "True"
            if(len(prereqs) > 0):
                prereq = prereqs[0].text
                for item in prereqs[1:-1]:
                    prereq.join(" and %s" % item)
            print("prereq : %s" % prereq)
            relevanceNode = element.find("relevance")
            relevance = relevanceNode.text if (relevanceNode != None) else None
            block.add(Question(element.find("text").text, prereq, relevance))
        if(element.tag == "block"):
            print("Adding block")
            newRoot = element
            newOrder = element.attrib["order"] if "order" in element.attrib else "linear"
            newLang = element.attrib["lang"] if ("lang" in element.attrib) else None
            newBlock = questions(newRoot,  newOrder, newLang)
            block.add(newBlock)
    print("Finished block : %s" % block)
    return block
    
def switch(value, dictionary, default=None):
    for item in dictionary:
        if value == item:
            return dictionary[item]
    return default

if __name__ == '__main__':
    testQTree = questions(ET.parse("file.xml").getroot(), order="linear", lang=None)
    print("tree : %s" % testQTree)
#     example = Survey("file.xml")
#     raw_input("Press enter to terminate...")
#     print(example)