# b3d
Boto3 utility library that supports deletion of collections of AWS resources (such as temporary resources created during unit tests).

# Usage

The function `b3d.delete_resources` is used to remove all AWS resources with a particular key / value tag
pair. It can be called as follows: 

```python
from b3d import delete_resources

reports = delete_resources("tag_key", "tag_value", "aws_region_name", dry=False)
```

The `delete_resources()` function returns an iterator whose elements are lists of reports for each single resource.
A list of reports is yielded (rather than an individual report) because a delete procedure might involve detaching 
any number of resources from the target resource first. Each report will detail the type of action performed (e.g. 
detachment from another resource, deletion, noop), whether that action was successful, and an error message if 
appropriate.

If `dry=True`, `delete_resources` will perform all the same queries on AWS resources, but all detach and delete 
operations will be skipped. The same reports list will therefore be produced, but the resources themselves will be 
unaffected.
