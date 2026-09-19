# Smart Service Center Engine

A command-line Python application that manages customer service requests using
manually implemented Queue, Stack, Hash Table, sorting algorithms (Bubble,
Selection, Insertion), and search algorithms (Sequential, Binary, Hash lookup).

## Files

- `System.py` — main program (menu, request handling, entry point)
- `Data_Stractures.py` — `Stack`, `Queue`, `HashTable` classes
- `Algorithms.py` — sorting and searching algorithms
- `System_Dataset.xlsx` — dataset with 4 sheets: `Random Order` (used as the live
  working data for the menu), plus `Already Sorted`, `Reverse Sorted`, and
  `Nearly Sorted` (used only for comparing sort algorithm behavior in the
  written analysis, not loaded into the live menu)
- `analysis.md` — written answers to the required analysis questions

## Requirements

- Python 3.8+
- `pandas` and `openpyxl` (for reading the `.xlsx` file)

Install dependencies:
```
pip install pandas openpyxl
```

## Setup

1. Place `System.py`, `Data_Stractures.py`, `Algorithms.py`, and
   `System_Dataset.xlsx` in the same folder.
2. Open `System.py` and update the `file_path` variable (near the top) to
   point to your local copy of `System_Dataset.xlsx`, for example:
   ```python
   file_path = r"C:\path\to\your\System_Dataset.xlsx"
   ```
   On macOS/Linux, use a normal path instead, e.g.
   `file_path = "System_Dataset.xlsx"` if it's in the same folder.

## Running the Program

From the project folder, run:
```
python System.py
```

You'll see a numbered menu:
```
[1]  Add incoming request
[2]  Process next request
[3]  Show waiting queue
[4]  Show processed requests
[5]  Sort requests
[6]  Sequential Search
[7]  Binary Search
[8]  Hash lookup
[9]  View/remove last search
[10] Show algorithm statistics
[11] Exit
```
Enter the number of the option you want and follow the prompts. The menu
keeps running until you choose `[11]` to exit.

## Notes

- New requests are validated (ID, name, priority 1–5, estimated time,
  duplicate ID) before being accepted; invalid ones are stored with a
  `Rejected` status instead of crashing the program.
- Every search (Sequential, Binary, Hash) is automatically logged to a
  search-history Stack, viewable/removable via option `[9]`.
- Option `[10]` prints statistics from the most recent sort and search
  performed in the current session.

## Bonus: Hash Collision Handling

The `HashTable` class handles collisions via separate chaining — each bucket
is a list, and `get()` searches within the bucket for the exact matching
`Request ID` rather than assuming one record per index. To see this directly:
add a request with an ID that is exactly `table_size` away from an existing
ID (e.g. `1041` and `1221`, since the table size is `180` and
`1221 % 180 == 1041 % 180`). Both records land in the same bucket, and
`get(1041)` / `get(1221)` (via Hash lookup, option `[8]`) each correctly
return their own record.
