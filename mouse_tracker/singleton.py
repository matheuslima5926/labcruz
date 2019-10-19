# class TestSetup:
#     __instance = None
#     animal = ""
#     timein_open = 0
#     timein_

#     @staticmethod 
#     def getInstance():
#         """ Static access method. """
#         if TestSetup.__instance == None:
#            TestSetup()
#         return TestSetup.__instance

#     def __init__(self):
#         """ Virtually private constructor. """
#         if TestSetup.__instance != None:
#            raise Exception("This class is a singleton!")
#         else:
#            TestSetup.__instance = self