# Option Pricing Simulator

An interactive web application and REST API for pricing European options using:

- 📈 Black-Scholes Model
- 🎲 Monte Carlo Simulation
- 🌲 Binomial Tree Model

## Live Web App
Deployed on Google Cloud using Docker and Streamlit (see `app.yaml`).

## Features
- Real-time price data from Yahoo Finance
- Caching via `requests-cache`
- Interactive Streamlit UI
- REST API with FastAPI

## Project Structure
```
option-pricing-simulator/
├── option_pricing/          # Model implementations
├── demo/                    # GIFs/screenshots
├── streamlit_app.py         # Streamlit web interface
├── api.py                   # FastAPI REST backend
├── option_pricing_test.py   # CLI tests
├── Dockerfile               # Docker config
├── app.yaml                 # GCP deployment config
├── Requirements.txt         # Dependencies
└── README.md                # Project overview
```

## REST API Example
`GET /price?model=black-scholes&S=100&K=100&T=1&r=0.05&sigma=0.2&option_type=call`

## Docker Deployment
```bash
docker build -t option-pricing .
docker run -p 8080:8080 option-pricing
```

## GCP Deployment
```bash
gcloud app deploy
```
