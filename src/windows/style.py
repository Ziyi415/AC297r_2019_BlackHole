########## Main Page ##############
def runBtn():
    return """
        QPushButton {
        padding: 12px;
        font-size: 15px;
        font-family: Arial Bold;
        background-color: #c9c9c9;
        border-style: inset;
        border-radius: 5px;

        }
        QPushButton:pressed {
        padding: 12px;
        font-family: Arial Bold;
        background-color: #f7c552;
        border-style: inset;
        border-radius: 5px;
        }
    
    """
def singleTeleUpdate():
    return """
        QLabel {
            color: #C3272B;
        }
    """


########### Single Tele ############
def single_tele_title():
    return """
        QLabel {
            font-size: 15px;
            font-family: Arial Bold;
        }
    """

########### Model result ############
def top_layout():
    return """
        Layout{
            background-color: black;
        }
    """
def model_title():
    return """
        QLabel{
            font-size: 20px;
            font-family: Arial Bold;
            color: white;
        }
    """

def model_label():
    return """
        QLabel{
            font-size: 15px;
        }
    """

def model_result():
    return """
        QLabel{
            font-size: 15px;
            color: #C3272B;
        }
    """

########### Contact ############
def contact_title():
    return """
        QLabel{
            font-size: 20px;
            font-family: Arial Bold;
        }
    """

