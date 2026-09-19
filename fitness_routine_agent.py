"""Fitness Routine Planner Agent — a LangChain agent that helps create personalized fitness routines.

Setup: pip install -r requirements.txt, copy .env.example to .env, add your key.
Run:   python fitness_routine_planner_agent.py
"""

import logging
import os
import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("fitness_routine_planner")

load_dotenv()
if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY").startswith("sk-your"):
    logger.error("OPENAI_API_KEY not set. Copy .env.example to .env and add your key.")
    sys.exit(1)

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.2)

# ----------------------------------------------------------------------
# Tools
# ----------------------------------------------------------------------
ASSESSMENT_FITNESS_REQUIREMENTS_PROMPT = PromptTemplate(
    input_variables=["fitness_requirement_details"],
    template="""You are a professional fitness trainer.
Given the following fitness requirement details, identify suitable training focus, volume, recovery needs, and safety constraints and give a fitness requirements profile.

Fitness requirement details: {fitness_requirement_details}

Write the fitness requirements profile with:
- Training focus
- Volume
- Recovery needs
- Safety constraints

Return ONLY the fitness requirements profile, nothing else.""",
)

CREATE_WORKOUT_SCHEDULE_PROMPT = PromptTemplate(
    input_variables=["fitness_requirements_profile"],
    template="""You are an expert at creating workout schedules.

Take this fitness requirements profile and perform weekly routine with exercises, sets, repetitions, rest, warm-up, and progression to create a detailed workout plan.

Rules:
- Include exercises for each muscle group
- Specify sets, reps, and rest periods
- Consider the user's experience level
- Account for available equipment and time constraints

Fitness requirements profile:
{fitness_requirements_profile}

Return ONLY the workout plan, nothing else.""",
)


@tool
def assess_fitness_requirements(fitness_requirement_details: str) -> str:
    """Assess fitness requirements and create a fitness requirements profile."""
    logger.info("[assess_fitness_requirements] assessing: %s", fitness_requirement_details)
    return llm.invoke(ASSESSMENT_FITNESS_REQUIREMENTS_PROMPT.format(fitness_requirement_details=fitness_requirement_details)).content


@tool
def create_workout_schedule(fitness_requirements_profile: str) -> str:
    """Create a workout schedule based on the fitness requirements profile."""
    logger.info("[create_workout_schedule] creating schedule")
    return llm.invoke(CREATE_WORKOUT_SCHEDULE_PROMPT.format(fitness_requirements_profile=fitness_requirements_profile)).content


# ----------------------------------------------------------------------
# Agent
# ----------------------------------------------------------------------

SYSTEM_PROMPT = """Act as a conservative general fitness coach, not a medical professional. Always use assess_fitness_requirements before create_workout_schedule and advise professional guidance for pain or medical concerns.

When the user gives you a fitness routine description, follow these steps:
1. First, use the assess_fitness_requirements tool to create a fitness requirements profile.
2. Then, use the create_workout_schedule tool to create a detailed workout schedule.
3. Return the final structured workout plan to the user.

Always use both tools in order: identify fitness requirements, then create workout schedule."""

agent = create_agent(model=llm, tools=[assess_fitness_requirements, create_workout_schedule], system_prompt=SYSTEM_PROMPT)


def run_fitness_routine_planner(routine_description: str) -> str:
    """Run the agent on a fitness routine description and return the planned routine."""
    result = agent.invoke({"messages": [HumanMessage(content=routine_description)]})
    return result["messages"][-1].content


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

def main() -> None:
    print("\nFITNESS ROUTINE PLANNER AGENT (LangChain + OpenAI)")
    print("Describe the fitness routine you want to create like your Goal, experience, available days, equipment and any preferences/limitations. Type 'quit' to exit.\n")

    while True:
        routine_description = input("Your fitness routine description: ").strip()
        if not routine_description:
            continue
        if routine_description.lower() in ("quit", "exit", "q"):
            break

        try:
            workout_plan = run_fitness_routine_planner(routine_description)
            print("\n" + "=" * 60)
            print(workout_plan)
            print("=" * 60 + "\n")
        except Exception as e:
            logger.error("Agent failed: %s", e)


if __name__ == "__main__":
    main()
