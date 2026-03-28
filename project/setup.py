from setuptools import setup, find_packages

setup(
    name="student_performance_app",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "pandas",
        "scikit-learn",
        "plotly"
    ],
    entry_points={
        "console_scripts": [
            "run-app=app:main"
        ]
    }
)
