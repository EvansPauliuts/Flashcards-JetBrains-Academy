# Write your code here
import random
import json
import argparse

from collections import OrderedDict
from io import StringIO


class FlashCards:
    od = OrderedDict()

    def __init__(self):
        self.logger = StringIO()
        self.count = 0
        self.hardest_line = []
        self.argument_data = {}
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--import_from')
        self.parser.add_argument('--export_to')
        self.args = self.parser.parse_args()

    def add_dict(self):
        self.saved_info_print('The card:')
        definition_valid = ''

        while True:
            term = input()
            if term in FlashCards.od:
                self.saved_info_print(f'The term "{term}" already exists. Try again:')
                continue
            else:
                self.saved_info_print('The definition of the card:')

                while True:
                    definition = self.saved_info_input()
                    values = [value for (value, count) in FlashCards.od.values()]

                    if definition in values:
                        self.saved_info_print(f'The definition "{definition}" already exists. Try again:')
                        continue
                    FlashCards.od[term] = (definition, 0)
                    definition_valid = definition
                    break
                break

        self.saved_info_print(f'The pair ("{term}":"{definition_valid}") has been added.')

    def remove_card(self):
        self.saved_info_print('Which card?')
        key_term = self.saved_info_input()

        try:
            if key_term in FlashCards.od:
                del FlashCards.od[key_term]
                self.saved_info_print('The card has been removed.')
                print()
            else:
                self.saved_info_print(f'Can\'t remove "{key_term}": there is no such card.')
        except TypeError:
            pass

    def ask_dict(self):
        self.saved_info_print('How many times to ask?\n')
        ask_number = int(self.saved_info_input())

        try:
            for _ in range(ask_number):
                random_dict = random.choice(list(FlashCards.od.items()))
                self.saved_info_print(f'Print the definition of "{random_dict[0]}":\n')
                answer = self.saved_info_input()

                if answer == random_dict[1][0]:
                    self.saved_info_print('Correct!\n')
                else:
                    values = [value for (value, count) in FlashCards.od.values()]

                    if answer in values:
                        keys_dict = self.get_dict_key(answer)
                        self.saved_info_print(f'Wrong. The right answer is "{random_dict[1][0]}", but your definition is correct for "{keys_dict}".\n')
                    else:
                        self.saved_info_print(f'Wrong. The right answer is "{random_dict[1][0]}".\n')

                    FlashCards.od[random_dict[0]] = (FlashCards.od[random_dict[0]][0], FlashCards.od[random_dict[0]][1] + 1)
        except ValueError:
            pass

    @staticmethod
    def get_dict_key(a):
        for key, value in FlashCards.od.items():
            if value[0] == a:
                return key
        return None

    def load_import_card(self, file_n=None):
        if not file_n:
            self.saved_info_print('File name:\n')
            file_n = self.saved_info_input()

        try:
            with open(f'{file_n}', 'r') as file:
                if file:
                    temp_dict = json.load(file)
                    for k, v in temp_dict.items():
                        FlashCards.od[k] = v
                    self.saved_info_print(f'{len(temp_dict)} cards have been loaded.')
        except IOError:
            self.saved_info_print('File not found.\n')

    def load_export_card(self, file_n=None):
        if not file_n:
            self.saved_info_print('File name:\n')
            file_n = self.saved_info_input()

        try:
            with open(f'{file_n}', 'w') as file:
                if file:
                    json.dump(FlashCards.od, file)
                    self.saved_info_print(f'{len(FlashCards.od)} cards have been saved.')
        except IOError:
            self.saved_info_print('File not found.\n')

    def hardest_card(self):
        for v in FlashCards.od.items():
            wrong_count = v[1][1]

            if wrong_count > self.count:
                self.count = wrong_count

        if self.count:
            card = [v for v in FlashCards.od.items() if v[1][1] == self.count]
            if len(card) > 1:
                hardest_list = [v[0] for v in card]
                hardest_line = ', '.join(hardest_list)
                self.saved_info_print(f'The hardest cards are {hardest_line}.\n')
            else:
                self.saved_info_print(
                    f'The hardest card is "{card[0]}". You have {self.count} errors answering it.\n'
                )
        else:
            self.saved_info_print('There are no cards with errors.\n')

    def reset_stats(self):
        for k in FlashCards.od.keys():
            FlashCards.od[k] = (FlashCards.od[k][0], 0)

        self.count = 0
        self.saved_info_print('Card statistics have been reset.\n')

    @staticmethod
    def saved_info_print(obj):
        with open('log', 'a') as logger:
            print(obj)
            logger.write(obj)
            logger.write('\n')

    @staticmethod
    def saved_info_input():
        with open('log', 'a') as logger:
            name = input()
            logger.write(name)
            logger.write('\n')
        return name

    def log_info(self):
        self.saved_info_print('File name:\n')
        file_n = self.saved_info_input()

        try:
            with open('log', 'r') as log_file, open(f'{file_n}', 'w', encoding='utf-8') as new_file_log:
                info_log = log_file.readlines()
                new_file_log.writelines(info_log)

            self.saved_info_print('The log has been saved.')
            return
        except IOError:
            self.saved_info_print('File not found.\n')

    def argument_parse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--import_from')
        parser.add_argument('--export_to')

        args = parser.parse_args()

        if args.import_from:
            self.argument_data['import_from'] = args.import_from
        if args.export_to:
            self.argument_data['export_to'] = args.export_to

    def start(self):
        if self.args.import_from is not None:
            self.load_import_card(self.args.import_from)

        while True:
            self.saved_info_print('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n')
            menu_action = self.saved_info_input()

            if menu_action == 'add':
                self.add_dict()
            elif menu_action == 'remove':
                self.remove_card()
            elif menu_action == 'ask':
                self.ask_dict()
            elif menu_action == 'import':
                self.load_import_card()
            elif menu_action == 'export':
                self.load_export_card()
            elif menu_action == 'exit':
                if self.args.export_to is not None:
                    self.load_export_card(self.args.export_to)
                self.saved_info_print('Bye bye!')
                break
            elif menu_action == 'log':
                self.log_info()
            elif menu_action == 'hardest card':
                self.hardest_card()
            elif menu_action == 'reset stats':
                self.reset_stats()
            else:
                self.saved_info_print('[Error]: That is not a valid action.')


if __name__ == '__main__':
    flash_cards = FlashCards()
    flash_cards.start()
