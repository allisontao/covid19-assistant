import requests
import json
import threading
import time

class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.data = self.get_data()
        
    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params=self.params)
        data = json.loads(response.text)
        return data

    def get_total_cases(self):
        data = self.data['total']
        for content in data:
            if content['name'] == 'Coronavirus Cases:':
                return content['value']
        return "0"
    
    def get_total_deaths(self):
        data = self.data['total']
        for content in data:
            if content['name'] == 'Deaths:':
                return content['value']
        return "0"
    
    def get_total_recovered(self):
        data = self.data['total']
        for content in data:
            if content['name'] == 'Recovered:':
                return content['value']
        return "0"
    
    def get_country_data(self, country):
        data = self.data['country']
        for content in data:
            if content['name'].lower() == country.lower():
                return content
        return "0"
    
    def get_list_of_countries(self):
        countries = [country['name'].lower() for country in self.data['country']]
        return countries
    
    def update_data(self):
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run', params=self.params)
        
        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print("Data updated")
                    break
                time.sleep(5)
        
        t = threading.Thread(target=poll)
        t.start()