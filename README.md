# b3d
Boto3 utility library that supports deletion of collections of AWS resources (such as temporary resources created during unit tests).

# Usage

The function `b3d.delete_resources` is used to remove all AWS resources with a particular key / value tag
pair. It can be called as follows: 

```python
from b3d import delete_resources

reports = delete_resources("tag_key", "tag_value", "aws_region_name", dry=False)

# reports list might look like:
# [
#   {'result': 'success', 'err': None, 'msg': 'Successfully deleted api-key with ID zdmz8ysque'}, 
#   {'result': 'success', 'err': None, 'msg': 'Successfully deleted api-key with ID qwv83b4pj5'}
# ]
```

The returned `reports` will be a list of all resources affected by the deletion procedure, the type of action
performed (e.g. detachment from another resource, deletion), and whether that action was successful, along with
an error message if appropriate.

If `dry=True`, `delete_resources` will perform all the same queries on AWS resources, but all detach and
delete operations are skipped. The same reports list will be produced, but the resources themselves will
be unaffected.
