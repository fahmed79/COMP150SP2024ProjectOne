import json
import sys
from typing import List
import random
from enum import Enum

class Statistic:
    def __init__(self, legacy_points: int = 0):
        self.value = self._generate_starting_value(legacy_points)
        self.description = None
        self.min_value = 0
        self.max_value = 100

    def __str__(self):
        return f"{self.value}"

    def increase(self, amount):
        self.value += amount
        if self.value > self.max_value:
            self.value = self.max_value

    def decrease(self, amount):
        self.value -= amount
        if self.value < self.min_value:
            self.value = self.min_value

    def _generate_starting_value(self, legacy_points: int):
        return legacy_points / 100 + random.randint(1, 3)


class Strength(Statistic):
    def __init__(self):
        super().__init__()
        self.description = "Strength is a measure of physical power."


class Dexterity(Statistic):
    def __init__(self):
        super().__init__()
        self.description = "Dexterity is a measure of agility."


class Location:
    def __init__(self, parser, number_of_events: int = 1):
        self.parser = parser
        self.events = [Event(self.parser) for _ in range(number_of_events)]

    def create_custom_event_from_static_text_file(self, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
        return Event(self.parser, data)


class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"


class Event:
    def __init__(self, parser, data: dict = None):
        self.parser = parser
        if data is not None:
            self.primary = data['primary_attribute']
            self.secondary = data['secondary_attribute']
            self.prompt_text = data['prompt_text']
            self.pass_ = data['pass']
            self.fail = data['fail']
            self.partial_pass = data['partial_pass']

        self.status = EventStatus.UNKNOWN
        self.fail_message = {"message": "You failed."}
        self.pass_message = {"message": "You passed."}
        self.partial_pass_message = {"message": "You partially passed."}
        self.prompt_text = "A dragon appears, what will you do?"

        self.primary: Statistic = Strength()
        self.secondary: Statistic = Dexterity()

    def execute(self, party):
        chosen_one = self.parser.select_party_member(party)
        chosen_skill = self.parser.select_skill(chosen_one)

        self.resolve_choice(party, chosen_one, chosen_skill)

    def set_status(self, status: EventStatus = EventStatus.UNKNOWN):
        self.status = status

    def resolve_choice(self, party, character, chosen_skill):
        skill_primary = chosen_skill.primary_attribute
        skill_secondary = chosen_skill.secondary_attribute

        if skill_primary == self.primary or skill_secondary == self.primary:
            self.set_status(EventStatus.PASS)
        elif skill_primary == self.secondary or skill_secondary == self.secondary:
            self.set_status(EventStatus.PARTIAL_PASS)
        else:
            self.set_status(EventStatus.FAIL)


class Character:
    def __init__(self, name):
        self.name = name
        self.strength = random.randint(1, 10)
        self.dexterity = random.randint(1, 10)
        self.constitution = random.randint(1, 10)
        self.vitality = random.randint(1, 10)
        self.endurance = random.randint(1, 10)
        self.intelligence = random.randint(1, 10)
        self.wisdom = random.randint(1, 10)
        self.knowledge = random.randint(1, 10)
        self.willpower = random.randint(1, 10)
        self.spirit = random.randint(1, 10)

    def __str__(self):
        return f"{self.name}: Str({self.strength}), Dex({self.dexterity}), Con({self.constitution}), " \
               f"Vit({self.vitality}), End({self.endurance}), Int({self.intelligence}), Wis({self.wisdom}), " \
               f"Know({self.knowledge}), Will({self.willpower}), Spir({self.spirit})"


class Party:
    def __init__(self):
        self.members = []

    def add_member(self, character):
        self.members.append(character)

    def remove_member(self, character):
        if character in self.members:
            self.members.remove(character)
        else:
            print(f"{character.name} is not a member of the party.")

    def list_members(self):
        print("Party Members:")
        for member in self.members:
            print(member)
class User:

    def __init__(self, parser, username: str, password: str, legacy_points: int = 0):
        self.username = username
        self.password = password
        self.legacy_points = legacy_points
        self.parser = parser  # Adding the parser attribute

        # Ensure that parser is provided before creating the game
        if parser:
            self.current_game = self._get_retrieve_saved_game_state_or_create_new_game()
        else:
            self.current_game = None

    def _get_retrieve_saved_game_state_or_create_new_game(self) -> 'Game':
        # Only create a new game if parser is provided
        if self.parser:
            new_game = Game(self.parser)
            return new_game
        else:
            return None

class Game:
    def __init__(self, parser):
        self.parser = parser
        self.party = Party()
        self.opponents = []  # Fill this with Giant instances
        self.continue_playing = True

    def start_game(self):
        print("Welcome to Ragnarok!")
        print("Choose which god characters to play with:")
        print("1. Kratos\n2. Loki\n3. Odin\n4. Thor")
        choices = input("Enter the numbers of the characters (e.g., '1 3' for Kratos and Odin): ").split()

        for choice in choices:
            if choice == '1':
                self.add_party_member(Kratos())
            elif choice == '2':
                self.add_party_member(Loki())
            elif choice == '3':
                self.add_party_member(Odin())
            elif choice == '4':
                self.add_party_member(Thor())
            else:
                print("Invalid choice!")

        print("Your party:")
        self.party.list_members()

        print("Prepare to face the giants in the final battle of Ragnarok!")
        for opponent in self.opponents:
            print(f"You are facing {opponent.name}: {opponent.ability()}")

    def add_party_member(self, character):
        self.party.add_member(character)


class Kratos(Character):
    def __init__(self):
        super().__init__("Kratos")
        self.strength += 5  # Kratos has great strength


class Loki(Character):
    def __init__(self):
        super().__init__("Loki")
        self.dexterity += 5  # Loki is a shape shifter


class Odin(Character):
    def __init__(self):
        super().__init__("Odin")
        self.willpower += 5  # Odin has psychological manipulation abilities


class Thor(Character):
    def __init__(self):
        super().__init__("Thor")
        self.spirit = float('inf')  # Thor has unlimited power


class UserInputParser:
    def __init__(self):
        self.style = "console"

    def parse(self, prompt) -> str:
        response: str = input(prompt)
        return response


class UserFactory:

    @staticmethod
    def create_user(parser: UserInputParser) -> User:
        username = parser.parse("Enter a username: ")
        password = parser.parse("Enter a password: ")
        # Here you can add more

        # Here you can add more logic as needed, e.g., validate input
        return User(parser, username=username, password=password)


class InstanceCreator:

    def __init__(self, user_factory: UserFactory, parser: UserInputParser):
        self.user_factory = user_factory
        self.parser = parser

    def _new_user_or_login(self) -> 'User':
        response = self.parser.parse("Create a new username or login to an existing account?")
        if "login" in response:
            return self._load_user()
        else:
            return self.user_factory.create_user(self.parser)

    def get_user_info(self, response: str) -> 'User':
        if "yes" in response:
            return self._new_user_or_login()
        else:
            return None

    def _load_user(self) -> 'User':
        pass


def start_game():
    parser = UserInputParser()
    user_factory = UserFactory()
    instance_creator = InstanceCreator(user_factory, parser)

    response = parser.parse("Would you like to start a new game? (yes/no)")
    print(f"Response: {response}")
    user = instance_creator.get_user_info(response)
    if user is not None:
        game_instance = user.current_game
        if game_instance is not None:
            game_instance.start_game()
            response = input("Do you want to save and quit? (yes/no): ").lower()
            if response == "yes":
                user.save_game()
                print("Game saved. Goodbye!")
                sys.exit()
            else:
                print("Goodbye!")
                sys.exit()
    else:
        print("See you next time!")
        sys.exit()


if __name__ == '__main__':
    start_game()
