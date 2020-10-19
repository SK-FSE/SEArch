# SEArch
This is a place of FSE project

To run:
1. `export FLASK_APP=app.py`
2. `python3 db/db.py`
3. `flask run`
4. go to `http://127.0.0.1:5000/` in browser

---

Some notes about demo.ipynb
In the notebook we:
1. load all necessary files
(if models were trained, go to the 4-th step)
2. train&save N models for searching through text in N papers (if models were)
3. train&save model for searching relevant articles
4. load model from the 3-rd step
5. create queries using model.dataset_search or model.paper_search methods