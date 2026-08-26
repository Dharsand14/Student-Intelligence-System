# 🎓 Student Intelligence System v2.2

An enterprise-ready, AI-powered predictive platform designed to monitor and enhance student academic performance in real-time.

---

## 🚀 Key Features
- **🔮 Dual-Mode Prediction**: Individual and Bulk input support.
- **🧠 5-Factor AI Model**: Uses Study Hours, Attendance, Mental Health, Sleep, and Exam Scores for high-precision forecasting.
- **💡 AI Explainability**: Real-time feedback on student performance drivers (Positives vs Concerns).
- **📉 Advanced Analytics Hub**: High-density Plotly visualizations, including Statistical heatmaps and performance distributions.
- **📊 Personal Journey Path**: Performance trend tracking and "Score Trajectory" forecasting for students.
- **📥 Data Persistence**: Secure SQLite logging of all predictions for long-term audit and analysis.
- **📧 Dynamic Communication**: Automated student feedback and reporting systems.
- **🛡️ 3-Tier Security**: Bcrypt hashing, JWT-ready reset tokens, and XSS sanitization for all inputs.

---

## 🛠️ Tech Stack
- **Frontend**: Streamlit (Reactive UI)
- **Backend**: Python (SOA Architecture)
- **AI/ML**: Scikit-Learn (RandomForest / LinearRegression)
- **Database**: SQLite (Relational Persistence)
- **Security**: Bcrypt / PyJWT / XSS Sanitizers
- **Visuals**: Plotly Express / Lottie Animations / Glassmorphism CSS

---

## 🚦 Quick Start
1.  **Environment Setup**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run Application**:
    ```bash
    streamlit run app.py
    ```
3.  **Administrator Access**:
    - Default Staff: `staff@university.edu` / `admin123`
    - Default Student: `testuser1@university.edu` / `Password123!`

---

## 🧪 Quality Assurance
Maintain system integrity by running the master test suite:
```bash
python run_all_tests.py
```

---
*Developed for the Advanced Educational Intelligence Initative | 2026*