import Tkinter as tk

class Question(tk.Frame):
    # prereq and relevance are passed as strings to be evaluated multiple times
    def __init__(self, text, prereq="True", relevanceStr="1"):
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
        
    def display(self):
        # TODO This method is the tkinter display object representing the 
        # display and input for the question (only displays text for base
        # Question)
        pass
        
    def __repr__(self):
        return "(%s : %s)" % (self.text, self.response)
    
class Choice(object):
    def __init__(self, text, prereq="True", relevanceStr="1"):
        pass
    
class TextQuestion(Question):
    # TODO
    pass

class TextOpenQuestion(TextQuestion):
    # TODO
    pass

class TextNumericalQuestion(TextQuestion):
    # TODO
    pass

class ChoiceQuestion(Question):
    # TODO
    pass

class ChoiceSingleQuestion(ChoiceQuestion):
    # TODO
    pass

class ChoiceMultipleQuestion(ChoiceQuestion):
    # TODO
    pass

class VoidQuestion(Question):
    # TODO
    pass
        
class QuestionBlock(object):
    def __init__(self, order="linear", lang=None):
        self.questions = []
        self.order = order
        self.lang = lang
    
    def add(self, question):
        self.questions.append(question)
    
    def __repr__(self):
        return "%s" % self.questions
    
# Dictionary with string to question class lookup
QuestionDict = {
    "text/open"         : TextOpenQuestion,
    "text/numerical"    : TextNumericalQuestion,
    "choice/single"     : ChoiceSingleQuestion,
    "choice/multiple"   : ChoiceMultipleQuestion,
    "void"              : VoidQuestion}

if __name__ == "__main__":
    newQ = QuestionDict["choice/multiple"]("Testing dictionary constructor lookup", "True", None)
    print(newQ)