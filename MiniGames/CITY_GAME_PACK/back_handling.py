from random import choice
import json 

class CheckIsTown:
    def __init__(self, city):
        self.city = city.lower()

    def binary_search(self, working_list):
        low = 0
        high = len(working_list)-1
        while low <= high:
            mid = (low+high)//2
            guess = working_list[mid]
            if guess == self.city:
                return True
            elif guess > self.city:
                high = mid-1
            else:
                low = mid+1
        return False
    
    def checking_is_town(self):
        with open('CITY_GAME_PACK/countries.json', 'r', encoding='utf-8') as f:
            countries_city_dict = json.load(f)
            input_city = sorted([citys.lower() for keys, values in countries_city_dict.items() for citys in values])
            return self.binary_search(input_city)
    def __call__(self):
        return self.checking_is_town()

class WordHandlerAnswerOutput:
    def __init__(self, symbol):
        self.symbol = symbol

    def binary_search(self, working_list):
        low = 0
        high = len(working_list)-1

        while low <= high:
            mid = (low+high)//2
            value = working_list[mid]
            if value.startswith(self.symbol.upper()):
                return value
            if value > self.symbol.upper():
                high = mid-1
            else:
                low = mid+1

    def handling(self):
        with open('CITY_GAME_PACK/countries.json', 'r', encoding='utf-8') as f:
            countries_city_dict = json.load(f)
            countries = sorted([])
            for keys, values in countries_city_dict.items():
                countries.append(keys)
            random_country = choice(countries)
            random_cities = countries_city_dict[random_country]
            sorted_random_cities = sorted(random_cities)
            binary_result =  self.binary_search(sorted_random_cities)
            if binary_result is None:
                try:
                    return self.handling()
                except RecursionError:
                    return 'GAMEOVER'
            else:
                return random_country, binary_result
            
    def __call__(self):
        return self.handling()

def choice_city():
    with open('CITY_GAME_PACK/countries.json', 'r', encoding='utf-8') as f:
            countries_city_dict = json.load(f)
            all_cities = sorted([citys for keys, values in countries_city_dict.items() for citys in values])
            return choice(all_cities)

def cut_filter_word(word):
    while word[-1].lower() in ['ъ', 'ь', 'ё', 'ы', 'Ы']:
        word = word[:-1]
    return word.lower()
