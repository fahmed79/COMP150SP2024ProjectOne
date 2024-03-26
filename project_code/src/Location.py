import json

class Location:
    def create_custom_event_from_static_text_files(self):
        with open("path/to/file.txt", "r") as file:
            data = json.load(file)

        event = Event()  # Assuming Event class exists
        event.primary = data['primary_attribute']
        event.secondary = "dexterity"  
        event.prompt_text = "A dragon appears, what will you do"  
        event.fail = {"message": "You failed"}  
        event.pass_ = {"message": "You passed"}  

        return event
