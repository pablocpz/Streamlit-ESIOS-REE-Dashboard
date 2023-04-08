# Streamlit-ESIOS-dashboard 
https://neuralroot-streamlit-esios-ree-dashboard-app-6b9hjz.streamlit.app/
-------------------------------------------------------------------------
## **Project Details**

- This web app visualize any indicator from **[ESIOS API](https://www.esios.ree.es/es)**, *(electric **generation** data or **price** data) of Spain*

### **Guide**
- Create a virtual enviromment using `conda create -n streamlit_app`, and then do `conda activate streamlit_app`
- Replace *"${{ secrets.ESIOS_TOKEN }}"* in `credentials.json` with your own ESIOS token, can be owned [here](consultasios@ree.es)
- Pip install -r requirements.txt
- Then, move to the `root folder`, and do **streamlit run app.py**


![image](https://user-images.githubusercontent.com/108333916/230737424-05d5e946-3575-46c7-998f-d89abc5cabe0.png)
