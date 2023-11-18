import re
import os

from openai import OpenAI
from typing import Tuple, List
from dataclasses import dataclass

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(
    api_key = OPENAI_API_KEY
)

NamePronc = Tuple[str, str]
curated_examples: List[NamePronc] = [
    ('Siobhan', 'Shi-VAWN'),
    ('Saoirse', 'SEE-uh-shuh'),
    ('Caoilfhionn', 'KWEE-lan')
]

def format_example(example) -> str:
    name, pronc = example
    return f'({name}) : [[{pronc}]]'

def is_correct_format(s: str) -> bool:
    pattern = r'\([A-Za-z]+\)\s:\s\[\[[A-Za-z\-]+\]\]'
    return bool(re.match(pattern, s))

def parse_example(s: str) -> NamePronc:
    if not is_correct_format(s):
        raise ValueError("String is not in the correct format")

    name = re.search(r'\((.*?)\)', s).group(1)
    pronc = re.search(r'\[\[(.*?)\]\]', s).group(1)
    return name, pronc


PROMPT_TEMPLATE = """
Give a simple English pronunciation guide for this Irish name: {name}

Strictly follow the following format:
(<NAME>) : [[<PRONUNCIATION>]]

E.g: 
(Caoilfhionn) : [[GWEE-lan]]
(Saoirse) : [[SEE-uh-shuh]]
(Siobhan) : [[Shi-VAWN]]
"""

async def get_response(name: str) -> 'ChatCompletionMessage':
    PROMPT = PROMPT_TEMPLATE.format(name = name)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": "You are a helpful assistant."
            },
            {   "role": "user", 
                "content": PROMPT
            }
        ]
    )
    return completion.choices[0].message

if __name__ == "__main__":
    # print(get_response('Aoife'))
    print(get_response('Caoimhe'))

