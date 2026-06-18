# EcoForecast Dashboard 🌍📈

An interactive forecasting tool designed to explore the relationship between economic growth (GDP) and $CO_2$ emissions across 12 key countries through 2030. This dashboard visualizes scenario projections, tracks decoupling trends, and highlights the high-leverage policy areas needed to accelerate the green energy transition.

👉 **https://ecoforecast-dashboard-jjuzaqkldagmt55d2ggy7x.streamlit.app/**

---

## 🎯 Core Features

### 🔮 1. Forecast Tab (Scenario Planning)
Visualize the future trajectory of emissions based on customizable inputs. 
* **Interactive Controls:** Filter by specific countries and climate scenarios.
* **Projections:** Solid lines track historical data, while dotted lines map out **Low**, **Baseline**, and **High** projections.
* **Uncertainty Tracking:** A shaded green band clearly represents the statistical uncertainty range of the forecasts.

### 🔄 2. Decoupling Tab (Economy vs. Climate)
Track whether economic growth is breaking away from environmental degradation.
* **The Decoupling Gap:** Bar lengths illustrate the exact variance between GDP growth rates and $CO_2$ growth rates.
* **Visual Indicators:** 
  * 🟢 **Green Bar:** Indicates active *decoupling* (GDP growing while emissions drop or slow down).
  * 🔴 **Red Bar:** Indicates a *carbon-locked* economy (emissions rising tightly alongside economic growth).

### 🏆 3. League Table (Global Rankings)
A comprehensive macro-view ranking all 12 tracked countries. 
* Compare countries side-by-side based on their **projected 2030 emissions**.
* Track growth percentages and instantly identify the decoupling status of each nation.

### ⚡ 4. Driver Attribution (Policy Insights)
 Pinpoint exactly what forces are driving each country's emissions profile.
* **Key Finding:** Energy is the dominant emissions driver for **11 out of the 12 countries** analyzed. 
* **Policy Takeaway:** This data confirms that the energy transition remains the absolute highest-leverage climate policy action available to governments.

---

## 🛠️ Tech Stack & Libraries

* **Language:** Python
* **Framework:** Streamlit
* **Data Visualization:** Matplot, Plotly
* **Forecasting Models:** Bayesian Ridge

---

## 🚀 Quick Start

### Prerequisites
Ensure you have `Python 3.10 or above` installed.

### Installation Steps 
1. Clone repositoy 
```bash
   git clone https://github.com/vinodsithamparam/ecoforecast-dashboard.git
```
2. Create a virtual environment and install required packages  
```bash
   cd ecoforecast-dashboard
   python3 -m venv .ecoforecast-dashboard
   source .ecoforecast-dashboard/bin/activate
   pip install -r requirements.txt
```
3. Launch the streamlit application
```bash
   streamlit run app.py
```
4. Interact with the streamlit application on your local browser 

## Demo Video 

https://github.com/user-attachments/assets/3415e8e5-32ab-4a3d-85ea-559387882088




