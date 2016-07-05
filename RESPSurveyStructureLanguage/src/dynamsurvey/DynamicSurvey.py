#                                                                             | Character #79 - Do not exceed
'''
Dynamic survey base module
Created on Jun 30, 2016

Interprets XML file containing survey structure (.ssl)
and communicates with a display program via local protocols

@author: Hunter Damron
'''

import xml.etree.ElementTree as ET
import js2py
from collections import OrderedDict

class Survey(object):
    """
    Survey tree made up of question blocks containing questions
    """
    
    def __init__(self, survey_path):
        """
        Creates the survey tree from path to XML survey structure
        
        :param survey_path: relative or absolute path to XML file (.ssl)
        :return: returns an instance of the survey class based on the file
        """
        
        self.docTree = ET.parse(survey_path).getroot()
        
        #: relevance threshold above which questions are relevant
        self.threshold = "TODO"
        
        #: relevance threshold below which questions can be eliminated entirely
        self.mandatory_threshold = "TODO"
        
        #: loads questions into root (instance of QuestionBlock)
        self.questionTree = load_questions(self.docTree)
        
        init_scripting(self.questionTree, self.genScope())
            
        
        """
        !!! Lots of stuff to do here !!!
        """
        
#         TODO __repr__()
#     def __repr__(self):
#         """
#         Creates string representation of survey
#         
#         Formatted in a tree showing the id's of each question and question block
#         """
#         return tree_display_gen(self.question_tree)
    
    def __iter__(self):
        """
        Piggy backs on recursive yieldfrom() to create linear iterator
        """
        for item in yieldfrom(self.question_tree):
            yield item
    
    def search(self, question_id):
        """
        Gets question and index by question id
        """
        index = 0
        for item in self:
            if item.id() == question_id:
                return item, index
            index += 1
            
    def get(self, index):
        """
        Gets question at the specified index in the tree or None otherwise
        
        :param index: index of question in linear shape
        :return: returns the question
        """
        i = index - 1
        for item in self:
            if i == 0:
                return item
            i -= 1
        return None
        
    def canTerminate(self):
        """
        Calculates if the survey can be finished and report data
        
        Runs through all questions remaining and if all relevances are below the 
        mandatory_threshold, returns true
        :return: Returns true if all questions are below mandatory_threshold
        """
        # TODO
        pass
    
    def genScope(self):
        """
        Generates scope of survey
        
        :return: Returns dictionary with names including
            -Questions
            -Variables
            -Sensors
        """
        # TODO iterate through survey and get all mappings
        pass
        
    # TODO
    pass

def load_questions(root):
    """
    Loads the question tree from the root element of the XML tree
    
    :return: Returns a root element (instance of QuestionBlock containing
            all elements in the tree)
    """
    return _load_block(root)
    
def _load_block(branchElement):
    """
    Loads the elements in branchElement into the block
    
    :param branch_element: XML doc element to be loaded
    :return: Returns a QuestionBlock containing the loaded branch
    """
    branch = QuestionBlock()
    for item in branchElement:
        pass
    # TODO
    pass
    
def init_scripting(root, param_scope):
    """
    Finds default-script tag and initializes context based on the value
    
    :param root: Document root (to find default-script)
    :param scope: Dictionary containing scope for execution
    :return: Returns (script-type string, scope)
    """
    #: script-type and scope (both global)
    global script_type, scope
    script_type = root.find("script-default")
    scope = param_scope
    
    if script_type == "javascript":
        global context
        context = js2py.EvalJs(scope)
    else:
        assert script_type == "python" or script_type == None, \
                "Unusable scripting language"
        script_type = "python"

def yieldfrom(item):
    """
    Creates a linear iterator over tree shaped survey
    
    Called recursively    
    :param item: root element of branch
    """
    for sub_item in item:
        if isinstance(sub_item, dict):
            for sub_sub_item in yieldfrom(sub_item):
                yield sub_sub_item
        else:
            yield sub_item
            
def tree_display_gen(root):
    """
    Creates tree display of the root element
    
    Generates display recursively using _branch_gen()
    :param root: root QuestionBlock of tree
    :return: Returns a string representation of the tree
    """
    return _branch_gen(root)
    
def _branch_gen(element, tabs=0):
    """
    Inner recursive string generator
    
    :param element: element in tree structure (Question or QuestionBlock)
    :param prefix: string characters of upper level branches and tabs
    :return: returns recursive string representation of branch and sub branches
    """
    if isinstance(element, MyTestIterable):
        str_repr = ""
        for sub in element:
            print("   " * tabs)
            print(sub)
            str_repr = str_repr.join("   " * tabs)
            str_repr = str_repr.join(_branch_gen(element, tabs + 1))
        return str_repr
    else:
        return ("\t" * tabs).join(element)

class Question(object):
    def __init__(self, element):
        """
        Constructor uses element from XML file
        
        :param element: XML element from parsing - must contain:
            -question type
            -text (XML element with question body)
            -param: boolean script value
                * True when parameters are fulfilled
                * Defaults True if param is not included
            -relevance: float script value
                * All questions must be in similar range (preferred [0,1) )
            -mandatory: float script value
                * Relevance below which, question can be ignored
            -other requirements depend on the type
        """
        
        # Load question text (asserts that question has text element)
        textNode = element.find("text")
        assert (textNode != None), "Question must provide a text body"
        self.text = textNode.text
        
        # Load relevance script (asserts that question has relevance element)
        relevanceNode = element.find("relevance")
        assert (relevanceNode != None), "Question must provide a relevance"
        self.relevance = relevanceNode.text
        
        # Load prereqs if available or True if not
        prereqs = element.findall("prereq")
        self.prereq = "True"
        if(len(prereqs) > 0):
            self.prereq = prereqs[0].text
            for item in prereqs[1:-1]:
                self.prereq.join(" and %s" % item)
        
        mandatoryNode = element.find("mandatory")
        if mandatoryNode != None:
            mandatoryNode = mandatoryNode.text
        
        """
        !! More to do here !!
        """
    
    def relevance(self):
        """
        Returns the evaluated relevance of the question
        """
        return evaluate(self.relevance)
    
    def mandatory(self):
        """
        Returns the evaluated mandatory value of the question
        """
        return evaluate(self.mandatory)
    
    # TODO
    pass

class QuestionBlock(OrderedDict):
    # TODO
    pass

class Input(object):
    # TODO
    pass

class MyTestIterable(QuestionBlock):
    """
    Class designed to test methods designed for QuestionBlock
    """
    def __init__(self, name, *args):
        self.items = list(args)
        self.name = name
        
    def __iter__(self):
        for item in self.items:
            yield item
            
    def __len__(self):
        return len(self.items)
    
    def __repr__(self):
        return self.name
    
    def id(self):
        return self.name
    
def evaluate(script):
    """
    Evaluates string script after replacing variables with usable values
    
    :return: Returns the result of the evaluation
    """
    if script_type == "javascript":
        return context.eval(script)
    else:
        return 
    # TODO Once you figure out how variables are going to be treated
    pass

def disp(element, tabs=0):
    print("- %s - beginning display" % tabs)
    msg = ""
    for item in element:
        prefix = "   " * tabs
        print("%s%s" % (prefix, item))
        if isinstance(item, MyTestIterable):
#             if(disp(item, tabs + 1) is None):
#                 print("#    %s of type %s produces None" % (item, type(item).__name__))
            msg = msg.join("%s%s\n%s\n" % (prefix, item, disp(item, tabs + 1)))
        else:
            msg = msg.join("%s%s\n" % (prefix, item))
    return msg

def printdisp(element, tabs=0):
    print("- %s - beginning display" % tabs)
    for item in element:
        prefix = "   " * tabs
        print("%s%s" % (prefix, item))
        if isinstance(item, MyTestIterable):
            print("%s%s\n%s\n" % (prefix, item.id(), disp(item, tabs + 1)))
        else:
            print("%s%s\n" % (prefix, item))

if __name__ == '__main__':
    test_list = MyTestIterable("root", 4, 9, 9, 
                               MyTestIterable("branch1", "st", 
                                              MyTestIterable("sub branch 1", "|", "intermission", 
                                                             MyTestIterable("sub sub 1", "interintermission"), 
                                                             MyTestIterable("sub sub 2", "another...", "intermission"),
                                                             "|"), "ing"), 9, 7)
#     for thing in yieldfrom(test_list):
#         print(thing)
#     for item in test_list:
#         print(item)
#     print(tree_display_gen(test_list))
#     printdisp(test_list)
#     disp(test_list, 1)
    docTree = ET.parse("file.xml").getroot()
    ET.dump(docTree)
    