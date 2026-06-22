# Get Recc'd: Video Game Recommendation System

An AI-driven video game recommendation web application built with a semi-modular monolithic architecture. This application allows users to safely manage accounts, search for game recommendations via text titles or form criteria metadata, and stream matched cover art images dynamically. 

The architecture is deliberately structured to isolate specific domains, laying a clear blueprint for an easy migration to an autonomous microservices model.

---

## 🏗️ Architecture Blueprint

The project follows a **Semi-Modular Monolith** pattern. While running out of a single process engine, the internal layers are decoupled into strict domains:

*   **Orchestration / Gateway Layer (`app.py`, `main.py`)**: Manages routing, user session states, and coordinates network inputs.
*   **Authentication Subsystem (`auth.py`, `user.py`)**: Controls credential verification, secure password hashing, and account persistence.
*   **Analytics & Engine Module (`recommendation_service.py`)**: Uses `scikit-learn` TF-IDF vectors and Cosine Similarity computations to isolate and return the top 3 contextual game matches from a Kaggle dataset.
*   **Asset Hydration Service (`image_service.py`)**: Fetches game image URLs independently to keep database and UI code uncoupled.

```text
               +--------------------------------------+

               |        Web Browser (Frontend)        |
               +------------------+-------------------+
                                  | HTTP
                                  v
               +--------------------------------------+

               |    Orchestration Layer (app.py)      |
               +----+-----------------+------------+---+

                    |                 |            |
  (Internal Import) |                 |            | (Internal Import)
                    v                 |            v
    +-----------------------+         |      +------------------------+

    | Authentication Module |         |      | Cover Image Module     |
    |   (auth.py / user.py) |         |      |   (image_service.py)   |
    +-----------------------+         |      +------------------------+
                                      v 
                      +-------------------------------+

                      |  Recommendation Engine Module |
                      |  (recommendation_service.py)  |
                      +-------------------------------+
```

---

## ⚡ Quick Start

### 1. System Requirements
*   Python 3.10+
*   Pip (Python Package Installer)

### 2. Setup & Installation
Clone the repository and enter the workspace directory:
```bash
git clone https://github.com
cd CS361-Get-Recc-d-Game-Recommendation-Website
```

Create a python virtual environment and activate it:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

Install the application dependencies:
```bash
pip install flask pandas scikit-learn werkzeug requests
```

### 3. Data Ingestion
Place your downloaded Kaggle video game dataset into the root directory. Ensure the file name matches your configuration (e.g., `games_dataset.csv`) and contains columns for `title` and a text block mapping your target features/tags (`metadata`).

### 4. Run Execution
Initialize your application lifecycle pipeline using the project controller:
```bash
python app.py
```
Open your local browser environment and navigate to: `http://127.0.0.1:5000`

---

## 🔍 Module Specifications & API Design

### Authentication System (`auth.py`)
Provides access protection using `werkzeug.security` encryption wrappers.
*   `create_user(username, password) -> bool`: Hashes passwords and saves the profile to the storage database. Returns `False` if a username collision occurs.
*   `authenticate_user(username, password) -> dict | None`: Validates user credentials. Returns a dictionary with safe user profile metadata or `None`.

### Machine Learning Engine (`recommendation_service.py`)
Computes mathematical correlations between metadata tags.
*   `init_recommender()`: Reads raw CSV data structures, vectorized elements via TF-IDF, and maps out a static matrix cache.
*   `get_recommendations(game_title, criteria_tags) -> list[str]`: Evaluates spatial distances across data fields. Extracts exactly 3 matched titles based on the highest cosine proximity scores.

### Asset Processor (`image_service.py`)
*   `get_game_cover_url(game_title) -> str`: Builds an image placeholder asset route or fetches data from external gaming APIs (IGDB/RAWG) to resolve visual layout cards dynamically.

---

## 🚀 Microservices Migration Route

Because the codebase is semi-modular, you can break it out into individual microservices by following this implementation map:

### Phase 1: Create HTTP Wrapper Boundaries
Isolate a service (e.g., `recommendation_service.py`) into its own standalone directory running on its own local port (e.g., `:5002`). Wrap its methods with API endpoint contracts:

```python
# recommendation_service/microservice.py
from flask import Flask, request, jsonify
import recommendation_service as core

app = Flask(__name__)
core.init_recommender()

@app.route('/api/recommend', methods=['POST'])
def recommend_endpoint():
    data = request.json
    results = core.get_recommendations(data.get('title'), data.get('criteria'))
    return jsonify({"games": results})

if __name__ == '__main__':
    app.run(port=5002)
```

### Phase 2: Refactor Monolith to Call Network APIs
Update your primary orchestration gateway (`app.py`) to swap out standard Python function calls for lightweight, networked HTTP requests:

```python
# Inside app.py (Updated orchestrator route)
import requests

# OLD: raw_recs = recommendation_service.get_recommendations(title, criteria)
# NEW: Network hook decoupling the service layer
response = requests.post(
    "http://localhost:5002/api/recommend", 
    json={"title": title_query, "criteria": criteria}
)
raw_recs = response.json().get("games", [])
```

---

## 🛠️ Built With
*   **Flask** - Web runtime framework and orchestration engine.
*   **Pandas** - Fast and flexible tabular data manipulation structures.
*   **Scikit-Learn** - Machine learning utilities for content filtering vectors.
*   **Bootstrap 5** - Responsive layout presentation engine.

