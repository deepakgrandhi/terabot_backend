import requests

class Tile:
    def __init__(self, name):
        self.name = name
        self.connected_tiles = []  # To store connections to other tiles

    def configure(self, **kwargs):
        """Configure the tile with the required parameters."""
        pass

    def execute(self):
        """Execute the tile's functionality."""
        pass

    def connect(self, tile):
        """Connect this tile to another tile."""
        self.connected_tiles.append(tile)
        print(f"{self.name} is now connected to {tile.name}")

class UserInteractionTile(Tile):
    def __init__(self, name):
        super().__init__(name)
        self.prompt = None
        self.options = []
        self.next_tile=None

    def configure(self, prompt, options,next_tile):
        """Set the user prompt and options for interaction."""
        self.prompt = prompt
        self.options = options
        self.next_tile=next_tile
        print(f"User Interaction Tile configured with prompt: '{self.prompt}' and options: {self.options}")
    def sendprompt(self):
        """Simulate user interaction by asking the prompt and receiving input."""
        print(f"Prompt: {self.prompt}")
        for idx, option in enumerate(self.options, 1):
            print(f"{idx}. {option}")
    def wait_for_response(self):
        # Wait for user input from CLI
        user_input = input("Please enter your choice: ")
        return user_input

    def execute(self):
        '''"""Simulate user interaction by asking the prompt and receiving input."""
        print(f"Prompt: {self.prompt}")
        for idx, option in enumerate(self.options, 1):
            print(f"{idx}. {option}")'''
        # Simulate user selecting an option
        #selected_option = self.options[0]  # Placeholder for user input
        selected_option = self.wait_for_response()
        print(f"User selected: {selected_option}")
        return {"selected_option":selected_option,"next_tile":self.next_tile}

class LogicBuilderTile(Tile):
    def __init__(self, name):
        super().__init__(name)
        self.condition = None
        self.true_tile = None
        self.false_tile = None

    def configure(self, condition, true_tile, false_tile):
        """Set the condition and the tiles to execute based on the condition."""
        self.condition = condition
        self.true_tile = true_tile
        self.false_tile = false_tile
        print(f"Logic Builder Tile configured with condition: {self.condition}")

    def execute(self):
        """Execute based on the condition."""
        if self.condition:
            print(f"Condition met, moving to {self.true_tile}")
            #return self.true_tile
            return {"next_tile":self.true_tile}
        else:
            print(f"Condition not met, moving to {self.false_tile}")
            #return self.false_tile
            return {"next_tile":self.false_tile}


class FlowJumpTile(Tile):
    def __init__(self, name):
        super().__init__(name)
        self.jump_target = None

    def configure(self, jump_target):
        """Set the target tile to jump to."""
        self.jump_target = jump_target
        print(f"Flow Jump Tile configured to jump to {self.jump_target}")

    def execute(self):
        """Jump to the configured target."""
        print(f"Jumping to {self.jump_target}")
        #return self.jump_target
        return {"next_tile":self.jump_target}



class APICallTile(Tile):
    def __init__(self, name):
        super().__init__(name)
        self.api_url = None
        self.http_method = "GET"
        self.payload = None
        self.params={}
        self.next_tile=None

    def configure(self, api_url, http_method, params,payload,next_tile):
        """Set the API endpoint, HTTP method, and optional payload."""
        self.api_url = api_url
        self.http_method = http_method
        self.payload = payload
        self.params=params
        self.next_tile=next_tile
        print(f"API Call Tile configured with URL: {self.api_url}, Method: {self.http_method}")

    def execute(self):
        """Execute the API call and retrieve data."""
        try:
            if self.http_method == "GET":
                response = requests.get(self.api_url)
            elif self.http_method == "POST":
                response = requests.post(self.api_url, json=self.payload)
            else:
                print(f"Unsupported HTTP method: {self.http_method}")
                return None

            if response.status_code == 200:
                print(f"API Call successful. Data: {response.json()}")
                return {"response":response.json(),"next_tile":self.next_tile} # Returning the API response data
            else:
                print(f"API Call failed with status code: {response.status_code}")
                return {"response":None,"next_tile":None}
        except Exception as e:
            print(f"Error during API call: {e}")
            return {response:None,"next_tile":None}
        
'''# Create tile instances
user_interaction = UserInteractionTile("User Interaction 1")
logic_builder = LogicBuilderTile("Logic Builder 1")
flow_jump = FlowJumpTile("Flow Jump 1")
api_call = APICallTile("API Call 1")


# Configure tiles
user_interaction.configure(prompt="What is your choice?", options=["Option 1", "Option 2"])
logic_builder.configure(condition=True, true_tile=api_call, false_tile=flow_jump)
flow_jump.configure(jump_target=user_interaction)
api_call.configure(api_url="https://jsonplaceholder.typicode.com/posts/1", http_method="GET")


# Execute the workflow
user_interaction.execute()
next_tile = logic_builder.execute()  # Checks condition and routes to the API Call tile
next_tile.execute()  # Executes the API call and retrieves data'''