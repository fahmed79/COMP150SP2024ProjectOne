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
        self.opponents = [ Giant(), Serpent(), Fenrir(), Hell()]  # Fill this with Giant instances
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
         # Select a random opponent
        random_opponent = random.choice(self.opponents)
        print(f"You are facing {random_opponent.name}: {random_opponent.ability()}")

        # Start the battle
        winner = self.battle(random_opponent)

        # Display the result
        if winner == "Player":
            print("Congratulations! You defeated the opponent.")
        else:
            print(f"Sorry, the opponent {random_opponent.name} won.")

    def battle(self, opponent):
        player_strength = sum(character.strength for character in self.party.members)
        opponent_strength = opponent.strength

        if player_strength > opponent_strength:
            return "Player"
        elif player_strength < opponent_strength:
            return "Opponent"
        else:
            return "Draw"

    def add_party_member(self, character):
        self.party.add_member(character)


class Kratos(Character):
    def __init__(self):
        super().__init__("Kratos")
        self.strength += 50  # Kratos has great strength


class Loki(Character):
    def __init__(self):
        super().__init__("Loki")
        self.dexterity += 60  # Loki is a shape shifter


class Odin(Character):
    def __init__(self):
        super().__init__("Odin")
        self.willpower += 50  # Odin has psychological manipulation abilities


class Thor(Character):
    def __init__(self):
        super().__init__("Thor")
        self.spirit = float('inf')  # Thor has unlimited power

class Giant(Character):
    def __init__(self, name="Giant"):
        super().__init__(name)
        self.strength = random.randint(10, 20)
        self.dexterity = random.randint(5, 10)
        self.constitution = random.randint(15, 25)

    def ability(self):
        return "Smashes enemies with brute force."

class Serpent(Character):
    def __init__(self, name="Serpent"):
        super().__init__(name)
        self.strength = random.randint(15, 25)
        self.dexterity = random.randint(10, 15)
        self.constitution = random.randint(20, 30)
        # Define other attributes as needed

    def ability(self):
        return "Breathes Poison and swallow the enemy."

class Fenrir(Character):
    def __init__(self, name="Fenrir"):
        super().__init__(name)
        self.strength = random.randint(20, 35)
        self.dexterity = random.randint(20, 25)
        self.constitution = random.randint(30, 40)

    def ability(self):
        return "Immense Agressive Attacks on enimies."

class Hell(Character):
    def __init__(self, name="Hell"):
        super().__init__(name)
        self.strength = random.randint(15, 25)
        self.dexterity = random.randint(10, 25)
        self.constitution = random.randint(40, 50)

    def ability(self):
        return "Attacks with the army."


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


#tests

import unittest

class TestStatistic(unittest.TestCase):

    def test_strength_increase(self):
        strength = Strength()
        strength.increase(10)
        self.assertEqual(strength.value, 10)

    def test_dexterity_decrease(self):
        dexterity = Dexterity()
        dexterity.decrease(5)
        self.assertEqual(dexterity.value, -5)  # Dexterity cannot be negative, you might want to handle this case

class TestEvent(unittest.TestCase):

    def test_resolve_choice_pass(self):
        parser = UserInputParser()
        event = Event(parser)
        party = Party()
        skill = []
        party.add_member(Character("Test", strength=20, dexterity=30))
        chosen_one = party.members[0]
        chosen_skill = skill(primary_attribute=Strength(), secondary_attribute=Dexterity())
        
        event.resolve_choice(party, chosen_one, chosen_skill)
        self.assertEqual(event.status, EventStatus.PASS)

    def test_resolve_choice_partial_pass(self):
        parser = UserInputParser()
        event = Event(parser)
        party = Party()
        skill = []

        party.add_member(Character("Test", strength=30, dexterity=20))
        chosen_one = party.members[0]
        chosen_skill = skill(primary_attribute=Strength(), secondary_attribute=Dexterity())
        
        event.resolve_choice(party, chosen_one, chosen_skill)
        self.assertEqual(event.status, EventStatus.PARTIAL_PASS)

    def test_resolve_choice_fail(self):
        parser = UserInputParser()
        event = Event(parser)
        party = Party()
        skill = []
        party.add_member(Character("Test", strength=10, dexterity=10))
        chosen_one = party.members[0]
        chosen_skill = skill(primary_attribute=Strength(), secondary_attribute=Dexterity())
        
        event.resolve_choice(party, chosen_one, chosen_skill)
        self.assertEqual(event.status, EventStatus.FAIL)

class TestParty(unittest.TestCase):

    def test_add_member(self):
        party = Party()
        character = Character("Test")
        party.add_member(character)
        self.assertIn(character, party.members)

    def test_remove_member(self):
        party = Party()
        character = Character("Test")
        party.add_member(character)
        party.remove_member(character)
        self.assertNotIn(character, party.members)

class TestGame(unittest.TestCase):

    def test_battle_player_wins(self):
        game = Game()
        party = Party()
        party.add_member(Character("Test", strength=20))
        game.party = party
        opponent = Giant()
        result = game.battle(opponent)
        self.assertEqual(result, "Player")

    def test_battle_opponent_wins(self):
        game = Game()
        party = Party()
        party.add_member(Character("Test", strength=10))
        game.party = party
        opponent = Giant()
        result = game.battle(opponent)
        self.assertEqual(result, "Opponent")

    def test_battle_draw(self):
        game = Game()
        party = Party()
        party.add_member(Character("Test", strength=15))
        game.party = party
        opponent = Giant(strength=15)
        result = game.battle(opponent)
        self.assertEqual(result, "Draw")

if __name__ == '__main__':
    unittest.main()

#-----------------------------------newupdate-Faizan-3/28/2024 - 3:50--------------------------------------------------
# This is the final edit. we have already submitted with the previous edit in Visual Studio Code application in the attachments of sakai Assignments, but this is the most recent editted version.
# Please consider this as the most recent and final edit of the project.

#PROJECT PART 2 - Option 2) 2) Same project. Students will implement a dynamic front-end project using the python backend they've already created.
#I am using HTML Language to create the beckend and for the front end I am using Visual Studio Code application.
