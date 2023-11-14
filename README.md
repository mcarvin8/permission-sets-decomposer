# Salesforce - Combine & Separate Permission Sets
Large permission sets can be a source of merge conflicts and specific permissions can be lost if multiple developers are working on the same permission set and they do not have certain objects in their sandboxes.

If you wish to separate permission sets into individual files for each permission for version control, run the separate script after retrieving all permission sets from the production org.

Run the combine script to re-combine permission sets for deployments.

Use the provided `.gitignore` and `.forceignore` to have Git ignore the original meta files and have the Salesforce CLI ignore the separated XML files.

The package parsing script can be used if you deploy with a manifest file (package.xml) and want to only compile permission sets declared in the manifest.
