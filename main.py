import sys  # import sys to provide access to system specific functions
import requests  # import requests for making the HTTP requests to external APIs
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QLabel, QLineEdit,
                             QPushButton, QVBoxLayout)  # import the essential PyQt5 UI components
from PyQt5.QtCore import Qt  # import alignment and other core constants

"""
This module implements PyQt5 desktop application
that displays the current weather information for a city of the user's choosing
"""


class WeatherApp(QWidget):
    """
    WeatherApp is a PyQt5 QWidget that allows users to input a city name
    and get the weather data including the temperature, description, and an
    emoji representation using the OpenWeatherMap API
    """

    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    """
    Initializes and arranges the UI elements using QVBoxLayout,
    sets widget alignments, applies styles, and connects the button signal
    """

    def initUI(self):
        self.setWindowTitle("Weather App")

        # layout setup
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)

        # center-align text in labels and input fields
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        # set object names for styling
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # apply css-style appearance using the Qt stylesheets
        self.setStyleSheet("""
            QLabel, QPushButton{
                    font-family: calibri
            }
            QLabel#city_label{
                    font-size: 40px;
                    font-style: italic;
            }
            QLineEdit#city_input{
                    font-size: 40px;
            }
            QPushButton#get_weather_button{
                    font-size: 30px;
                    font-weight: bold;
            }
            QLabel#temperature_label{
                    font-size: 75px;
            }
            QLabel#emoji_label{
                    font-size: 100px;
                    font-family: Segoe UI emoji;
            }
            QLabel#description_label{
                    font-size: 50px;
            }
        """)

        # connect button click to the weather getting method
        self.get_weather_button.clicked.connect(self.get_weather)

    """
    fetches thw weather data from OpenWeatherMap API using the city input,
    parses the JSON response, and displays the weather or an error message
    """

    def get_weather(self):

        global response
        api_key = "d392813f3b41061be1144eda97c92944"  # OpenWeatherMap API key
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"  # construct the API URL

        # try sending request and handle the response
        try:
            response = requests.get(url)
            response.raise_for_status()  # raise an exception for HTTP errors
            data = response.json()  # parse JSON response

            if data["cod"] == 200:
                self.display_weather(data)

        # handle the necessary errors using exceptions
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occurred:\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as request_error:
            self.display_error(f"Request Error:\n{request_error}")

    """
    displays an error message and displays it 
    """

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    """
    parses the weather data and updates the UI with the temperature, emoji and description
    """

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_k = data["main"]["temp"]  # access the temp. in Kelvin
        temperature_f = (temperature_k * 9 / 5) - 459.67

        weather_id = data["weather"][0]["id"]  # access the weather condition ID
        weather_description = data["weather"][0]["description"]  # access the weather description

        self.temperature_label.setText(f"{temperature_f:.0f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    """
    returns an emoji representation using the OpenWeatherMap weather condition ID
    (string representation)
    """

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""  # return empty string for unrecognized codes


"""
using __main__ start the application
"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
