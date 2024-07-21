# rep2md4LLM
A script to convert a GitHub Repository to a single Marrkdown file for feeeding as context to an LLM

## Editing Default Values

These are in "config.yaml" which you can edit to set up different defaults.

```yaml
default_repo: https://github.com/grayerbeard/localAI  # Replace with your default repo
output_folder: D:/Obsidian Vaults/Second Brain/notes  # Folder for output file
output_filename: "repoLocalAI.md"  # output filename
```

1. **Run the Script:**
   - Execute the Python script.
   - You will be prompted to enter a GitHub repository URL.
   - If you press Enter without typing a URL, the script will use the `default_repo` from your `config.yaml` file.

2. **Output:**
   - The script will create a Markdown file using the filename and folders specified.
   - A success message will be printed to the console, indicating the location of the generated Markdown file.

**Using With SystemSculpt AI :**

 **Using with SystemSculpt:**
    - Open the generated markdown file in Obsidian.
    - At the end of the file type in a question together with details of how you want the question answered. (e.g. in Markdown format)
    - Use the SystemSculpt hotkey to send the entire file to the AI.
    - ALTERNATIVLEY you can add the generated markdown file as context in a chat. Click the "C" button at the bottom of the screen to start a chat then click the "Context Files +" button and enter "context".  Then enter your question(s).

Now you can request changes that will use all the files as context