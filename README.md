# Streamlit-ESIOS-dashboard 
## **Project Details**

- This web app visualize any indicator from **[ESIOS API](https://www.esios.ree.es/es)**, *(electric **generation** data or **price** data) of Spain*

### **Guide**
- Create a virtual enviromment using `conda create -n streamlit_app`, and then do `conda activate streamlit_app`
- Replace *"${{ secrets.ESIOS_TOKEN }}"* in `credentials.json` with your own ESIOS token, can be owned [here](consultasios@ree.es)
- Pip install -r requirements.txt
- Then, move to the `root folder`, and do **streamlit run app.py**
