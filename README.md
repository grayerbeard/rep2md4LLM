# rep2md4LLM
A script to convert a GitHub Repository to a single Marrkdown file for feeeding as context to an LLM

## Editing Default Values

These are in "config.yaml" which you can edit to set up different defaults.

When script is run the default value is used unless the user inputs a different value.

```yaml
default_owner: grayerbeard # Replace with your default owner
default_repo: localAI  # Replace with your default repo
default_obsidian_vault_location: D:\Obsidian Vaults\Second Brain
default_obsidian_folder_for_output: notes  # (Optional) Folder for output file
default_output_filename: repoAsMD.md  # Replace with your defauly filename
default_files_to_exclude:  # List of files to exclude from the output
  - LICENSE
  - .gitignore
```

1. **Run the Script:**
   - Execute the Python script.
   - You withe all the values from the config.yaml file so an alternative may be entered.
   - If you press Enter without entering anything the default is used.
   - 
**Using With SystemSculpt AI :**

 **Using with SystemSculpt AI Plugin in Obsidian (two alternative ways):**
   Method One:
    - Open the generated markdown file in Obsidian.
    - At the end of the file type in a question together with details of how you want the question answered. (e.g. in Markdown format)
    - Use the SystemSculpt hotkey to send the entire file to the AI.
   Method Two:
    - You can add the generated markdown file as context in a chat. Click the "C" button at the bottom of the screen to start a chat then click the "Context Files +" button and enter in filename you used for the output.  Then enter your questions or your requests for changes to the files in the repository.