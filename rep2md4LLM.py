import requests
from urllib.parse import urlparse
from pathlib import Path
import yaml
import os
import time

def get_public_repo_contents(owner, repo, path=""):
    '''Note: While an access token isn't required for public repositories, using one can provide benefits like:

    Higher rate limits: You'll be able to make more API requests per hour.
    Access to private repositories: Obviously, this is only applicable to private repositories.
    Additional features: Some API endpoints might require authentication.
    If you anticipate high usage or need to access private repositories, consider using an access token.'''
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for error HTTP statuses
    return response.json()

def github_repo_to_markdown(owner, repo, output_file, exclude_files):
    """
    Fetches files from a GitHub repository and combines them into a single Markdown file.
    Args:
        owner: The owner of the GitHub repository.
        repo: The Repository within the Github Repository
        output_file: The path to the output Markdown file.
        exclude_files: List of filenames to exclude from the output.
    """
    # Fetch repository contents
    print(f"Will try to get contents of repo with Owner: {owner} and Repo: {repo}")
    try:
        contents = get_public_repo_contents(owner, repo, path="")
    except:
        print(f"Error getting repository Contents")  
        exit()  

    # Initialize Markdown content
    markdown_content = f"# Code from GitHub repository: {owner}/{repo}\n\n"
    markdown_content += "This document contains the content of files present in the root of the specified GitHub repository. Each file's content is placed under a heading corresponding to the filename.\n\n"

    # Convert exclude_files to a list if it's a string
    if isinstance(exclude_files, str):
        exclude_files = [file.strip() for file in exclude_files.split(',')]

    # List to store omitted files
    omitted_files = []

    # Iterate through files and append to Markdown
    for item in contents:
        if item['type'] == 'file':
            file_name = Path(item['path']).name
            print(f"Checking if {file_name} is in {exclude_files}")
            if file_name not in exclude_files:
                print(f"File {file_name} is not excluded")
                file_url = item['download_url']
                file_content = requests.get(file_url).text

                # Create a heading for the file
                heading = f"## {file_name}\n\n"

                # Add file content wrapped in code blocks
                markdown_content += heading + f"```\n{file_content}\n```\n\n"
            else:
                print(f"File {file_name} found to be in excluded files")
                omitted_files.append(file_name)

    # Add list of omitted files
    if omitted_files:
        markdown_content += "## Files omitted from output\n\n"
        for file in omitted_files:
            markdown_content += f"- {file}\n"

    # Save the Markdown output to a file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"Markdown file created successfully at: {output_file}")

if __name__ == "__main__":
    # Load configuration from YAML file
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    # Get default values from config
    default_owner = config.get("default_owner","missed")
    default_repo = config.get("default_repo","missed")
    default_obsidian_vault_location = config.get("default_obsidian_vault_location","missed")
    default_obsidian_folder_for_output = config.get("default_obsidian_folder_for_output","missed")
    default_output_filename = config.get("default_output_filename","missed")
    default_files_to_exclude = config.get("default_files_to_exclude","missed")

    # Prompt user for repository URL (using default if not provided)
    owner = input(f"Enter GitHub repository owner (default: {default_owner}): ") or default_owner 
    repo = input(f"Enter GitHub repository name (default: {default_repo}): ") or default_repo
    obsidian_vault_location = input(f"Enter Obsidian Vault Location (default: {default_obsidian_vault_location}): ") or default_obsidian_vault_location
    
    obsidian_folder_for_output = input(f"Enter Obsidian folder for Output (default:{default_obsidian_folder_for_output})") or default_obsidian_folder_for_output
    
    output_filename = input(f"Enter output filename (default: {default_output_filename})") or default_output_filename
    
    exclude_files = input(f"Enter files to exclude (default: {default_files_to_exclude})") or default_files_to_exclude

    # Construct the full output file path
    full_output_folder = os.path.join(obsidian_vault_location,obsidian_folder_for_output)
    if not os.path.exists(full_output_folder):
        print(f"Error: The output folder {full_output_folder} does not exist.")
        exit(1)
    output_file = os.path.join(full_output_folder,output_filename)
    if os.path.exists(output_file):
        # Get the current datetime
        dt = str(time.strftime('%Y%m%d%H%M%S'))
        # Create the new filename with the timestamp
        newname = f'output_file_{dt}.md'
        os.rename(output_file,newname)
        print(f"The specified Output file exists so old file renamed to {newname}")

    # Call the function to generate the Markdown file
    github_repo_to_markdown(owner, repo, output_file, exclude_files)