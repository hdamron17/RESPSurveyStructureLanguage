'''
Created on Jun 23, 2016

@author: ei-student
'''

import xml.dom.minidom as parser
import string, re

class Survey(object):
    def __init__(self, fileName, customFormat=None, defaultFormat="DefaultQuestionFormat.xml"):
        self.docTree = parser.parse(fileName)
        self.questionTree = parser.parse(defaultFormat)
        self.customTree = parser.parse(customFormat) if (customFormat != None) else None
        scriptType = self.docTree.getElementsByTagName("script-default")[0].childNodes[0].data
        imports(self.docTree, scriptType)
        scripts(self.docTree, scriptType)
        self.languages = languages(self.docTree)
        
        
class Question(object):
    def __init__(self, text):
        self.text = text
        self.response = None
        
    def answer(self, answer):
        self.response = answer
        
    def filled(self):
        return self.response != None
        
        
class QuestionBlock(object):
    def __init__(self):
        pass
        # TODO
        
            
def runScript(scriptElement, scriptType):
    assert scriptType == "python", "Scripting has not been enabled"
    script = scriptElement.childNodes[0].data
    whitespace = re.search("^\s*", script).group().lstrip("\r\n")
    
    script = string.replace(script, "\n%s" % whitespace, "\n")
    exec(script)
    
def imports(root, scriptType):
    assert scriptType == "python", "Scripting has not been enabled"
    imports = root.getElementsByTagName("import")
    for item in imports:
        namespace = item.getAttribute("name")
        if(namespace):
            exec("global {1}\nimport {0} as {1}".format(item.childNodes[0].data, namespace))
        else:
            exec("global {0}\nimport {0}".format(item.childNodes[0].data))
            
def scripts(root, scriptType):
    assert scriptType == "python", "Scripting has not been enabled"
    scripts = root.getElementsByTagName("script")
    for item in scripts:
        runScript(item, scriptType)
        
def languages(root):
    languages = root.getElementsByTagName("languages")[0].getElementsByTagName("language")
    langs = []
    for item in languages:
        langs.append(item.childNodes[0].data)
    return langs

def questions(root, order="linear", lang=None):
    blocks = root.getElementsByTagName("block")
    questions = root.getElementsByTagName("question")
    
def switch(value, dictionary, default=None):
    for item in dictionary:
        if value == item:
            return dictionary[item]
    return default

if __name__ == '__main__':
    thing = Survey("file.xml")