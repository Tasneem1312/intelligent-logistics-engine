# 🚚 Intelligent Logistics Engine: Supply Chain Optimization

An enterprise-grade routing optimization engine built to solve the **Capacitated Vehicle Routing Problem (CVRP)**. This system simulates localized delivery nodes, calculates real-world geospatial distances, and utilizes Constraint Programming to generate the most efficient delivery routes, minimizing total distance driven while adhering to vehicle weight capacities.

## ⚙️ Key Features
* **Geospatial Distance Matrix:** Calculates highly accurate great-circle distances between all delivery nodes using the Haversine formula.
* **Algorithmic Routing:** Leverages Google OR-Tools to solve NP-hard combinatorial optimization problems in seconds.
* **Constraint Management:** Prevents vehicle overloading by actively tracking cumulative payload weight against strict capacity limits.
* **Interactive Dashboard:** A Streamlit-powered frontend featuring live KPI tracking (Distance, Fleet Utilization, Payload) and dynamic map rendering via Folium.

## 🛠️ Technology Stack
* **Language:** Python 3.x
* **Optimization Engine:** Google OR-Tools
* **Data Engineering:** Pandas, NumPy
* **Frontend & Visualization:** Streamlit, Folium, Streamlit-Folium

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/tasneem/intelligent-logistics-engine.git](https://github.com/tasneem/intelligent-logistics-engine.git)
   cd intelligent-logistics-engine

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt

4. **Launch the application:**

    ```bash
    streamlit run app.py

**📁 Project Structure**

intelligent-logistics-engine/

├── data/                   # (Optional) Static datasets

├── src/                    # Core engine modules

│   ├── data_generator.py   # Synthetic node generation 

│   ├── distance_calc.py    # Haversine matrix mathematics

│   └── optimizer.py        # OR-Tools CVRP solver logic

├── app.py                  # Streamlit dashboard and UI

├── requirements.txt        # Environment dependencies

└── README.md               # Project documentation

<img width="1891" height="847" alt="image" src="https://github.com/user-attachments/assets/7855a054-0301-4a67-884b-b47a112b40db" />
