# Notebook Code Standards

Applies to all Jupyter notebooks in research projects. These standards
prioritize readability for a human reviewer skimming the notebook
top-to-bottom, not performance or terseness.

---

## Headings

Use a Markdown heading to name each logical group of cells. Follow the heading
immediately with 1-2 sentences in plain English describing what the group does.
A reader skimming the notebook should know what is happening and why without
reading the code.

Rules:
- Do not use em-dashes or parentheses in headings or their descriptions.
- Keep descriptions to 1-2 sentences.
- Name the section after what it produces or decides, not after the technique it uses.

Example:

```markdown
## Load and filter play-by-play data
Read the raw Statcast CSV files and drop rows that are missing release speed or
plate location. These rows account for under 1 percent of pitches and cannot be
imputed reliably.
```

---

## Output formatting

Print results as plain labeled lines, not styled banners or dividers:

```python
# good
print(f"output: {accuracy:.3f}")
print(f"rows dropped: {n_dropped}")

# bad
print(f"===== RESULTS =====")
print(f"--- Accuracy: {accuracy:.3f} ---")
```

One output statement per logical result. No decorative `---/===` separators.

---

## Comments

One-line English comments above the code chunk they describe. No block
comment walls, no restating what the code obviously does:

```python
# remove incomplete rows and pitchers below the minimum sample threshold
df = df.dropna(subset=["pitch_speed", "spin_rate"])
df = df[df["pitch_count"] >= MIN_PITCHES]
df = df.reset_index(drop=True)
```

Write the comment as if explaining to a colleague what this chunk is for,
not what Python is doing mechanically.

---

## Docstrings

Complex functions get a short human-readable docstring: what it does, what
goes in, what comes out. Nothing more:

```python
def compute_era_plus(era, league_era):
    """
    Returns ERA+ (park/league adjusted ERA).
    era: float, pitcher ERA; league_era: float, league average ERA.
    Higher is better; 100 is league average.
    """
```

Simple utility functions (< 5 lines, obvious purpose) don't need one.

---

## Cell scope

Each cell does one logical thing — load, clean, transform, plot, or evaluate.
Not several at once. If a cell is doing two things, split it.

---

## Named constants

No unexplained inline numbers. Define them as named variables at the top of
the cell where they're used:

```python
TRAIN_SPLIT = 0.80
MIN_PITCHES = 50

train = df.sample(frac=TRAIN_SPLIT, random_state=42)
df = df[df["pitch_count"] >= MIN_PITCHES]
```

---

## Import hygiene

All imports go in a single cell at the top of the notebook. Never import
inside a later cell unless there is a specific reason (e.g., optional heavy
dependency). Keep stdlib, third-party, and local imports in that order,
separated by a blank line.

---

## Dead cell cleanup

No scratch cells, failed experiments, or commented-out code blocks left in
the notebook. Exploratory work either gets cleaned into a real cell or
deleted. The notebook that gets committed is readable start-to-finish.

---

## Variable naming

Full descriptive names. Abbreviations only when the full name is universally
known in the domain (`era`, `ops`, `whip` are fine in baseball; `ba` for
`batting_average` is not):

```python
# good
era_adjusted = era / league_era * 100
train_features, test_features = split(features)

# bad
era_adj = era / l_era * 100
X_tr, X_te = split(X)
```
