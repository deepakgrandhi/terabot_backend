'''
Workflow Engine Design Overview:
==Core Components of the Workflow Engine:
	*Workflow Manager: Responsible for starting and stopping workflows, managing their lifecycle.
	*Tile Executor: Executes the logic of each tile, triggering actions like API calls, logic checks, or sending emails.
	*Condition Evaluator: Evaluates conditions in LogicBuilderTile and determines the next tile to execute.
	*Data Handler: Stores and retrieves data between tile executions, e.g., user input or API responses.
	*Action Dispatcher: Sends out email notifications, API requests, or task assignments based on tile configuration.
	*State Manager: Keeps track of the current state of each workflow, ensuring smooth transitions between tiles.
'''
import logging
import json
from typing import Dict, Any, Optional
from TileExecuter import TileExecutor
#from workflow_manager import WorkflowManager

class WorkflowManager:
    def __init__(self):
        self.active_workflows = {}

    def start_workflow(self, workflow_id: str):
        logging.info(f"Starting workflow {workflow_id}")
        self.active_workflows[workflow_id] = "running"

    def stop_workflow(self, workflow_id: str, failed: bool = False):
        status = "failed" if failed else "completed"
        logging.info(f"Stopping workflow {workflow_id} with status {status}")
        self.active_workflows[workflow_id] = status

    def get_workflow_status(self, workflow_id: str) -> str:
        return self.active_workflows.get(workflow_id, "not started")
    
class WorkflowEngine:
    def __init__(self):
        """
        Initialize the WorkflowEngine which manages and executes workflows.
        """
        self.logger = logging.getLogger("WorkflowEngine")
        self.workflow_manager = WorkflowManager()
        self.tile_executor = TileExecutor()

    def run_workflow(self, workflow_id: str, workflow_definition: Dict[str, Any]) -> None:
        """
        Start the workflow execution based on its definition.

        Parameters:
        - workflow_id: The unique ID of the workflow.
        - workflow_definition: The structured workflow containing all tiles and configuration.
        """
        self.logger.info(f"Starting workflow execution: {workflow_id}")
        self.workflow_manager.start_workflow(workflow_id)

        try:
            current_tile_id = workflow_definition.get("start_tile")
            #print(current_tile_id)
            workflow_data = {}

            while current_tile_id:
                # Get the tile definition
                tile = self._get_tile_definition(workflow_definition, current_tile_id)

                if tile:
                    # Execute the tile logic
                    workflow_data = self.tile_executor.execute_tile(tile, workflow_data)
                    # Update the current tile based on flow jump or the next step
                    current_tile_id = workflow_data.get("next_tile")
                    #print("next id ",current_tile_id)

                    # If there's no next tile, end the workflow
                    if not current_tile_id:
                        self.logger.info(f"Workflow {workflow_id} completed.")
                        ##self.workflow_manager.stop_workflow(workflow_id)
                else:
                    self.logger.error(f"Tile with ID {current_tile_id} not found in workflow definition.")
                    raise ValueError(f"Tile with ID {current_tile_id} not found.")
        
        except Exception as e:
            self.logger.error(f"[workflowengine.py(77)]Error during workflow execution: {str(e)}")
            ##self.workflow_manager.stop_workflow(workflow_id, failed=True)

    def _get_tile_definition(self, workflow_definition: Dict[str, Any], tile_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve the definition of a tile from the workflow.

        Parameters:
        - workflow_definition: The structured workflow definition.
        - tile_id: The ID of the tile to retrieve.

        Returns:
        - The tile definition dictionary or None if not found.
        """
        '''for tile in workflow_definition.get("tiles", []):
            if tile.get("id") == tile_id:
                return tile
        return None'''
        tile_ids=workflow_definition.get("tileids",[])
        idx=tile_ids.index(tile_id)
        tile=workflow_definition.get("tiles")[idx]
        return tile

    '''def get_workflow_status(self, workflow_id: str) -> str:
        """
        Get the current status of the workflow.

        Parameters:
        - workflow_id: The unique ID of the workflow.

        Returns:
        - The current status of the workflow (e.g., running, completed, failed).
        """
        return self.workflow_manager.get_workflow_status(workflow_id)'''
    @staticmethod
    def load_workflow_from_file(file_path: str) -> Dict[str, Any]:
        """
        Load the workflow from a JSON file.

        Parameters:
        - file_path: The path to the JSON file containing the workflow definition.

        Returns:
        - The workflow definition as a dictionary.
        """
        with open(file_path, 'r') as file:
            workflow_definition = json.load(file)
        return workflow_definition



if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO)

    # Sample workflow definition for testing
    # Load workflow definition from a JSON file
    file_path = "workflowengine2\workflow1.json"  # Update with your file path
    workflow_definition = WorkflowEngine.load_workflow_from_file(file_path)


    # Instantiate the WorkflowEngine and run a sample workflow
    
    workflow_engine = WorkflowEngine()
    ##workflow_engine.run_workflow(workflow_definition["workflow_id"], workflow_definition)
    workflow_engine.run_workflow(workflow_definition["workflow_name"], workflow_definition)