# Salesforce - Combine & Separate Permission Sets
Large permission sets can be a source of merge conflicts and specific permissions can be lost if multiple developers are working on the same permission set and they do not have certain objects in their sandboxes.

If you wish to separate permission sets into individual files for each permission for version control, run the separate script after retrieving all permission sets from the production org.

```
- python3 ./separate_perms.py
```

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
