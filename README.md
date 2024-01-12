# Salesforce - Combine & Separate Permission Sets

**NOTICE**: This repository has been replaced by https://github.com/mcarvin8/sfdx-decomposer. Any updates required will be pushed to the sfdx-decomposer repository instead of this one.

Large permission sets can be a source of merge conflicts and specific permissions can be lost if multiple developers are working on the same permission set and they do not have certain objects in their sandboxes.

If you wish to separate permission sets into individual files for each permission for version control, run the separate script after retrieving all permission sets from the production org.

```
- python3 ./separate_perms.py
```

The script will fail to parse permission sets if the file-path exceeds the operating system limit. Ensure you use shorter permission set names when possible.
The error message `ERROR writing file: %s` will be printed in the terminal, but the script will continue parsing other permission sets.

Use the provided `.gitignore` and `.forceignore` to have Git ignore the original meta files and have the Salesforce CLI ignore the separated XML files.

For deployments, run the combine script to compile the permission sets.

Supply the `--manifest` argument if you deploy with a manifest file (package.xml) and want to only compile permission sets declared in the manifest.

```
- python3 ./combine_perms.py --manifest "./manifest/package.xml"
```

Otherwise, omit the argument to compile all permission sets in the default directory (`force-app/main/default/permissionsets`).

```
- python3 ./combine_perms.py
```
