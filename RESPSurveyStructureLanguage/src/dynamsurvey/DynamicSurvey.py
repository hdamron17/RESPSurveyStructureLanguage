#                                                                             | Character #79 - Do not exceed
'''
Dynamic survey base module
Created on Jun 30, 2016

Interprets XML file containing survey structure (.ssl)
and communicates with a display program via local protocols

@author: hdamron
'''

from collections import Iterable

class Survey(object):
    """
    Survey tree made up of question blocks containing questions
    """
    
    def __init__(self, survey_path):
        """
        Creates the survey tree from path to XML survey structure
        
        :param survey_path: relative or absolute path to XML file (.ssl extension)
        :return: returns an instance of the survey class based on the file
        """
        
        #: relevance threshold above which questions are relevant
        self.threshold = "TODO"
        
        #: relevance threshold below which questions can be eliminated entirely
        self.mandatory_threshold = "TODO"
        
        #: root of question tree (instance of QuestionBlock)
        self.question_tree = "TODO"
        
    def __repr__(self):
        """
        Creates string representation of survey
         
        Formatted in a tree showing the id's of each question and question block
        """
        return tree_display_gen(self.question_tree)
    
    def __iter__(self):
        for item in yieldfrom(self.question_tree):
            yield item
    
    def load_questions(self, root):
        """
        Loads the question tree from the root element of the XML tree
        """
        
    def canTerminate(self):
        """
        Calculates if the survey can be finished and report data
        
        Runs through all questions remaining and if all relevances are below the 
        mandatory_threshold, returns true
        :return: Returns true if all questions are below mandatory_threshold
        """
        # TODO
        pass
    
    
    
    # TODO
    pass

def yieldfrom(item):
    for sub_item in item:
        if isinstance(sub_item, MyTestIterable):
            for sub_sub_item in yieldfrom(sub_item):
                yield sub_sub_item
        else:
            yield sub_item
            
def tree_display_gen(root):
    str_repr = root.id()
    for item, i in zip(root, range(0, len(root))):
        str_repr.join(branch_gen(item, i < len(root) - 1))
    return str_repr
    
def branch_gen(element, hasNext, prefix=""):
    """
    Creates a string tree display
    
    :param element: element in tree structure (Question or QuestionBlock)
    :param prefix: string characters of upper level branches and tabs
    :return: returns recursive string representation of branch and sub branches
    
    main
     |-branch
     |  |-sub branch
     |     |-Leaf
     |     |-Leaf
     |-branch
     |  |-sub branch
     |  |  |-sub sub branch
     |  |-sub branch
     |-branch
    """    
    str_repr = "%s-%s\n" % (prefix, element.id())
    if not isinstance(element, MyTestIterable): # TODO Change to QuestionBlock
        return str_repr
    new_prefix = prefix.join("  |")
    for item, i in zip(element[:-1], range(len(element))):
        str_repr.join(branch_gen(item, i < len(element) - 1), new_prefix)
    return str_repr
                    
class MyTestIterable(object):
    def __init__(self, name, *args):
        self.items = list(args)
        self.name = name
        
    def __iter__(self):
        for item in self.items:
            yield item
            
    def __len__(self):
        return len(self.items)
    
    def id(self):
        return self.name

class Question(object):
    # TODO
    pass

if __name__ == '__main__':
    test_list = MyTestIterable("root", 4, 9, 9, 
                               MyTestIterable("branch1", "st", 
                                              MyTestIterable("sub branch 1", "|", "intermission", 
                                                             MyTestIterable("sub sub 1", "interintermission"), 
                                                             MyTestIterable("sub sub 2", "another...", "intermission"),
                                                             "|"), "ing"), 9, 7)
#     for thing in yieldfrom(test_list):
#         print(thing)
    print(tree_display_gen(test_list))