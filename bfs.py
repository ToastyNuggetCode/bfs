import time
import threading
import os
import sys

blocked_funcs = [
"command_handler"
]

help_messages = {
"help" : "Displays this help message.",
"echo" : "Echos the user's message.",
"sequence" : "Runs provided functions in a sequence.\n  Syntax: function1(arg1,arg2 function2(arg1,arg2 "
}

# User functions

class UserFuncs:

    @staticmethod
    def clear():
        if sys.platform == "win32":
            os.system("cls")
        else:
            os.system("clear")

    @staticmethod
    def sequence(*commands):
        # For each function and argument combination the user provides,
        # we run the function with its provided arguments

        for c in commands:

            # If the command is blank, we skip it
            if c == "":
                continue

            # Seperates each user argument into its respective child function and arguments
            command = c.split("(")

            function = command[0]

            #print(function)

            # Since no spaces can be used when the user sequences functions,
            # they must seperate each function argument with commas,
            # so we must split the arguments before providing them to the command handler.
            # If arguments cannot be found, we set arguments equal to []

            try:
                arguments = command[1].split(",")
            except:
                arguments = []

            SysFuncs.command_handler(function,arguments)

    @staticmethod
    def file(file):
        pass
        script = open(file,"r")
        content = script.read().split("\n")
        script.close()
        UserFuncs.sequence(*content)

    @staticmethod
    def wait(wait,sym_type="lines"):
        symbols = {
        "lines" : ["|","/","-","\\","|","/","-","\\"],
        "other" : ["a","b","c"],
        "circles" : ["O","o"]
        }
        target = time.time() + float(wait)
        while time.time() < target:
            for symbol in symbols[sym_type]:
                remaining = str(round(target - time.time(),0))
                print(f"{symbol} {remaining}", end="")
                time.sleep(0.1)
                print("\r", end = "")
                if time.time() >= target:
                    break
    @staticmethod
    def pig():
        print("Oink")

    @staticmethod
    def echo(*messages):
        buffer = ""
        for message in messages:
            buffer += f"{message} "
        print(buffer)

    @staticmethod
    def help(lookup = None):
        try:
            if lookup == None:
                for key in help_messages:
                    print(f"{key}: {help_messages[key]}")
            else:
                print(f"{lookup}: {help_messages[lookup]}")
        except:
            print(f"Help for function \"{lookup}\" could not be found.")

# System functions
class SysFuncs:

    @staticmethod
    def command_handler(function,arguments):
        if function in blocked_funcs:
            print("You may not perform that function.")
            return "You may not perform that function."

        #if function not in globals():
            #return "Function not found."

        # If no arguments are provided, runs the function bare
        if arguments == []:
            try:
                getattr(UserFuncs,function)()
            except:
                raise
                return "Your function could not be run."
        # If arguments are provided, tries to run the function with the arguments
        else:
            try:
                # Runs the function with the unpacked list of arguments
                getattr(UserFuncs,function)(*arguments)
            except:
                # If the function fails to run, we will try to run the function without arguments
                try:
                    getattr(UserFuncs,function)()
                    #globals()[function]()
                except:
                    raise
                    return "Your function could not be run."
    @staticmethod
    def input_loop:
        while True:
            user_command = input("Enter command: ").split()

            function = user_command[0]
            arguments = user_command[1:]

            #print(arguments)

            error = SysFuncs.command_handler(function,arguments)

            if error != None:
                print(error)
