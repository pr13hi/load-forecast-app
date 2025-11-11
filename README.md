# ⚡ Load Forecasting Application  
**LSTM + Twin Support Vector Regression for Hourly Electric Load Forecasting**

## 🧭 Overview  
The **Load Forecasting Application** is a full-stack machine learning system designed for **hourly electric load forecasting**.  
It features an intuitive **React-based frontend** and a secure **Flask-based backend**, allowing users to register, log in, make load predictions, and view their forecast history stored in a PostgreSQL database.  

The backend integrates **deep learning (LSTM)** and **Twin Support Vector Regression (Twin-SVR)** models to produce accurate load predictions, supporting both individual and future batch forecasting capabilities.

---

## ✨ Features  

### 🔧 Backend  
- Modular **Flask API** architecture using blueprints (authentication, prediction, etc.)  
- **JWT-based authentication** with secure registration, login, and logout  
- **Password hashing** and role-based user management  
- **CORS enabled** for local React integration  
- **SQLAlchemy ORM** for database management (PostgreSQL)  
- API endpoints for **health checks** and **status monitoring**  
- Robust **error handling and structured logging**

### 💻 Frontend  
- **React app** with React Router for multi-page navigation  
- Responsive design featuring: **Home, Login, Register, Dashboard, Forecast, Profile**  
- Persistent authentication via **JWT tokens stored in localStorage**  
- Interactive **forecasting form** connected to Flask API  
- Dynamic **dashboard** with navigation and placeholder analytics  
- **React Bootstrap** for professional UI design  

---

## 🧠 Tech Stack  

| Layer | Technologies |
|-------|---------------|
| **Frontend** | React, React Router, React Bootstrap, Chart.js |
| **Backend** | Flask, SQLAlchemy, PostgreSQL |
| **Machine Learning** | TensorFlow/Keras (LSTM), Twin Support Vector Regression |
| **Authentication** | JWT, Werkzeug password hashing |

---

## ⚙️ Installation & Setup  

### 🐍 Backend Setup  

1. **Create and activate a virtual environment:**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables:**  
   ```bash
   export FLASK_ENV=development
   export SECRET_KEY=your_secret_key
   export JWT_SECRET_KEY=your_jwt_secret
   export DATABASE_URL=postgresql://user:password@localhost:5432/loadforecastdb
   ```

4. **Run the Flask app:**  
   ```bash
   python app.py
   ```
   - Backend runs at: **http://localhost:5000**

---

### ⚛️ Frontend Setup  

1. **Navigate to the frontend directory:**  
   ```bash
   cd frontend
   ```

2. **Install dependencies:**  
   ```bash
   npm install
   ```

3. **Run the React app:**  
   ```bash
   npm start
   ```
   - Frontend runs at: **http://localhost:3000**

---

## 📂 Repository Structure  

```
load-forecast-app/
│
├── backend/                    # Flask backend (blueprints, models, routes)
│   ├── auth/                   # Authentication routes and logic
│   ├── prediction/             # Forecast API endpoints
│   ├── models/                 # SQLAlchemy ORM models
│   ├── utils/                  # Helpers and config loaders
│   ├── requirements.txt        # Python dependencies
│   └── ...
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── pages/              # UI pages (Home, Login, Register, etc.)
│   │   ├── components/         # Shared UI components
│   │   └── utils/              # API and auth helpers
│   └── package.json
│
├── app.py                      # Flask entry point
├── config.py                   # Configuration and environment variables
└── README.md                   # Project documentation
```

---

## 🚀 Usage  
Once both servers are running:  
1. Visit **http://localhost:3000**.  
2. Register or log in to your account.  
3. Navigate to the **Forecast** page and input parameters for prediction.  
4. View results and (in future versions) access your prediction history.

---

## 🔮 Future Plans  
- Add **forecast history tracking and export** (CSV/Excel)  
- Support **batch prediction uploads**  
- Implement **advanced analytics and reporting dashboards**  
- Deploy full-stack app to **cloud (AWS/GCP/Render)**  
- Integrate **user profile management and settings**

---

## 🧩 Troubleshooting  
| Issue | Possible Solution |
|-------|--------------------|
| Flask server not starting | Ensure virtual environment is active and `requirements.txt` is installed |
| JWT token errors | Verify correct `JWT_SECRET_KEY` in environment variables |
| CORS issue between frontend & backend | Confirm both run on localhost and Flask CORS is enabled |
| Database connection error | Check PostgreSQL service and correct `DATABASE_URL` |

---

## 👥 Contributors  
- **Prachi Shaw** – Full Stack Developer  
- Open for community contributions!  

---

## 📜 License  
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
