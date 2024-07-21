'''
**Explanation and How to Use:**

1. **Create `config.yaml`:**
   - Create a file named `config.yaml` in the same directory as your Python script.
   - Add the following content to `config.yaml`, replacing placeholders with your desired values:

     ```yaml
     default_repo: "https://github.com/username/repository"  # Replace with your default repo
     output_folder: "output"  # (Optional) Folder for output file
     output_filename: "repo_docs.md"  # (Optional) Custom filename
     ```

2. **Run the Script:**
   - Execute the Python script.
   - You will be prompted to enter a GitHub repository URL.
   - If you press Enter without typing a URL, the script will use the `default_repo` from your `config.yaml` file.

3. **Output:**
   - The script will create a Markdown file (using the filename and folder from `config.yaml` or defaults) containing the content of the specified GitHub repository.
   - A success message will be printed to the console, indicating the location of the generated Markdown file.

**Key Improvements:**

- **Configuration File:** Uses `config.yaml` to store default values, making the script more configurable.
- **User Input with Default:** Prompts the user for the repository URL but provides a default from the config file.
- **Output File Control:** Allows customizing the output folder and filename through `config.yaml`.
- **Clearer Organization:** Uses `if __name__ == "__main__":` block for better code structure.

Now you have a more flexible and configurable script to convert GitHub repositories to Markdown files for use with LL'''

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