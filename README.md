## One Stitch Simulator

Simulates and generates running stitch patterns.
Handles 4 stitch passes, East, North East, North, and North West

### Run tests

```
pytest -q
```

### Lint

```
ruff check
ruff format
```
### Run

```
python one_stitch.py

# If impatient set NO_ANIMATION = True

```

### Some Patterns

#### Chaotic
```
H_ROW_PATTERNS = [
    "00110011",
    "11001100",
    "00110011",
    "00110011",
    "11001100",
    "00110011",

]
V_COL_PATTERNS = [
    "00110011",
    "11001100",
    "00110011",
    "11001100",
    "11001100",
]
NE_DIAG_PATTERNS = []

NW_DIAG_PATTERNS = []
```
#### Neat
```
H_ROW_PATTERNS = ["0101", "1010"]
V_COL_PATTERNS =  ["0011", "1100"]
NE_DIAG_PATTERNS = []

NW_DIAG_PATTERNS = []
```

#### Juji Hanashi
```
H_ROW_PATTERNS = ["0", "0011", "0", "1100"]
V_COL_PATTERNS = ["0", "0011", "0", "1100"]
NE_DIAG_PATTERNS = ["00", "00", "00", "10", "00", "01", "00", "00"]

NW_DIAG_PATTERNS = ["01", "00", "00", "00", "00", "00", "10", "00"]


```
#### Kakinohana

```
H_ROW_PATTERNS = [ "0101", "1010", "0101", "1010", "1010",]
V_COL_PATTERNS =  [ "0101", "1010", "0101", "1010", "1010",]
NE_DIAG_PATTERNS = []

NW_DIAG_PATTERNS = []
```