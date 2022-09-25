import asyncio
import json
import requests
from datetime import datetime


github_url = 'https://api.github.com/repos/{}'
head = """# Top Crypto & Blockchain Projects
A list of popular cryptocurrency and blockchain projects on github, automatically updated and ranked by stars every day\n
| Framework | Description | Language | Github Stars |
| --------- | ----------- | -------- | ------------ |
"""
tail = '\n*Last update:* {}'
with open('list.json', 'r') as f:
    projects = json.load(f)


async def fetch_data(projects, github_url):
    loop = asyncio.get_event_loop()
    futures = [loop.run_in_executor(None, requests.get, github_url.format(project)) for project in projects]
    try:
        responses = [response.json() for response in await asyncio.gather(*futures)]
        responses = sorted(responses, key=lambda response: response['stargazers_count'], reverse=True)
    except Exception as e:
        print(f'Exception occured during fetching the data: {e}')
    return responses

readme = ''
readme += head
responses = asyncio.run(fetch_data(projects, github_url))
for response in responses:
    readme += f'| [{response["full_name"]}]({response["html_url"]}) ' \
            f'| {response["description"]} ' \
            f'| {response["language"]} ' \
            f'| {response["stargazers_count"]} |\n'

readme += tail.format(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))

with open('README.md', 'w') as f:
    f.write(readme)
