# Sorting Algorithm Visualizer

An interactive web app built with Python and Dash that animates how Bubble Sort,
Selection Sort, and Insertion Sort work step by step on a random array of bars.

## Features

- Random array generation
- Bar-chart visualization of array values
- Dropdown to pick between Bubble Sort, Selection Sort, and Insertion Sort
- Start / Reset controls
- Real-time animated color coding:
  - **Orange** — elements currently being compared
  - **Red** — elements currently being swapped/shifted
  - **Green** — elements in their final sorted position

## Technologies Used

- Python 3.x
- Dash (Plotly)
- Plotly Graph Objects
- Git & GitHub for version control
- Deployed on: <!-- Render / Railway / PythonAnywhere -->

## Project Structure

```
sorting-visualizer/
├── algorithms/
│   ├── bubble_sort.py
│   ├── selection_sort.py
│   └── insertion_sort.py
├── assets/
│   └── style.css
├── app.py
├── requirements.txt
├── Procfile
└── README.md
```

## Setup Instructions (Local)

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd sorting-visualizer
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
  python app.py 
   ```
5. Open the URL printed in the terminal (usually http://127.0.0.1:8050).

## Deployment

This app is deployed on <!-- platform name --> and available at:
**<!-- your deployed URL here --> **

To deploy on Render:
1. Push this repo to GitHub.
2. Create a new Web Service on Render, connect the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:server`

## How It Works

Each sorting algorithm is implemented as a Python generator that yields the
array's state after every comparison and swap. The app pre-computes the full
list of animation frames when you click Start, then steps through them one at
a time using a `dcc.Interval` component to redraw the bar chart.

## Author

mohaddeseh badpa 