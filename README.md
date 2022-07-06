# b3d
Boto3 utility library that supports deletion of collections of AWS resources (such as temporary resources created during unit tests).


### Structure

Many AWS resources enforce a particular ordering on their deletion, i.e. you can't delete an IAM policy if it is currently
attached to an instance, etc. If we want the high-level flow of this library to be something like (1) query all resources
tagged {A: B}, then remove them all, we would need to first order those resources by whatever deletion procedure AWS 
enforces, which won't always be a clean ordering (e.g. EC2 resources, then Lambda resources, then, IAM resources) if we
were to expand this library to support more than a couple AWS service or resource types. Any top-level ordering we'd 
try to impose would likely get super complicated as well, and I would definitely forget important details, which would 
cause it to get very messy very quickly.

The top-level flow for this design is still the same as it was previously (query ARNs, iterate over those arns and delete
them), but instead of trying to order the deletion stuff around AWS Services, I made specific Service & Resource container
classes, each with their own destroy() function that will have all the ordering logic for each resource contained there.
This will help keep the delete procedures for each resource type atomic, which will mitigate later messiness in the library.

The destroy() logic for each resource type should be minimal, in the sense that actual deletion of resources not included
in that resource type should be avoided. For example, when deleting an IAM policy, if that policy is attached to some 
EC2 instance, the policy should be detached from that instance before being deleted, rather than deleting the instance
outright. This also helps keep delete logic atomic, which will allow us to support arbitrarily many AWS resource types
in the future.
