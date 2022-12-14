import streamlit as st
import random
import pandas as pd
import json
from google.cloud import firestore
from google.oauth2 import service_account



@st.experimental_memo
def get_imps():
    df = pd.read_excel("f_out.xlsx")
    df.set_index('urn',inplace=True)
    imps = df[[x for x in df.columns if 'imp' in x.lower()]]
    imps = imps.melt(ignore_index=False).dropna()
    return imps


@st.experimental_singleton
def fire_db():
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="imps-store")
    return db



imps = get_imps()


if 'imp' not in st.session_state:
    #imps = get_imps()
    ran_imp = random.choice(list(imps.itertuples(index=True)))
    st.session_state['imp'] = ran_imp


def new_imp():
    st.session_state['imp'] = random.choice(list(imps.itertuples(index=True)))



st.title("Ofsted improvements")

st.button("Get new random improvement",on_click = new_imp)

#imps = get_imps()

#ran_imp = imps.sample()#['value'].item()

ran_imp = st.session_state['imp']

st.write(ran_imp.value)

#st.write(f"URN {ran_imp.Index}: {ran_imp.variable}")


with st.form('Classify',clear_on_submit=True):
    imp_type = st.text_input("Enter imp type")
    imp_key_words = st.text_input("Enter key word(s)")

    #test = st.multiselect('testing this',['dsfs','dfdfd','fhgh'])
    submitted = st.form_submit_button("Submit")

    if submitted:
        if imp_type is not None:
            db = fire_db()
            #with open('tags.txt','a+') as f:
            #    f.write(f'{ran_imp.Index};{ran_imp.variable};{imp_type};{imp_key_words}\n')
            db.collection('imps_data').add({'urn':ran_imp.Index,'imp':ran_imp.variable,'type':imp_type,'key_words':imp_key_words})


        new_imp()
        st.experimental_rerun()
        
        #pass # write to db



