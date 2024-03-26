# main.py
import json
import sys
from typing import List
import random


class Location:

    def __init__(self, parser, number_of_events: int = 1):
        self.parser = parser
        self.events = [Event(self.parser) for _ in range(number_of_events)]


    import json

    def create_custom_event_from_static_text_file(self, file_path):
        # load json file from path
        with open(file_path, "r") as file:
            data = json.load(file)

        return Event(self.parser, data)



from enum import Enum


class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"


class Event:

        def __init__(self, parser, data: dict = None):



            self.parser = parser
            # parse json file
            self.primary = data['primary_attribute']
            self.secondary = data['secondary_attribute']
            self.prompt_text = data['prompt_text']
            self.pass_ = data['pass']
            self.fail = data['fail']
            self.partial_pass = data['partial_pass']


            self.status = EventStatus.UNKNOWN
            self.fail = {
                "message": "You failed."
            }
            self.pass_ = {
                "message": "You passed."
            }
            self.partial_pass = {
                "message": "You partially passed."
            }
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
            # Get the primary and secondary attributes of the chosen skill
            skill_primary = chosen_skill.primary_attribute
            skill_secondary = chosen_skill.secondary_attribute
            
            # Check if the chosen skill's attributes overlap with the event's attributes
            if skill_primary == self.primary or skill_secondary == self.primary:
                # If the primary attribute of the chosen skill overlaps with the event's primary attribute
                # or if the secondary attribute of the chosen skill overlaps with the event's primary attribute,
                # the character passes
                self.set_status(EventStatus.PASS)
            elif skill_primary == self.secondary or skill_secondary == self.secondary:
                # If the primary attribute of the chosen skill overlaps with the event's secondary attribute
                # or if the secondary attribute of the chosen skill overlaps with the event's secondary attribute,
                # the character partially passes
                self.set_status(EventStatus.PARTIAL_PASS)
            else:
                # If there's no overlap between the chosen skill's attributes and the event's attributes,
                # the character fails
                self.set_status(EventStatus.FAIL)



import random
class Character:
    def __int__(self, name):
        self.name = name
        self.strength = name
        self.strength = random.randint(1,10)
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
        return f"{self.name}: Str({self.strength}), Dex({self.dexterity}), Con({self.constitution}), Vit({self.vitality}), End({self.endurance}), Int({self.intelligence}), Wis({self.wisdom}), Know({self.knowledge}), Will({self.willpower}), Spir({self.spirit})"

    def action(self):
        # Placeholder for character action
        print(f"{self.name} performs an action.")

# Define character classes with special abilities
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


class Game:

    def __init__(self, parser):
        self.parser = parser
        self.characters: List[Character] = []
        self.locations: List[Location] = []
        self.events: List[Event] = []
        self.party: List[Character] = []
        self.current_location = None
        self.current_event = None
        self.continue_playing = True

        self._initialize_game()

    def add_character(self, character: Character):
        """Add a character to the game."""
        self.characters.append(character)

    def add_location(self, location: Location):
        """Add a location to the game."""
        self.locations.append(location)

    def add_event(self, event: Event):
        """Add an event to the game."""
        self.events.append(event)

    def _initialize_game(self):
        """Initialize the game with characters, locations, and events based on the user's properties."""
        character_list = [Character() for _ in range(10)]
        location_list = [Location(self.parser) for _ in range(2)]

        for character in character_list:
            self.add_character(character)

        for location in location_list:
            self.add_location(location)

    def start_game(self):
        return self._main_game_loop()

    def _main_game_loop(self):
        """The main game loop."""
        while self.continue_playing:
            self.current_location = self.locations[0]
            self.current_event = self.current_location.getEvent()

            self.current_event.execute()

            if self.party is None:
                # award legacy points
                self.continue_playing = False
                return "Save and quit"
            else:
                continue
        if self.continue_playing is False:
            return True
        elif self.continue_playing == "Save and quit":
            return "Save and quit"
        else:
            return False


class User:

    def __init__(self, parser, username: str, password: str, legacy_points: int = 0):
        self.username = username
        self.password = password
        self.legacy_points = legacy_points
        self.current_game = self._get_retrieve_saved_game_state_or_create_new_game()
        self.parser = parser

    def _get_retrieve_saved_game_state_or_create_new_game(self) -> Game:
        new_game = Game(self.parser)
        return new_game

    def save_game(self):
        pass


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
        # Here you can add more logic as needed, e.g., validate input
        return User(parser, username=username, password=password)


class InstanceCreator:

    def __init__(self, user_factory: UserFactory, parser: UserInputParser):
        self.user_factory = user_factory
        self.parser = parser

    def _new_user_or_login(self) -> User:
        response = self.parser.parse("Create a new username or login to an existing account?")
        if "login" in response:
            return self._load_user()
        else:
            return self.user_factory.create_user(self.parser)

    def get_user_info(self, response: str) -> User | None:
        if "yes" in response:
            return self._new_user_or_login()
        else:
            return None

    def _load_user(self) -> User:
        pass





class Statistic:
    def __init__(self, legacy_points: int):
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
        """Generate a starting value for the statistic based on random number and user properties."""
        """This is just a placeholder for now. Perhaps some statistics will be based on user properties, and others 
        will be random."""
        return legacy_points / 100 + random.randint(1, 3)


class Strength(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Strength is a measure of physical power."


class User:

    def __init__(self, parser, username: str, password: str, legacy_points: int = 0):
        self.username = username
        self.password = password
        self.legacy_points = legacy_points
        self.parser = parser
        self.current_game = self._get_retrieve_saved_game_state_or_create_new_game()

    def _get_retrieve_saved_game_state_or_create_new_game(self) -> Game:
        new_game = Game(self.parser)
        return new_game

    def save_game(self):
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
            response = game_instance.start_game()
            if response == "Save and quit":
                user.save_game()
                print("Game saved. Goodbye!")
                sys.exit()
            elif response:
                print("Goodbye!")
                sys.exit()
    else:
        print("See you next time!")
        sys.exit()


if __name__ == '__main__':
    start_game()
#-------------------------------
# 3/22/2024 - Faizan Ahmed

import random

class Character:
    def __int__(self, name):
        self.name = name
        self.strength = name
        self.strength = random.randint(1,10)
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
        return f"{self.name}: Str({self.strength}), Dex({self.dexterity}), Con({self.constitution}), Vit({self.vitality}), End({self.endurance}), Int({self.intelligence}), Wis({self.wisdom}), Know({self.knowledge}), Will({self.willpower}), Spir({self.spirit})"

    def action(self):
        # Placeholder for character action
        print(f"{self.name} performs an action.")

# Define character classes with special abilities
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
        
# Faizan Ahmed - 11:47am - 2/23/24 
# Huukha Le - 4:50 PM - 2/25/24

class Party:
    def __int__(self):
        self.member = []
        
    def add_member(self, character):
        """Adding a character to the part. """
        self.member.append(character)
        
    def remove_member(self, character):
        """Remove a character from the party."""
        if character in self.members:
            self.members.remove(character)
        else:
            print(f"{character.name} is not a member of the party.")

    def list_members(self):
        """List all members of the party."""
        print("party Members:")
        for member in self.members:
            print(member)

#game.py

from party import Party
from characters import Kratos, Loki, Odin, Thor
import random

class Game:
    def __init__(self):
        self.party = Party()
        self.events = []
        self.opponents = [WorldSerpent(), Fenrir(), Surtur(), Hel()]

    def add_party_member(self, character):
        """Add a character to the party."""
        self.party.add_member(character)

    def remove_party_member(self, character):
        """Remove a character from the party."""
        self.party.remove_member(character)

    def start_game(self):
        """Start the game loop."""
        print("Welcome to Ragnarok!")

        # Let the player choose gods characters to play with
        print("Choose which gods characters to play with:")
        print("1. Kratos\n2. Loki\n3. Odin\n4. Thor")
        choices = input("Enter the numbers of the characters (e.g., '1 3' for Kratos and Odin): ").split()

        # Add selected gods characters to the party
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

        # Display party composition
        print("Your party:")
        for members in self.party.members:
            print(members.name)

        # Battle against all giants
        print("Prepare to face the giants in the final battle of Ragnarok!")
        for opponent in self.opponents:
            print(f"You are facing {opponent.name}: {opponent.ability()}")

# Example usage:
game = Game()
game.start_game()

# in this game class above, we import the 'Party class' and the character classes (kratos, loki, odin, and thor)
# Movng on in Game class, we initialize a 'Party' instance to manage the player's party
# the 'start_game' method starts the game loop and  right now displaying welcome message
# lastly, at the bottom we deamand to start the game by calling the 'start_game' method.

# March 25, 2024 - Faizan Ahmed

    class Event:
        def __int__(self):
            self.description = "A random event occurs."
            self.success = "You succeeded!"
            self.failure_message = "You failed! "

        def execute(self, character):
            """Execute the event action for the given character."""
            print(self.description)
            # Placeholder: Implement event action based on character attributes
            if random.random() < 0.5:
                print(self.success_message)
            else:
                print(self.failure_message)


            
    
