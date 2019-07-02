import requests
from bs4 import BeautifulSoup
import pprint
import json

pp = pprint.PrettyPrinter()


class MultiplexFilm:
    def __new__(cls, link: str):
        if link[:31] == 'https://multiplex.ua/ua/cinema/':  # check if link is correct
            return MultiplexFilm.__new__(cls, link)
        else:
            print('Invalid link')
            return None

    def __init__(self, link: str):
        self.link = link

    def get_input(self) -> list:
        response = requests.get(self.link)  # get response from multiplex (html page)
        soup = BeautifulSoup(response.text, 'html.parser')  # create html parser
        multiplex_raw_data = soup.select('.sch_date')  # find all elements with class=".sch_date"

        return multiplex_raw_data

    def get_data(self) -> dict:
        multiplex_raw_data = self.get_input()  # retrieve raw input data (data type = list) from multiplex.ua,
        # grouped by date

        output = {}  # create empty output dictionary
        for date in multiplex_raw_data:  # iterate through an input list
            show = {}  # create dict for film and sessions time
            films = date.select('.info')
            for film in films:
                title = film.a['title']  # get movie title

                sessions = film.select('.ns')
                time = []  # list for sessions time
                for session in sessions:
                    time.append(session.p.span.string)  # add value (time) in list for each session of each film

                show.update({title: time})  # add time for each film
            output.update({date['data-date']: show})  # add date for film sessions

        return output

    def write_output_json(self, output: dict):
        with open('mult.json', 'w') as json_file:
            json.dump(output, json_file, ensure_ascii=False)

    def get_json_data(self):
        multiplex_dict = self.get_data()

        multiplex_json = json.dumps(multiplex_dict, ensure_ascii=False)

        return multiplex_json
