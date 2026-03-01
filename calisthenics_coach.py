from vision_agents.core import Agent, AgentLauncher, User, Runner
from vision_agents.plugins import getstream, gemini, ultralytics
from dotenv import load_dotenv
import os

load_dotenv()


# EXERCISE SELECTION
# Options: "pushups", "squats", "pullups", "planks", "dips", "burpees"

SELECTED_EXERCISE = "pushups"  # Change this line to switch exercises


EXERCISE_FILES = {
    "pushups": "instructions/pushups.md",
    "squats": "instructions/squats.md",
    "pullups": "instructions/pullups.md",
    "planks": "instructions/planks.md",
    "dips": "instructions/dips.md",
    "burpees": "instructions/burpees.md",
}

def load_instructions(exercise_name: str) -> str:
    """Load exercise-specific instructions from MD file."""
    file_path = EXERCISE_FILES.get(exercise_name)
    
    if not file_path:
        raise ValueError(f"Unknown exercise: {exercise_name}")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Instruction file not found: {file_path}")
    
    with open(file_path, 'r') as f:
        return f.read()

async def create_agent(**kwargs) -> Agent:
    
    instructions = load_instructions(SELECTED_EXERCISE)
    
    return Agent(
        edge=getstream.Edge(),
        agent_user=User(name=f"Calisthenics Coach ({SELECTED_EXERCISE.title()})", id="agent"),
        instructions=instructions,  # Loaded from MD file
        llm=gemini.Realtime(fps=10),
        processors=[ultralytics.YOLOPoseProcessor(model_path="yolo11n-pose.pt")],
    )

async def join_call(agent: Agent, call_type: str, call_id: str, **kwargs) -> None:
    call = await agent.create_call(call_type, call_id)
    async with agent.join(call):
        greeting = f"Hey! I'm your calisthenics coach. Let's work on your {SELECTED_EXERCISE}. Show me your form!"
        await agent.simple_response(greeting)
        await agent.finish()

if __name__ == "__main__":
    Runner(AgentLauncher(create_agent=create_agent, join_call=join_call)).cli()