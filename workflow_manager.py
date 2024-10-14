import logging
from typing import Dict, Any, Optional
from workflowengine_new import WorkflowEngine  # Assuming WorkflowEngine is implemented separately

# Setup logger for debugging and tracking workflow execution
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowManager:
    def __init__(self):
        """
        Initialize the Workflow Manager with empty containers for active workflows and workflow data.
        """
        self.active_workflows: Dict[str, WorkflowEngine] = {}  # Workflow instances indexed by workflow_id
        self.workflow_data_store: Dict[str, Dict[str, Any]] = {}  # Data associated with each workflow instance

    def start_workflow(self, workflow_id: str, workflow_definition: Dict[str, Any], initial_data: Optional[Dict[str, Any]] = None) -> None:
        """
        Starts the workflow execution by initializing its state and triggering the first tile.

        Parameters:
        - workflow_id: Unique identifier for the workflow instance.
        - workflow_definition: The configuration or structure that defines the workflow.
        - initial_data: Optional, initial input data to start the workflow.
        """
        if workflow_id in self.active_workflows:
            logger.warning(f"Workflow {workflow_id} is already running.")
            return

        # Initialize the workflow state using the WorkflowEngine
        try:
            workflow_engine = WorkflowEngine(workflow_definition)
            self.active_workflows[workflow_id] = workflow_engine
            self.workflow_data_store[workflow_id] = initial_data if initial_data else {}

            # Start the workflow
            workflow_engine.run_workflow(self.workflow_data_store[workflow_id])
            logger.info(f"Workflow {workflow_id} started successfully.")
        except Exception as e:
            logger.error(f"Error starting workflow {workflow_id}: {e}")
            raise

    def stop_workflow(self, workflow_id: str) -> None:
        """
        Stops the workflow execution and removes it from active workflows.

        Parameters:
        - workflow_id: Unique identifier for the workflow instance to be stopped.
        """
        if workflow_id in self.active_workflows:
            try:
                self.active_workflows[workflow_id].stop_workflow()
                del self.active_workflows[workflow_id]
                del self.workflow_data_store[workflow_id]
                logger.info(f"Workflow {workflow_id} stopped and removed.")
            except Exception as e:
                logger.error(f"Error stopping workflow {workflow_id}: {e}")
                raise
        else:
            logger.warning(f"Workflow {workflow_id} not found in active workflows.")

    def pause_workflow(self, workflow_id: str) -> None:
        """
        Pauses the execution of a workflow.

        Parameters:
        - workflow_id: Unique identifier for the workflow instance to be paused.
        """
        if workflow_id in self.active_workflows:
            try:
                self.active_workflows[workflow_id].pause_workflow()
                logger.info(f"Workflow {workflow_id} paused.")
            except Exception as e:
                logger.error(f"Error pausing workflow {workflow_id}: {e}")
                raise
        else:
            logger.warning(f"Workflow {workflow_id} not found.")

    def resume_workflow(self, workflow_id: str) -> None:
        """
        Resumes a paused workflow.

        Parameters:
        - workflow_id: Unique identifier for the workflow instance to be resumed.
        """
        if workflow_id in self.active_workflows:
            try:
                self.active_workflows[workflow_id].resume_workflow()
                logger.info(f"Workflow {workflow_id} resumed.")
            except Exception as e:
                logger.error(f"Error resuming workflow {workflow_id}: {e}")
                raise
        else:
            logger.warning(f"Workflow {workflow_id} not found.")

    def get_workflow_state(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the current state of the workflow, including its progress and data.

        Parameters:
        - workflow_id: Unique identifier for the workflow instance.

        Returns:
        - The current state of the workflow (e.g., the last executed tile, data).
        """
        if workflow_id in self.active_workflows:
            try:
                current_state = self.active_workflows[workflow_id].get_current_state()
                workflow_data = self.workflow_data_store.get(workflow_id, {})
                logger.info(f"Retrieved state for workflow {workflow_id}.")
                return {
                    "workflow_state": current_state,
                    "workflow_data": workflow_data
                }
            except Exception as e:
                logger.error(f"Error retrieving state for workflow {workflow_id}: {e}")
                raise
        else:
            logger.warning(f"Workflow {workflow_id} not found.")
            return None

    def get_all_active_workflows(self) -> Dict[str, Any]:
        """
        Returns a list of all currently active workflows.

        Returns:
        - A dictionary of all active workflows and their states.
        """
        try:
            active_workflow_list = {workflow_id: engine.get_current_state() for workflow_id, engine in self.active_workflows.items()}
            logger.info("Retrieved all active workflows.")
            return active_workflow_list
        except Exception as e:
            logger.error(f"Error retrieving active workflows: {e}")
            raise

    def restart_workflow(self, workflow_id: str) -> None:
        """
        Restarts a completed or failed workflow by re-initializing its state and starting from the beginning.

        Parameters:
        - workflow_id: Unique identifier for the workflow instance to be restarted.
        """
        if workflow_id in self.active_workflows:
            logger.warning(f"Workflow {workflow_id} is already running. Stop it first to restart.")
            return

        if workflow_id in self.workflow_data_store:
            workflow_definition = self.workflow_data_store[workflow_id]["workflow_definition"]
            initial_data = self.workflow_data_store[workflow_id]["initial_data"]

            self.start_workflow(workflow_id, workflow_definition, initial_data)
            logger.info(f"Workflow {workflow_id} restarted.")
        else:
            logger.error(f"Cannot restart workflow {workflow_id}. No data found.")

