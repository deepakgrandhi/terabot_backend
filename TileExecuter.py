import logging
import json
from typing import Any, Dict, Optional
from tiles_new import UserInteractionTile , LogicBuilderTile,FlowJumpTile,APICallTile 

class TileExecutor:
    def __init__(self):
        """
        Initialize TileExecutor to execute tile logic.
        """
        #self.supported_tiles = ["UserInteraction", "LogicBuilder", "FlowJump", "APICall"]
        self.supported_tiles = {
            "UserInteractionTile": UserInteractionTile,
            "LogicBuilderTile": LogicBuilderTile,
            "FlowJumpTile": FlowJumpTile,
            "APICallTile": APICallTile
        }
        self.logger = logging.getLogger("TileExecutor")

    def execute_tile(self, tile: Dict[str, Any], workflow_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Executes the logic of the provided tile and returns updated data.
        
        Parameters:
        - tile: The tile configuration containing the type and necessary parameters.
        - workflow_data: The current workflow data available for the tile execution.

        Returns:
        - Updated workflow data after tile execution.
        """
        tile_type = tile.get("type")
        tile_name = tile.get("name", "UnnamedTile")
        tile_config = tile.get("configuration", {})
        print(tile_type)

        if tile_type not in self.supported_tiles:
            self.logger.error(f"Unsupported tile type: {tile_type}")
            raise ValueError(f"Unsupported tile type: {tile_type}")

        #self.logger.info(f"Executing tile: {tile_type}")
        self.logger.info(f"Executing tile: {tile_name} of type: {tile_type}")
        # Dynamically create the tile instance based on tile type
        tile_instance = self.supported_tiles[tile_type](tile_name)
        if tile_type == "UserInteractionTile" :
            #return self._execute_user_interaction_tile(tile, workflow_data)
            print("exucting user interaction config")
            self._configure_user_interaction_tile(tile_instance, tile_config)
        elif tile_type == "LogicBuilderTile":
            #return self._execute_logic_builder_tile(tile, workflow_data)
            print("exucting logic builer config")
            self._configure_logic_builder_tile(tile_instance, tile_config)
        elif tile_type == "FlowJumpTile" :
            #return self._execute_flow_jump_tile(tile, workflow_data)
            print("exucting FlowJumpTile config")
            self._configure_flow_jump_tile(tile_instance, tile_config)
        elif tile_type == "APICallTile" :
            #return self._execute_api_call_tile(tile, workflow_data)
            print("exucting APICallTile config")
            self._configure_api_call_tile(tile_instance, tile_config)
        

        # Execute the tile and update workflow data
        updated_data = tile_instance.execute()
        workflow_data.update(updated_data or {})
        return workflow_data

        #return workflow_data
    def _configure_user_interaction_tile(self, tile_instance, config: Dict[str, Any]):
        prompt = config.get("prompt", "Enter your choice:")
        options = config.get("options", ["Yes", "No"])
        next_tile=config.get("next_tile",None)
        tile_instance.configure(prompt, options,next_tile)
    def _configure_logic_builder_tile(self, tile_instance, config: Dict[str, Any]):
        condition = config.get("condition", True)
        true_tile_name = config.get("true_tile")
        false_tile_name = config.get("false_tile")
        #true_tile = Tile(true_tile_name) if true_tile_name else None
        #false_tile = Tile(false_tile_name) if false_tile_name else None
        tile_instance.configure(condition, true_tile_name, false_tile_name)
    def _configure_flow_jump_tile(self, tile_instance, config: Dict[str, Any]):
        jump_target_name = config.get("jump_target")
        #jump_target = Tile(jump_target_name) if jump_target_name else None
        tile_instance.configure(jump_target_name)

    def _configure_api_call_tile(self, tile_instance, config: Dict[str, Any]):
        api_url = config.get("api_url", "https://example.com")
        http_method = config.get("http_method", "GET")
        params=config.get("params",{})
        payload = config.get("payload", {})
        next_tile=config.get("next_tile")
        tile_instance.configure(api_url=api_url, http_method=http_method, params=params,payload=payload,next_tile=next_tile)
    
    '''def _execute_user_interaction_tile(self, tile: Dict[str, Any], workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        # Handle user interaction, capture data or process input
        user_input = tile.get("user_input", "default_input")
        workflow_data["user_input"] = user_input

        self.logger.info(f"User input captured: {user_input}")
        return workflow_data

    def _execute_logic_builder_tile(self, tile: Dict[str, Any], workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        # Execute logic checks and updates
        logic_result = tile.get("logic_result", True)
        workflow_data["logic_result"] = logic_result
        self.logger.info(f"Logic evaluated: {logic_result}")
        return workflow_data

    def _execute_flow_jump_tile(self, tile: Dict[str, Any], workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        # Handle flow jumping logic
        next_tile_id = tile.get("next_tile_id", "default_tile")
        workflow_data["next_tile"] = next_tile_id
        self.logger.info(f"Flow jumped to: {next_tile_id}")
        return workflow_data

    def _execute_api_call_tile(self, tile: Dict[str, Any], workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        # Perform API call and update workflow data with the result
        api_result = {"response_data": "sample_data"}  # Simulated API result
        workflow_data["api_response"] = api_result
        self.logger.info(f"API call executed, response: {api_result}")
        return workflow_data'''

'''
with open('workflow1.json', 'r') as file:
        workflow_definition = json.load(file)
# Create an instance of the TileExecutor
tile_executor = TileExecutor()
# Simulate the workflow execution
workflow_data = {}

for tile in workflow_definition["tiles"]:
#    print(tile)
    tile_executor.execute_tile(tile, workflow_data)'''
    #workflow_data = tile_executor.execute_tile(tile, workflow_data)