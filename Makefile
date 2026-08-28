setup:
	python -m pip install -r requirements.txt

pipeline:
	python load_data.py
	python analysis.py
	python statistical_analysis.py
	python subset_analysis.py

dashboard:
	python -m streamlit run dashboard.py