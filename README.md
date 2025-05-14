# RegNes Dashboard

**RegNes Dashboard** visualizes previous work by [Tom Broekel](https://regnes.shinyapps.io/Regnes/), reimagined with a modern tech stack and interactive design. The dashboard provides a visual interface to explore regional sentiment, happiness, and valence data.

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm 9+
- Virtual environment (`venv` or Conda)

---

## Backend Setup

```bash
cd backend
python -m venv env
source env/bin/activate  # or use `env\Scripts\activate` on Windows
pip install -r requirements.txt
mkdir instance
flask db upgrade
flask ingest-data app/raw/data
flask run
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```
## Environment variables

```bash
cp .env.example .env
```

## Future work

The project was not the main part about the thesis and misses a lot of tests. Fetching data in real time has not been added, because we are changing from RSS feed to Commoncrawl to gether news. Heatmap feature was changed last minute from globe to geographical view to satisfy the product owner