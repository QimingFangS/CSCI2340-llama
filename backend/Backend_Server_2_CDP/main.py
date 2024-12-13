#############################################################################################################################
# Program: main.py                                                                                                          #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program contains the main entry point for the application.                                              #                                                                                                 
#############################################################################################################################

from flask import Flask
from app.routes import app_routes 

app = Flask(__name__)
app.register_blueprint(app_routes)  

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)