import asyncio
import os
import sys
from dotenv import load_dotenv

from datetime import date

from typing_extensions import NotRequired, TypedDict

from pydantic_ai import Agent


load_dotenv()

# Checken, ob der API-Key gesetzt ist
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable not set.")
    print("Please create a .env file with your OpenAI API key or set it in your environment.")
    sys.exit(1)

class UserProfile(TypedDict):
    name: str
    dob: NotRequired[date]
    bio: NotRequired[str]
    response: str


agent = Agent(
    os.getenv("MODEL_CHOICE", "gpt-4.1-mini"),
    output_type=UserProfile,
    system_prompt='Extract a user profile from the input and finish with a response',
)


async def main():
    user_input = 'My name is Ben, I was born on January 28th 1990, I like the chain the dog and the pyramid.'
    async with agent.run_stream(user_input) as result:
        async for profile in result.stream_output():
            print(profile)
            #> {'name': 'Ben'}
            #> {'name': 'Ben'}
            #> {'name': 'Ben', 'dob': date(1990, 1, 28), 'bio': 'Likes'}
            #> {'name': 'Ben', 'dob': date(1990, 1, 28), 'bio': 'Likes the chain the '}
            #> {'name': 'Ben', 'dob': date(1990, 1, 28), 'bio': 'Likes the chain the dog and the pyr'}
            #> {'name': 'Ben', 'dob': date(1990, 1, 28), 'bio': 'Likes the chain the dog and the pyramid'}


if __name__ == "__main__":
    asyncio.run(main())