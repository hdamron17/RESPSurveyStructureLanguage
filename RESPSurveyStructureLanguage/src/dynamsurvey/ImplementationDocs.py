'''
Created on Jul 7, 2016

@author: Hunter Damron
'''

class UI_Interface(object):
    """
    Interface to UI module
    
    Communicates questions and receives responses from UI
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
                    by UI
        
        Example return:
        [["age", "text/integer"
        """
    
    # TODO
    pass

class Sensor_Interface(object):
    
    # TODO
    pass