'''
*'''

import requests
from urllib.parse import urlparse
from pathlib import Path
import yaml


def github_repo_to_markdown(repo_url, output_file):
  """
  Fetches files from a GitHub repository and combines them into a single Markdown file.

  Args:
    repo_url: The URL of the GitHub repository.
    output_file: The path to the output Markdown file.
  """

  # Extract repository information from URL
  parsed_url = urlparse(repo_url)
  if not (parsed_url.netloc == 'github.com' and len(parsed_url.path.split('/')) == 3):
    raise ValueError("Invalid GitHub repository URL.")
  owner, repo = parsed_url.path.strip('/').split('/')

  # Fetch repository contents
  api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/"
  response = requests.get(api_url)
  response.raise_for_status()
  contents = response.json()

  # Initialize Markdown content
  markdown_content = f"# Code from GitHub repository: {owner}/{repo}\n\n"
  markdown_content += "This document contains the content of all the files present in the root of the specified GitHub repository. Each file's content is placed under a heading corresponding to the filename.\n\n"

  # Iterate through files and append to Markdown
  for item in contents:
    if item['type'] == 'file':
      file_url = item['download_url']
      file_content = requests.get(file_url).text

      # Create a safe filename for the heading
      file_name = Path(item['path']).name
      heading = f"## {file_name}\n\n"

      markdown_content += heading + file_content + "\n\n"

  # Save the Markdown output to a file
  with open(output_file, "w", encoding="utf-8") as f:
    f.write(markdown_content)

  print(f"Markdown file created successfully at: {output_file}")

if __name__ == "__main__":
  # Load configuration from YAML file
  with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

  # Get default values from config
  default_repo = config.get("default_repo")
  output_folder = config.get("output_folder", ".")  # Default to current directory
  output_filename = config.get("output_filename", "repo_content.md")

  # Prompt user for repository URL (using default if not provided)
  repo_url = input(f"Enter GitHub repository URL (default: {default_repo}): ")
  if not repo_url:
    repo_url = default_repo

  # Construct the full output file path
  output_file = Path(output_folder) / output_filename

  # Call the function to generate the Markdown file
  github_repo_to_markdown(repo_url, output_file)