# ILMT generator
## Description
This simple generator is to be used in order to create a dataframe resolving real data
from ILMT, which can be used for testing purposes 
## How to use it
```bash
python3 pip install -r requirements.txt
```
or just
```bash
pip install -r requirements.txt
```
Then
```python
from main import Generator

gen = Generator(
    1000,
    "path_to_your_file.csv"
)
print(gen.generate())
```
### Alternatively you can work inside main.py script :)
