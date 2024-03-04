import streamlit as st
import pandas as pd
import pickle
import streamlit as st
import pickle
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import streamlit as st
import pandas as pd
import streamlit as st
import pandas as pd
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import pickle
import time
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
import hashlib

# Security
#passlib,hashlib,bcrypt,scrypt

def make_hashes(password):
        return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
        if make_hashes(password) == hashed_text:
                return hashed_text
        return False

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
        c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
        c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
        conn.commit()

def login_user(username,password):
        c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
        data = c.fetchall()
        return data


def view_all_users():
        c.execute('SELECT * FROM userstable')
        data = c.fetchall()
        return data

model_filename = 'model.pkl'

with open(model_filename, 'rb') as file:
    model = pickle.load(file)

def str2():
    age = st.slider('Age', 18, 100, 50)
    sex_options = ['Male', 'Female']
    sex = st.selectbox('Sex', sex_options)
    sex_num = 1 if sex == 'Male' else 0 
    cp_options = ['Typical Angina', 'Atypical Angina', 'Non-anginal Pain', 'Asymptomatic']
    cp = st.selectbox('Chest Pain Type', cp_options)
    cp_num = cp_options.index(cp)
    trestbps = st.slider('Resting Blood Pressure', 90, 200, 120)
    chol = st.slider('Cholesterol', 100, 600, 250)
    fbs_options = ['False', 'True']
    fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl', fbs_options)
    fbs_num = fbs_options.index(fbs)
    restecg_options = ['Normal', 'ST-T Abnormality', 'Left Ventricular Hypertrophy']
    restecg = st.selectbox('Resting Electrocardiographic Results', restecg_options)
    restecg_num = restecg_options.index(restecg)
    thalach = st.slider('Maximum Heart Rate Achieved', 70, 220, 150)
    exang_options = ['No', 'Yes']
    exang = st.selectbox('Exercise Induced Angina', exang_options)
    exang_num = exang_options.index(exang)
    oldpeak = st.slider('ST Depression Induced by Exercise Relative to Rest', 0.0, 6.2, 1.0)
    slope_options = ['Upsloping', 'Flat', 'Downsloping']
    slope = st.selectbox('Slope of the Peak Exercise ST Segment', slope_options)
    slope_num = slope_options.index(slope)
    ca = st.slider('Number of Major Vessels Colored by Fluoroscopy', 0, 4, 1)
    thal_options = ['Normal', 'Fixed Defect', 'Reversible Defect']
    thal = st.selectbox('Thalassemia', thal_options)
    thal_num = thal_options.index(thal)



    if st.button('Predict'):
        user_input = pd.DataFrame(data={
            'age': [age],
            'sex': [sex_num],  
            'cp': [cp_num],
            'trestbps': [trestbps],
            'chol': [chol],
            'fbs': [fbs_num],
            'restecg': [restecg_num],
            'thalach': [thalach],
            'exang': [exang_num],
            'oldpeak': [oldpeak],
            'slope': [slope_num],
            'ca': [ca],
            'thal': [thal_num]
        })
        prediction = model.predict(user_input)
        prediction_proba = model.predict_proba(user_input)

        if prediction[0] == 1:
            bg_color = 'red'
            prediction_result = 'Positive'
        else:
            bg_color = 'green'
            prediction_result = 'Negative'
        
        confidence = prediction_proba[0][1] if prediction[0] == 1 else prediction_proba[0][0]

        st.markdown(f"<p style='background-color:{bg_color}; color:white; padding:10px;'>Prediction: {prediction_result}<br>Confidence: {((confidence*10000)//1)/100}%</p>", unsafe_allow_html=True)

def main():

        st.markdown("<h1 style='text-align: center; color: green;'>Heart Disease Prediction</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: green;'>Empowering Health Through Predictive Insights</h4>", unsafe_allow_html=True)

        menu = ["HOME","ADMIN LOGIN","USER LOGIN","SIGN UP"]
        choice = st.sidebar.selectbox("Menu",menu)

        if choice == "HOME":
                st.markdown("<h1 style='text-align: center;'>HOMEPAGE</h1>", unsafe_allow_html=True)
                image = Image.open(r"image.png")
                st.image(image, caption='',use_column_width=True)
                st.subheader(" ")
                st.write("     <p style='text-align: center;'> Our 'Heart Disease Prediction' application harnesses the power of machine learning to provide predictive insights into cardiovascular health. By analyzing key indicators and risk factors, our tool offers personalized assessments to help individuals understand and mitigate their risk of heart disease. Whether you're proactively managing your health or seeking early detection, our application equips you with the knowledge to make informed decisions and prioritize your well-being. Empower yourself with actionable insights and take control of your cardiovascular health journey today.", unsafe_allow_html=True)
                time.sleep(3)
                st.warning("Goto Menu Section To Login !")

        elif choice == "ADMIN LOGIN":
                 st.markdown("<h1 style='text-align: center;'>Admin Login Section</h1>", unsafe_allow_html=True)
                 user = st.sidebar.text_input('Username')
                 passwd = st.sidebar.text_input('Password',type='password')
                 if st.sidebar.checkbox("LOGIN"):

                         if user == "Admin" and passwd == 'admin123':

                                                st.success("Logged In as {}".format(user))
                                                task = st.selectbox("Task",["Home","Profiles"])
                                                if task == "Profiles":
                                                        st.subheader("User Profiles")
                                                        user_result = view_all_users()
                                                        clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                                                        st.dataframe(clean_db)
                                                str2()
                                                
                         else:
                                st.warning("Incorrect Admin Username/Password")
          
        elif choice == "USER LOGIN":
                st.markdown("<h1 style='text-align: center;'>User Login Section</h1>", unsafe_allow_html=True)
                username = st.sidebar.text_input("User Name")
                password = st.sidebar.text_input("Password",type='password')
                if st.sidebar.checkbox("LOGIN"):
                        # if password == '12345':
                        create_usertable()
                        hashed_pswd = make_hashes(password)

                        result = login_user(username,check_hashes(password,hashed_pswd))
                        if result:

                                st.success("Logged In as {}".format(username))
                                str2()
                                         
                        else:
                                st.warning("Incorrect Username/Password")
                                st.warning("Please Create an Account if not Created")

        elif choice == "SIGN UP":
                st.subheader("Create New Account")
                new_user = st.text_input("Username")
                new_password = st.text_input("Password",type='password')

                if st.button("SIGN UP"):
                        create_usertable()
                        add_userdata(new_user,make_hashes(new_password))
                        st.success("You have successfully created a valid Account")
                        st.info("Go to User Login Menu to login")

if __name__ == '__main__':
        main()
