import json
import datetime
from dateutil.relativedelta import relativedelta
import requests

API_URL = 'http://127.0.0.1:8000/'
API_USERS = 'users/'
API_ENTRIES = 'entries/'
API_P_ENTRIES = 'p_entries/'
API_GOALS = 'goals/'


# Klasa odpowiadająca za logikę aplikacji łączenia się z REST API

class App:
    token: str | None = None
    token_type: str | None = None

    def __init__(self):
        pass

    def is_logged(self) -> bool:
        return self.token is not None

    def logging(self, username, password):
        data = {'grant_type': None, 'username': username, 'password': password, 'scope': None, 'client_id': None,
                'client_secret': None}
        response = requests.post(API_URL + API_USERS + 'token', data=data)
        if response.status_code == 200:
            self.token = response.json()['access_token']
            self.token_type = response.json()['token_type']

        return response.status_code

    def head(self):
        return {'Authorization': f'{self.token_type} {self.token}'}

    def register(self, username, password):
        data = json.dumps({'username': username, 'password': password})
        response = requests.post(API_URL + API_USERS, data=data)
        return response.status_code

    # Users
    def get_current_user(self):
        response = requests.get(API_URL + API_USERS + 'me', headers=self.head())
        if response.status_code == 200:
            return response.json()
        return None

    def edit_personalities(self, first_name, last_name):
        data = json.dumps({'first_name': first_name, 'last_name': last_name})
        response = requests.put(API_URL + API_USERS + 'me', headers=self.head(), data=data)
        if response.status_code == 200:
            return response.json()['first_name'], response.json()['last_name']
        return None

    def delete_user(self):
        return requests.delete(API_URL + API_USERS + 'me', headers=self.head()).status_code

    def change_balance(self, change):
        return requests.patch(API_URL + API_USERS + 'me/' + str(change), headers=self.head()).json()['balance']

    def set_balance(self, new_balance):
        return requests.put(API_URL + API_USERS + 'me/' + str(new_balance), headers=self.head()).json()['balance']

    def change_password(self, old_pass, new_pass):
        data = json.dumps({'old_password': old_pass, 'new_password': new_pass})
        return requests.put(API_URL + API_USERS + 'me_password', data=data, headers=self.head()).status_code

    # Entry
    def get_entries(self, skip=0, limit=5):
        response = requests.get(API_URL + API_ENTRIES + f'?skip={skip}&limit={limit}', headers=self.head())
        if response.status_code == 200:
            return response.json()
        return None

    def add_entry(self, category, name, is_outcome, date, amount, description):
        data = json.dumps({'category': category, 'name': name, 'is_outcome': is_outcome, 'date': date, 'amount': amount,
                           'description': description})
        response = requests.post(API_URL + API_ENTRIES + 'add', data=data, headers=self.head())
        if response.status_code == 200:
            return response.json()
        return None

    def get_entry(self, entry_id):
        response = requests.get(API_URL + API_ENTRIES + f'get/{entry_id}', headers=self.head())
        if response.status_code == 200:
            return response.json()
        return None

    def edit_entry(self, entry_id, category, name, is_outcome, date, amount, description):
        data = json.dumps({'category': category, 'name': name, 'is_outcome': is_outcome, 'date': date, 'amount': amount,
                           'description': description})
        response = requests.put(API_URL + API_ENTRIES + f'edit/{entry_id}', data=data, headers=self.head())
        if response.status_code == 200:
            return response.json()
        return None

    def delete_entry(self, entry_id):
        return requests.delete(API_URL + API_ENTRIES + f'delete/{entry_id}', headers=self.head()).status_code

    # Planned entry
    def get_planned_entries(self, skip=0, limit=5):
        response = requests.get(API_URL + API_P_ENTRIES + f'?skip={skip}&limit={limit}', headers=self.head())
        if response.status_code == 200:
            return response.json()
        return None

    def add_planned_entry(self, category, name, is_outcome, date, amount, description, periodicity):
        data = json.dumps({'category': category, 'name': name, 'is_outcome': is_outcome, 'date': date, 'amount': amount,
                           'description': description, 'periodicity': periodicity})
        response = requests.post(API_URL + API_P_ENTRIES + 'add', data=data, headers=self.head())
        if response.status_code == 200:
            return response.json()
        return None

    def get_planned_entry(self, planned_entry_id):
        response = requests.get(API_URL + API_P_ENTRIES + f'get/{planned_entry_id}', headers=self.head())
        if response.status_code == 200:
            return response.json()
        return None

    def edit_planned_entry(self, planned_entry_id, category, name, is_outcome, date, amount, description, periodicity):
        data = json.dumps({'category': category, 'name': name, 'is_outcome': is_outcome, 'date': date, 'amount': amount,
                           'description': description, 'periodicity': periodicity})
        response = requests.put(API_URL + API_P_ENTRIES + f'edit/{planned_entry_id}', data=data, headers=self.head())
        if response.status_code == 200:
            return response.json()
        return None

    def delete_planned_entry(self, planned_entry_id):
        return requests.delete(API_URL + API_P_ENTRIES + f'delete/{planned_entry_id}', headers=self.head()).status_code

    # Goal
    def get_goals(self, skip=0, limit=5):
        response = requests.get(API_URL + API_GOALS + f'?skip={skip}&limit={limit}', headers=self.head())
        if response.status_code == 200:
            return response.json()
        return None

    def add_goal(self, name, target_amount, actual_amount, date, color, icon, description):
        data = json.dumps({'name': name, 'target_amount': target_amount, 'actual_amount': actual_amount, 'date': date,
                           'color': color, 'icon': icon, 'description': description})
        response = requests.post(API_URL + API_GOALS + 'add', data=data, headers=self.head())
        if response.status_code == 200:
            return response.json()
        return None

    def get_goal(self, goal_id):
        response = requests.get(API_URL + API_GOALS + f'get/{goal_id}', headers=self.head())
        if response.status_code == 200:
            return response.json()
        return None

    def edit_goal(self, goal_id, name, target_amount, actual_amount, date, color, icon, description):
        data = json.dumps({'name': name, 'target_amount': target_amount, 'actual_amount': actual_amount, 'date': date,
                           'color': color, 'icon': icon, 'description': description})
        response = requests.put(API_URL + API_GOALS + f'edit/{goal_id}', data=data, headers=self.head())
        if response.status_code == 200:
            return response.json()
        return None

    def delete_goal(self, goal_id):
        return requests.delete(API_URL + API_GOALS + f'delete/{goal_id}', headers=self.head()).status_code

    # Dealing with planned entries
    def perform_planned_entries(self):
        p_entry_list = self.get_planned_entries(0, 1)
        if len(p_entry_list) == 0:
            return

        p_entry = self.get_planned_entry(p_entry_list[0]['id'])
        date_str = p_entry['date']

        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')

        if date > datetime.datetime.today():
            return

        self.add_entry(category=p_entry['category'], name=p_entry['name'], is_outcome=p_entry['is_outcome'],
                       date=p_entry['date'], amount=p_entry['amount'], description=p_entry['description'])

        if p_entry['periodicity'] == 0:
            self.delete_planned_entry(p_entry['id'])
        else:
            if p_entry['periodicity'] == 1:
                date = date + datetime.timedelta(days=1)
            elif p_entry['periodicity'] == 2:
                date = date + relativedelta(months=1)
            else:
                date = date + relativedelta(years=1)

            date_str = date.strftime('%Y-%m-%d')
            self.edit_planned_entry(planned_entry_id=p_entry['id'], category=p_entry['category'], name=p_entry['name'],
                                    is_outcome=p_entry['is_outcome'], date=date_str, amount=p_entry['amount'],
                                    description=p_entry['description'], periodicity=p_entry['periodicity'])

        self.perform_planned_entries()
