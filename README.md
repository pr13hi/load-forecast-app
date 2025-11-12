# Load Forecaster

A full-stack web app for hourly electric load forecasting with model explainability and personal prediction history.

---

## Features

- **User Authentication:** Register, login, and secure all endpoints with JWT.  
- **Dashboard:** Run new predictions, see your 20 most recent forecasts, and export results.  
- **Forecasting:** Modern single-point forecast form, leveraging LSTM + Twin SVR, with confidence intervals.  
- **Prediction History:** All predictions are stored for logged-in users in a searchable history table.  
- **Profile Page:** View and (soon) update your profile info; single-click logout.  
- **Responsive UI:** Clean, mobile-ready design with professional branding and logo.  
- **Error Handling:** Friendly messages if not logged in.

---

## Quick Start

### Backend

1. Create a virtualenv and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\activate on Windows
   ```

2. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy and edit `.env` or set environment variables:

   ```
   FLASK_ENV=development
   SECRET_KEY=your_secret
   JWT_SECRET_KEY=your_jwt_secret
   ```

4. Run the Flask app:

   ```bash
   flask run
   ```

### Frontend

1. Navigate to `/frontend` folder.  
2. Run:

   ```bash
   npm install
   npm start
   ```

3. Visit [http://localhost:3000](http://localhost:3000).

---

## Folder Structure

```
/backend
└── app.py, routes/, schemas/, ...

/frontend
└── src/
    pages/
    components/
    utils/
    assets/ (custom logo here)
```

---

## Tech Stack

- **Backend:** Python, Flask, JWT (flask-jwt-extended), SQLAlchemy  
- **Frontend:** ReactJS, React Router, Bootstrap, Fetch API  
- **ML Model:** LSTM + SVR, `joblib` serialization

---

## Attribution & Credits

- Dashboard and UI inspired by analytics dashboards and pro web apps.  
- ML concepts from recent academic load forecasting literature.

---

## License

MIT

---

## Contact

Maintained by [pr13hi](https://github.com/pr13hi).  
Forks and PRs welcome!
