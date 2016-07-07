'''
Created on Jul 7, 2016

@author: Hunter Damron
'''

class UI_Interface(object):
    """
    Interface to UI module
    
    Communicates questions and receives responses from UI
    """
    
    def title(self):
        """
        Gets the survey title (formerly included in startup_data)
        
        :return: Returns string name of survey found in XML file
        """
        # TODO
        pass
    
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
         ["rating", "choice/multiple", "How would you rate beans?", 
                {"selection": "radio", "choice": ["gross", "what are beans?", "delicious"]}]]
        """
        # TODO
        pass
    
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
        
        Example return:
        [["age", "text/integer", "How old are you?", {"range": "0, 150", "color": "red"}],
         ["rating", "choice/multiple", "How would you rate beans?", 
                {"selection": "radio", "choice": ["gross", "what are beans?", "delicious"]}]]
        """
        # TODO
        pass
    
    def get_changes(self, question_id, response, timestamp):
        """
        Calls recalculate and gets changes from last call to recalculate
        
        Compares call to recalculate to last call and reports changes
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
          ["rating", "choice/multiple", "How would you rate beans?", 
                {"selection": "radio", "choice": ["gross", "what are beans?", "delicious"]}]],
         ["grand-children", "hunger", "profession"])
        """
        # TODO
        pass
    
    def quit(self):
        """
        Notifies the engine that the user is ready to quit (i.e. closed the window)
        
        Saves survey state before exiting program by creating XML file with title related to 
            survey id and filling it with:
                -user responses (id, response, timestamp)
                -current set of display questions (to prevent deletion of questions 
                    proved irrelevant)
        """
        # TODO
        pass

class Sensor_Interface(object):
    """
    Interface to Sensor Module
    
    Communicates with module which contains connections to all sensors that the survey 
    can access
    """
    
    def neededSensors(self):
        """
        Gets the list of sensors requested by the survey (by id)
        
        Sensor module is responsible for providing values via update method;
        Prevents loading unnecessary sensor values
        :return: Returns list of id's that need to be loaded
        
        Example return:
        ["thermometer", "gps_location", "avg_height"]
        """
        # TODO
        pass
    
    def update(self, sensor_id, value):
        """
        Updates the value of sensor under id or creates variable if nonexistent
        
        :param sensor_id: id of sensor to be updated/created
        :param value: value to be saved in cache for sensor_id (can be any raw type, 
            including array)
        """
        # TODO
        pass