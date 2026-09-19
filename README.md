# Fitness Routine Planner Agent

A LangChain agent that turns a plain-language fitness description into a safe,
structured beginner workout plan. It acts as a conservative general fitness
coach — not a medical professional — and always recommends professional
guidance for pain or medical concerns.

## Use case

Given a user's goal, experience level, available days, equipment, and any
stated limitations, the agent produces a weekly workout plan with exercises,
sets, reps, rest periods, warm-up, and progression guidance.

It does this with two chained tools, always used in order:

1. **`assess_fitness_requirements`** — Takes the raw fitness description and
   identifies a fitness requirements profile: training focus, volume,
   recovery needs, and safety constraints.
2. **`create_workout_schedule`** — Takes the requirements profile from Tool 1
   and produces the final structured weekly workout plan (exercises, sets,
   reps, rest, warm-up, progression).

The agent's system prompt enforces that Tool 1 always runs before Tool 2, and
that the agent advises consulting a professional for any pain or medical
concerns rather than working around them.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Copy the example environment file and add your OpenAI API key:
   ```
   cp .env.example .env
   ```
   Then edit `.env` and replace `sk-your-api-key-here` with your real key
   (get one at https://platform.openai.com/api-keys). `.env` is git-ignored
   and never committed.

## Run

```
python fitness_routine_agent.py
```

You'll be prompted to describe your fitness routine — mention your goal,
experience level, days available, equipment, and any limitations. Type
`quit` (or `exit` / `q`) to stop.

### Example

**Input:**
> I want to strengthen my knees and legs and I do running at least 2 miles a
> day and I like to work out mostly in the morning. I also have yoga classes
> in the morning from 6:30 to 7:30am and I am totally open in the weekend
> mornings. I don't have much health issues but I feel my flexibility
> reduced in my knees.

**Output (abridged):**
```
### Weekly Workout Plan: Lower Body Strength, Knee Stabilization & Flexibility

Monday – Lower Body Strength
  Step-ups (3x10 each leg), Wall Sit (3x30 sec), Glute Bridges (3x15),
  Seated Hamstring Curls (3x12 each leg), Calf Raises (3x20)

Tuesday – Yoga + Running
  2 mile easy run + yoga class (flexibility, balance, knee-friendly poses)

...

Progression & Safety
  - Gradually increase reps/time every 2 weeks if no knee pain
  - Avoid deep knee flexion beyond 90 degrees
  - Rest at least 48 hours between strength sessions targeting same muscles

If you experience any knee pain or discomfort, please consult with a
medical or physiotherapy professional before continuing or modifying
your routine.
```

## Project structure

```
fitness_routine_agent.py   # Agent, tools, and CLI
requirements.txt                   # Python dependencies
.env.example                       # Template for required environment variables
.gitignore                         # Excludes .env, .venv, __pycache__
```

## Notes

- This agent provides general fitness guidance only and is not a substitute
  for medical advice. Always consult a healthcare or fitness professional
  for pain, injuries, or medical conditions.
