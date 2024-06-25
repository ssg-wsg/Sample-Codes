# Tests

This folder contains the different unit tests and checkstyle tests that are used for CI/CD purposes.

You may freely extend or remove the test cases (spare for the checkstyle cases) as you see fit.

However, when extending or removing test cases, make sure to take note of the following points:

1. New test cases should adhere to the `unittest` framework and thus implement the `unittest.TestCase` class
2. When creating new files to store test classes and methods, ensure that the file name is prepended by `test_`
   1. e.g. If you wish to test the functionality of a class `A` located in `A.py`, the name of your test file should be
      `test_A.py`
3. Make sure that your test files' overall structure mirror that of the source code files.
   1. If you have a folder structure like `revamped_application/core/abc.py`, your test file should be located at
      `revamped_application/tests/core/test_abc.py`
   2. This ensures that test cases can be more easily found by developers and maintainers

## Resources

This folder is a special folder that contains resources that you might use in your tests.

You may freely add more test resources to this folder, but make sure not to remove existing resources as 
that may cause existing test cases to fail.

To get the path to the resources folder, you should reference `RESOURCES_PATH` in
`revamped_application/test/resources/definitions.py` and use it to form a path to the resource of interest.

```python
# example code
# if your resource is found at 'resources/test/resource.txt'
import os
from revamped_application.test.resources.definitions import RESOURCES_PATH

resource_path = os.path.join(RESOURCES_PATH, 'test', 'resource.txt')

with open(resource_path, 'r') as f:
    ...
```
