#                                                                              | Thus ends the allowed 79 characters
'''
Created on Jul 7, 2016

@author: Hunter Damron
'''

import warnings
from collections import OrderedDict

# Borrowed from code.activestate.com for marking functions as deprecated
# # TODO Remove before final version
def deprecated(func):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    """
    def newFunc(*args, **kwargs):
        warnings.warn("Call to deprecated function %s." % func.__name__,
                      category=DeprecationWarning)
        return func(*args, **kwargs)
    newFunc.__name__ = func.__name__
    newFunc.__doc__ = func.__doc__
    newFunc.__dict__.update(func.__dict__)
    return newFunc

class UI_Interface(object):
    """
    Interface to UI module
    
    Communicates questions and receives responses from UI
    
    Future implementation extensions that I'll likely never get to:
        -registerKeys() method to check that the UI can handle all question types 
            found in the XML file : not included because there is nothing you can 
            do about it so why not just allow python to throw an error
        -get_changes() method to find the differences between call of recalculate 
            and the most recent call to reduce redundant recalculation and data 
            transfer
    """
    
    def __init__(self, parent):
        """
        Constructs interface with access to parent (instance of Dynamic Survey)
        
        This will be called by DynamicSurvey passing parent=self
        """
        self.parent = parent
    
    def title(self):
        """
        Gets the survey title (formerly included in startup_data)
        
        :return: Returns string name of survey found in XML file
        """
    
    def startup_data(self):
        """
        Gets the startup data for displaying the survey
        
        :return: Returns first data from first iteration of 
            recalculate before any responses are added
            formatted as list of questions as lists each containing:
                -question_id: id of question to be displayed
                -question_type: type string interpreted by UI
                -text: body text for question
                -elements: dictionary containing attributes to be handled
                    by UI (multiples are contained in lists)
        
        Example return:
        [["age", "text/integer", "How old are you?", {"range": "0, 150"}],
         ["rating", "choice/multiple", "How would you rate beans?", {"selection": 
                 "radio", "choice": ["gross", "what are beans?", "delicious"]}]]
        """
    
    def recalculate(self, question_id, response, timestamp):
        """
        Recalculates question list after user response
        
        :param question_id: id of question answered
        :param response: value inputted from question answered
            (type of value depends on question, may be array)
        :param timestamp: timestamp of when question was answered
        :return: Returns list of relevant questions to be displayed
            formatted as list of questions as lists each containing:
                -question_id: id of question to be displayed
                -question_type: type string interpreted by UI
                -text: body text for question
                -elements: dictionary containing attributes to be handled
                    by UI (multiples are contained in lists)
            Returns None if the survey is deemed finished
                
        Note: all questions which have been answered are automatically 
            included even if they have been deemed irrelevant (to prevent 
            questions from disappearing) - may be modified when get_changes is 
            implemented
        
        Example return:
        [["age", "text/integer", "How old are you?", {"range": "0, 150", 
                "color": "red"}],
        ["rating", "choice/multiple", "How would you rate beans?", {"selection": 
                 "radio", "choice": ["gross", "what are beans?", "delicious"]}]]
        """
        self.parent._response(question_id, response, timestamp)
        return self.parent._recalculate()

    @deprecated  # May be completed later but not now for simplicity
    def get_changes(self, question_id, response, timestamp):
        """
        Calls recalculate and gets changes from last call to recalculate
        
        Compares call to recalculate to last call and reports changes
        Note: questions with changed attributes are included as if they are new
        :param question_id: id of question answered
        :param response: value inputted from question answered
            (type of value depends on question, may be array)
        :param timestamp: timestamp of when question was answered
        :return: Returns tuple containing (added items, id's for removed items)
            added question list containing questions as lists each containing:
                -question_id: id of question to be displayed
                -question_type: type string interpreted by UI
                -text: body text for question
                -elements: dictionary containing attributes to be handled
                    by UI (multiples are contained in lists)
            removed question list containing only id strings for questions
            
        Example return:
        ([["age", "text/integer", "How old are you?", {"range": "0, 150", "color": "red"}],
          ["rating", "choice/multiple", "How would you rate beans?", {"selection": 
                "radio", "choice": ["gross", "what are beans?", "delicious"]}]],
                 ["grand-children", "hunger", "profession"])
        """
        
        """ Implementation Notes:
        When _recalculate is called, it stores the version in the engine
        This method calls _recalculate() finds the changes between the two (if a text or 
            value changes, the question is returned as if it were added)
        """
    
    def quit(self):
        """
        Notifies the engine that the user is ready to quit (i.e. closed the window)
        
        Saves survey state before exiting program by creating XML file with title related to 
            survey id and filling it with:
                -user responses (id, response, timestamp)
                -current set of display questions (to prevent deletion of questions 
                    proved irrelevant)
        """
    
    def wecome_message(self):
        """
        Gets welcome message to display before survey starts
        
        :return: Returns the survey welcome message
        """
        
    def end_message(self):
        """
        Gets end message to display after survey stops
        
        :return: Returns the survey welcome message
        """

class Sensor_Interface(object):
    """
    Interface to Sensor Module
    
    Communicates with module which contains connections to all sensors that the survey
    can access
    
    Future implementation extensions that I'll likely never get to:
        -Back flow allowing engine to request sensor values instead of constantly 
            updating variables which will be always available (for example, 
            heavy calculations) : not included for simplicity and to avoid 
            synchronization issues with possible back flow delay
    """
    
    def __init__(self, parent):
        """
        Constructs interface with access to parent (instance of Dynamic Survey)
        
        This will be called by DynamicSurvey passing parent=self
        """
        self.parent = parent
    
    def neededSensors(self):
        """
        Gets the list of sensors requested by the survey (by id)
        
        Sensor module is responsible for providing values via update method;
        Prevents loading unnecessary sensor values
        :return: Returns list of id's that need to be loaded
        
        Example return:
        ["thermometer", "gps_location", "avg_height"]
        """
    
    def update(self, sensor_id, value):
        """
        Updates the value of sensor under id or creates variable if nonexistent
        
        :param sensor_id: id of sensor to be updated/created
        :param value: value to be saved in cache for sensor_id (can be any raw type, 
            including array)
        """
    
    def get_variable(self, variable_id):
        """
        Gets the value of a variable stored in the engine cache for use in sensor math
        
        :return: Returns the value of the variable with variable_id or None if the 
            variable does not exist
        """
    
class DynamicSurvey(object):
    """
    Class to contain survey root and interface methods
    
    Contains attributes from xml survey document needed for survey 
    to run and be displayed by generic UI; also contains UI_Interface and 
    Sensor_Interface
    
    Variables:
        ui: UI_Interface which will communicate with UI module
        sensors: Sensor_Interface which will communicate with sensors module
        root: root element of survey data structure (instance of QuestionBlock)
            -contains global threshold and mandatory_threshold
        name: name of survey
        welcome_msg: (optional) welcome message
        end_msg: (optional) end message
        scope: dictionary of available variables with names in the form that 
            they would be used in xml math strings
        cache: dictionary which holds most recent sensor values
        sensor_list: list of sensors required by survey
    """
    
    def __init__(self, survey_path, save_state=None):
        """
        Constructor for DynamicSurvey class
        
        Completes the following tasks:
            -construct UI_ and Sensor_Interfaces, passing parent=self
            -parse survey_path to xml.etree.ElementTree
            -load QuestionBlock root from ElementTree
            -load name, welcome_msg, and end_msg from ElementTree
            -generate scope for survey variables
            -load save_state if not None
            
            # TODO Finish planning survey constructor
            
        :param survey_path: path to XML survey structure file
        :param save_state: path to XML survey save state
        """
        
    def _parse_xml(self, path):
        """
        Parses XML document at path
        
        :param path: Path of XML file with survey structure
        
        Extracts from root:
            -name
            -welcome_msg
            -end_msg
            -question_tree (QuestionBlock)
            -needed_sensors - initializes sensor cache as dictionary
            
        Gets survey data from root element and then constructs 
            QuestionBlock also from root element (generates tree)
        Does not return anything but it initializes local variables as part 
            of the __init__() method
        """
    
    def _load_save_state(self, path):
        """
        Loads the pickle save state at path 
        
        Must be called after question tree has been loaded into survey
        For every question entry in the save state pickle file, it finds the 
            question, calls load(response, timestamp)
        Questions stored in pickled format {"id": (data, timestamp), ...}
            
        :param path: path to pickle file containing save state dictionary
        """
        
    def _save_state(self, path=None):
        """
        Saves survey progress in pickle file at path
        
        Iterates through all questions and loads answered questions into 
            dictionary to be saved in pickle
        Questions stored in pickled format {"id": (data, timestamp), ...}
        :param path: save state destination (should have pkl extension
            If path is None, the survey is stored within the application 
            at %SURVEY_ID%-%SAVE_TIME%.pkl
        """
    
    def _response(self, question_id, response, timestamp):
        """
        Updates question with question_id with response info
        
        Finds question from id and calls _update(response, timestamp)
        :param question_id: id of question answered
        :param response: value inputted from question answered
            (type of value depends on question, may be array)
        :param timestamp: timestamp of when question was answered
        """
        
        """ Implementation Notes:
        Answered questions are stored in a dictionary formatted with
            { id : (response, timestamp), ... }
        The dictionary value for question_id is added or modified with 
            response and timestamp as a tuple
        """
    
    def _recalculate(self):
        """
        Dirty work of the recalculation
        
        Runs through all questions and determines which are relevant      
        :return: Returns list of relevant questions to be displayed
            formatted as list of questions as lists each containing:
                -question_id: id of question to be displayed
                -question_type: type string interpreted by UI
                -text: body text for question
                -elements: dictionary containing attributes to be handled
                    by UI (multiples are contained in lists)
            Returns None if the survey is deemed finished (i.e. all questions 
                are below mandatory threshold
        
        Note: all questions which have been answered are automatically 
            included even if they have been deemed irrelevant (to prevent 
            questions from disappearing) - may be modified when get_changes is 
            implemented
            
        Note: if all questions are below threshold but not all are below mandatory 
            threshold, the most relevant question is added to the list
        
        Example return:
        ([["age", "text/integer", "How old are you?", {"range": "0, 150", "color": "red"}],
          ["rating", "choice/multiple", "How would you rate beans?", 
                {"selection": "radio", "choice": ["gross", "what are beans?", "delicious"]}]],
         ["grand-children", "hunger", "profession"])
        """
        
        """ Implementation Notes:
        -Calculates relevance of each question (using _evaluate() )
        -Adds questions with relevance above threshold to list to return
        -Tracks with boolean if all questions are below mandatory threshold
            to test if survey is finished
        -Returns the list of questions to be displayed in format above
        """
        
    def _scope(self):
        """
        Gets the scope of the survey that was calculated at initialization
        
        :return: Returns dictionary containing 
        """
        
    def _needed_sensors(self):
        """
        Gets a list containing the ids of the sensors required for the survey
        
        :return: Returns a list of needed sensor ids (sensors included 
            in XML structure file)
        """
    
class QuestionBlock(OrderedDict):
    """
    Block of questions with similar properties
    
    Extends OrderedDict because it has the same properties in that it is an ordered 
    set of questions and/or question blocks called by id
    
    Variables:
        -threshold: threshold above which block is relevant (overrides parent's 
            value if not None)
        -mandatory_threshold: threshold below which block may be discarded 
            (overrides parent's value if not None)
        -self is an ordered dictionary of questions and/or question blocks
            accessed by self.get(index) or by traditional dictionary lookup
    
    Methods to be implemented later if needed:
        -insert(index, item_id, item) : to insert item in dictionary at index
        -add(item_id, item) : to make function call of adding items to dictionary
    """
    
    def __init__(self, element):
        """
        Generates QuestionBlock instance from XML ElementTree element
        
        Extracts from branch contained in element:
            -prereq: prereq math string
            -relevance: relevance math string
            -threshold: threshold math string (overrides parent if not None)
            -mandatory threshold: mandatory threshold (overrides parent if 
                not None)
        :param element: XML ElementTree element containing branch to be loaded
        """
    
    def __iter__(self):
        """
        Iterates linearly over the tree using _yieldfrom() recursively
        
        :yield: Yields each item in _yieldfrom(self)
        """
    
    def _remove(self, item_id):
        """
        Removes and returns value contained by item_id
        
        :return: Returns value formerly held at item_id
        """
        
    def _indexOf(self, item_id):
        """
        Finds index of item with item_id
        
        :return: Returns index of item_id in self.keys()
        """
        
    def _getByIndex(self, index):
        """
        Get key and value found at index
        
        :return: Returns tuple with (key, value)
        """
        
def _yieldfrom(self, element):
    """
    Recursively iterates over a tree of dictionaries
    
    :param element: Root element of current branch to be iterated over
    """
    
class Question(object):
    """
    Represents a question loaded from an XML file
    
    Variables:
        -text: list of strings and/or Evaluables to create body text
        -prereq: math string which yields boolean prerequisites
        -relevance: math string holding relevance to be evaluated
        -threshold: threshold above which question is relevant (overrides parent's 
            value if not None)
        -mandatory_threshold: threshold below which question may be discarded 
            (overrides parent's value if not None)
        -elements: dictionary of Element objects with variable-dependence
        -question_data: dictionary containing any other data to be 
            used by the UI module
        -answered: boolean which is true if the question has been answered
        -response: user response to question, None if unanswered
        -response_time: timestamp of user response, None if unanswered
            Stored in seconds but likely used in different units
    """
    
    def __init__(self, xml_element):
        """
        Constructor uses element from XML file
        
        :param xml_element: XML element from parsing - must contain:
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
        
    def answered(self):
        """
        Tests if the question has been answered already
        
        This is stored in Question as a boolean because it is used in 
            relevance calculation
        :return: Returns True if a response has been logged for this question
        """
        
    def response(self):
        """
        Gets the most recent user response to the question or None if unanswered
        
        :return: Returns most recent response to this question's id logged 
            by _response()
        """
        
    def timestamp(self, units="seconds"):
        """
        Returns the time of the user response or None if unanswered
        
        :param units: Units to return the time in (defaults to seconds)
        :return: Returns time since epoch in specified units
        """
        
    def text(self):
        """
        Gets the question text after values are evaluated
        
        :return: Returns the text of the question as a single string after value 
            tags are evaluated
        """
        
    def _update(self, response, timestamp):
        """
        Updates question with response and timestamp
        
        Updates self.response and self.timestamp and sets answered = True
        :param response: User response to question
        :param timestamp: Time in seconds from epoch when question was answered
        """
        
    def _included(self):
        """
        Evaluates if question is relevant
        
        :return: Returns true if prereqs are True and relevance is 
            above threshold
        """
        
class Evaluable(object):
    """
    Simple class which contains a single string that can be evaluated 
        by _evaluate()
    """
    
    def __init__(self, math_str):
        """
        Evaluable constructor
        
        :param math_str: string which can be evaluated by _evaluate()
        """
        self.str = math_str
    
    def evaluate(self):
        """
        Evaluates the object's math string
        
        :return: Returns the value returned from evaluating 
            math string
        """

class Element(object):
    """
    Element or group of elements which depends on survey variables
    
    Variables:
        -prereq: math string which yields boolean prerequisites
        -relevance: math string holding relevance to be evaluated
        -threshold: threshold above which element is relevant (overrides 
            parent's value if not None)
        -element_data: dictionary containing any other data to be 
            used by the UI module
    """
    
    def _included(self):
        """
        Evaluates if element is relevant
        
        :return: Returns True if prereqs are True and relevance is above threshold
        """
        
    def _data(self):
        """
        Gets data to be used by UI
        
        :return: Returns the element_data dictionary
        """
    
def _evaluate(math_string, scope):
    """
    Evaluates math_string with access to variables in scope
    
    :param math_string: string containing math with rules:
        -values and operators are separated by spaces with 
            the exception of brackets and variable signs
        -evaluates to a single value
        -only uses the following operators (separated by order of ops):
            $( ... ) encloses variable as listed below
            
            ( ... )  traditional parentheses
            | ... |  absolute value brackets
            
            x ^ y  powers
            
            +x, -x  variable signs
            
            x * y  multiplication
            x / y  division
            x // y  floor division    # only yield integers
            x % y  modulo function
            
            x + y  addition
            x - y  subtraction
            
            # only yield booleans
            x > y  greater than
            x >= y  greater than or equal to
            x == y  compares if equal
            x <= y  less than or equal to
            x < y  less than
            
            # can only apply to booleans
            not x  logical NOT
            x and y  logical AND
        -reserves keywords:
            not
            and
            or
            true
            false
    
    :param scope: dictionary of variables which mathString can access including: 
        -QuestionBlocks which can provide:
            -completed which is true if all questions in block have been answered
        -Questions which can provide:
            -answered which is true if the question has been answered
            -response which gives the user response if answered else None
            -timestamp which returns timestamp of response in seconds if answered 
                else None
        -Sensors which provide most recent sensor value
    :return: returns numerical or boolean value of evaluated string
    """