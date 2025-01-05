# My Bookshelf

My Bookshelf is a Python-based application designed to help you organize and manage your reading journey. Whether you're an avid reader or someone looking to track your literary aspirations, My Bookshelf provides a simple and intuitive interface to keep your book collection in order.

Key Features:
* Track Your Reading Status: Categorize books into three lists—Read, Currently Reading, and To Be Read (TBR)—for seamless organization.
* Progress Tracking: For books you're currently reading, log your progress to stay motivated and monitor how far you've come.
* Search and Filter: Quickly locate books using filters based on title, author, genre, or reading status.

Use Cases:
* Keep track of all the books you've read over time.
* Organize your current reads and stay on top of your reading goals.
* Build a wishlist of books you want to read in the future.

This Python application is perfect for readers of all types who want a practical way to manage their reading lists while keeping their literary adventures organized.

**Note**: The application is only available in Spanish and English depending on the OS language.

## Prerequisites

[Python](https://www.python.org/) It is recommended to use version 3.12 or higher.

### Setting up the Python environment and dependencies

1. Create a virtual environment:

* `cd <repository_directory>`
* `python3 -m venv venv`
* `source ./venv/bin/activate`

2. Install the dependencies:

* `pip3 install -r ./pip/requirements.txt`

## Running the Bookshelf

To run the Bookshelf run the following command inside the repository directory (after setting the Python environment):

`python3 ./my_bookshelf_app.py`

**Note**: The Bookshelf can be configured passing some optional arguments:

```
  --user USER  (Optional) The name of the user to log in with.
  --no-gui     Run the application in console mode.
```

## Icons

<a target="_blank" href="https://icons8.com/icon/1806/back">Back</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a></br>
<a target="_blank" href="https://icons8.com/icon/23662/book-shelf">Book Shelf</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a></br>
<a target="_blank" href="https://icons8.com/icon/PpPWnJWADeno/export-excel">Export Excel</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a></br>
<a target="_blank" href="https://icons8.com/icon/61/forward">Forward</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a></br>
<a target="_blank" href="https://icons8.com/icon/8ggStxqyboK5/star">Colored Star</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a></br>
<a target="_blank" href="https://icons8.com/icon/tAfqdu2AVpjT/star">Star</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a></br>
<a target="_blank" href="https://icons8.com/icon/6895/reading">Reading</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a></br>
<a target="_blank" href="https://icons8.com/icon/132/search">Search</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>

## Api

My Bookshelf uses the [Google Books APIs](https://developers.google.com/books) to retrieve book information. 