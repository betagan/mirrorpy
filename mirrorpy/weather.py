import requests
import json
from datetime import datetime

from mirrorpy.plugin import Plugin


class WeatherPlugin(Plugin):
    baseurl = "http://api.openweathermap.org/data/2.5/{0}?units=metric&APPID=1ba44d08af637d2899097f510bf9f882"
    query_url = None

    def __init__(self, name="", query=None, city=None, coords=None):
        self.name = name

        if city is not None:
            self.query_url = self.baseurl + "&city=%s" % city
        elif coords is not None:
            self.query_url = self.baseurl + "&lat=%s&lon=%s" % coords
        elif query is not None:
            self.query_url = self.baseurl + "&q=%s" % query
        else:
            raise ValueError("Neither city nor coords provided")

    def get(self):
        template = """
        <div class="row">
            <div class="col-xs-4 weather-location">{2}</div>
            <div class="col-xs-7 weather-temp-current">{0}° {1}</div>
        </div>
        """

        print(self.query_url.format("weather"))
        response = requests.get(self.query_url.format("weather"))
        j = json.loads(response.content.decode('utf-8'))

        tmp = ""
        for i in j["weather"]:
            tmp += "<img class='weather-icon-current' src='http://openweathermap.org/img/w/%s.png' />" % (i["icon"])

        result = template.format(round(j["main"]["temp"]), tmp, self.name)

        response = requests.get(self.query_url.format("forecast"))

        j = json.loads(response.content.decode('utf-8'))

        result += """<div class="row">"""
        template = """<div class="col-xs-1 weather-temp-forecast">{0}<br />{2}<br/>{1}°</div>"""

        cnt = 0

        for i in j["list"]:
            if cnt >= 9:
                break

            tmp = ""
            for k in i["weather"]:
                tmp += "<img class='weather-icon-forecast' src='http://openweathermap.org/img/w/%s.png' />" % (k["icon"])

            result += template.format(datetime.fromtimestamp(i["dt"]).hour, round(i["main"]["temp"]), tmp)

            cnt += 1

        result += "</div>"

        return result
