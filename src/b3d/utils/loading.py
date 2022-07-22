import os
from pkgutil import iter_modules
from importlib import import_module


def list_module(module):
    """
    Extract names of all top-level sub-modules given some parent module
    """
    return [
        name for _, name, is_pkg
        in iter_modules(
            [os.path.dirname(os.path.realpath(module.__file__))]
        )
        if not is_pkg
    ]


def find_objects(modules):
    """
    Extract fully qualified import paths for all sub-modules given some parent module
    """
    ret = set()
    for mod in modules:
        objects = [".".join([mod.__package__, m]) for m in list_module(mod) if mod != "__pycache__"]
        ret.update(objects)
    return sorted(ret)


def extend_resource_map(submodule):
    """
    Produce a dictionary with a single top-level key representing some AWS Service,
    further populated by resources contained within that service. The "submodule" argument
    is some sub-module of the src.b3d.resources module.
    """

    # Import objects from top-level module (e.g. src.b3d.resource.ec2)
    m = import_module(submodule)

    # List all classes included with this module
    module_classes = [
        getattr(m, c) for c in [c for c in dir(m) if c[0] != "_" and c != "Service"]
    ]

    # Extract top-level service type class from this module (for src.b3d.resource.ec2, this is EC2)
    top_level_service_classes = [sc for sc in module_classes if getattr(sc, "service_type", None) is not None]
    if len(top_level_service_classes) != 1:
        raise ValueError("There should be exactly one top level Service class per delete module.")
    top_level_service_class = top_level_service_classes[0]

    # Extract all resource classes from top-level service class
    cc = [
        c for c
        in dir(top_level_service_class)
        if c not in ["service_type", "Resource"] and c[0] != "_"
    ]

    return {
        top_level_service_class.service_type(): {
            getattr(top_level_service_class, c).resource_type(): getattr(top_level_service_class, c) for c in cc
        }
    }


def build_resource_map(module):
    """
    Populate and return a resource map consisting of top-level AWS service types
    (e.g. ec2, iam, etc.), and further keyed on resource types for that service
    (e.g. instances, policies, etc.).
    """

    resource_map = {}
    submodules = find_objects([import_module(module)])
    for sm in submodules:
        resource_map.update(extend_resource_map(sm))
    return resource_map
