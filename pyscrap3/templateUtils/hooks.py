import os
import mrbob
from datetime import datetime


def checkName(configurator, question, answer):
    print("nombre: " + answer)
    proyectPath = os.getcwd() + "/" + answer
    print("path " + proyectPath)
    if not os.path.exists(proyectPath):
        print("no existe, ok")
    else:
        print("Directory '" + answer + "' already exists!")
        raise mrbob.bobexceptions.ValidationError
    return answer


def setCurrentYear(configurator, question):
    question.default = datetime.now().year
