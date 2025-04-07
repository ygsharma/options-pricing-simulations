# Option Pricing Simulator

An interactive web application for pricing European options using:

- Black-Scholes Model
- Monte Carlo Simulation
- Binomial Tree Model

## Project Structure
```
option-pricing-simulator/
├── option_pricing/          # Model implementations
├── streamlit_app.py         # Streamlit web interface
├── api.py                   # FastAPI REST backend(To be implemented)
├── option_pricing_test.py   # CLI tests
├── Dockerfile               # Docker config
├── Requirements.txt         # Dependencies
└── README.md                # Project overview
```

## How to Run

```bash
pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

## Docker Deployment
```bash
docker build -t option-pricing .
docker run -p 8080:8080 option-pricing
```