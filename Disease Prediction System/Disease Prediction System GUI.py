from tkinter import *
import numpy as np
import pandas as pd
from PIL import Image, ImageTk

l1=['back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine',
'yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach',
'swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs',
'fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool',
'irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs',
'swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips',
'slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints',
'movement_stiffness','spinning_movements','loss_of_balance','unsteadiness',
'weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine',
'continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain',
'abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum',
'rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion',
'receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen',
'history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf',
'palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling',
'silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose',
'yellow_crust_ooze']

disease=['Fungal infection','Allergy','GERD','Chronic cholestasis','Drug Reaction',
'Peptic ulcer diseae','AIDS','Diabetes','Gastroenteritis','Bronchial Asthma','Hypertension',
' Migraine','Cervical spondylosis',
'Paralysis (brain hemorrhage)','Jaundice','Malaria','Chicken pox','Dengue','Typhoid','hepatitis A',
'Hepatitis B','Hepatitis C','Hepatitis D','Hepatitis E','Alcoholic hepatitis','Tuberculosis',
'Common Cold','Pneumonia','Dimorphic hemmorhoids(piles)',
'Heartattack','Varicoseveins','Hypothyroidism','Hyperthyroidism','Hypoglycemia','Osteoarthristis',
'Arthritis','(vertigo) Paroymsal  Positional Vertigo','Acne','Urinary tract infection','Psoriasis',
'Impetigo']

l2=[]
for x in range(0,len(l1)):
    l2.append(0)

# TESTING DATA 

df=pd.read_csv("Training.csv")

df.replace({'prognosis':{'Fungal infection':0,'Allergy':1,'GERD':2,'Chronic cholestasis':3,'Drug Reaction':4,
'Peptic ulcer diseae':5,'AIDS':6,'Diabetes ':7,'Gastroenteritis':8,'Bronchial Asthma':9,'Hypertension ':10,
'Migraine':11,'Cervical spondylosis':12,
'Paralysis (brain hemorrhage)':13,'Jaundice':14,'Malaria':15,'Chicken pox':16,'Dengue':17,'Typhoid':18,'hepatitis A':19,
'Hepatitis B':20,'Hepatitis C':21,'Hepatitis D':22,'Hepatitis E':23,'Alcoholic hepatitis':24,'Tuberculosis':25,
'Common Cold':26,'Pneumonia':27,'Dimorphic hemmorhoids(piles)':28,'Heart attack':29,'Varicose veins':30,'Hypothyroidism':31,
'Hyperthyroidism':32,'Hypoglycemia':33,'Osteoarthristis':34,'Arthritis':35,
'(vertigo) Paroymsal  Positional Vertigo':36,'Acne':37,'Urinary tract infection':38,'Psoriasis':39,
'Impetigo':40}},inplace=True)

X= df[l1]

y = df[["prognosis"]]
np.ravel(y)


# TRAINING DATA 
tr=pd.read_csv("Testing.csv")
tr.replace({'prognosis':{'Fungal infection':0,'Allergy':1,'GERD':2,'Chronic cholestasis':3,'Drug Reaction':4,
'Peptic ulcer diseae':5,'AIDS':6,'Diabetes ':7,'Gastroenteritis':8,'Bronchial Asthma':9,'Hypertension ':10,
'Migraine':11,'Cervical spondylosis':12,
'Paralysis (brain hemorrhage)':13,'Jaundice':14,'Malaria':15,'Chicken pox':16,'Dengue':17,'Typhoid':18,'hepatitis A':19,
'Hepatitis B':20,'Hepatitis C':21,'Hepatitis D':22,'Hepatitis E':23,'Alcoholic hepatitis':24,'Tuberculosis':25,
'Common Cold':26,'Pneumonia':27,'Dimorphic hemmorhoids(piles)':28,'Heart attack':29,'Varicose veins':30,'Hypothyroidism':31,
'Hyperthyroidism':32,'Hypoglycemia':33,'Osteoarthristis':34,'Arthritis':35,
'(vertigo) Paroymsal  Positional Vertigo':36,'Acne':37,'Urinary tract infection':38,'Psoriasis':39,
'Impetigo':40}},inplace=True)

X_test= tr[l1]
y_test = tr[["prognosis"]]
np.ravel(y_test)

# Data Modelling

def DecisionTree():

    from sklearn import tree

    clf3 = tree.DecisionTreeClassifier()  
    clf3 = clf3.fit(X,y)

    # calculating accuracy
    from sklearn.metrics import accuracy_score
    y_pred=clf3.predict(X_test)
    print(accuracy_score(y_test, y_pred))
    print(accuracy_score(y_test, y_pred,normalize=False))

    psymptoms = [Symptom1.get(),Symptom2.get(),Symptom3.get(),Symptom4.get(),Symptom5.get()]

    for k in range(0,len(l1)):
        # print (k,)
        for z in psymptoms:
            if(z==l1[k]):
                l2[k]=1

    inputtest = [l2]
    predict = clf3.predict(inputtest)
    predicted=predict[0]

    h='no'
    for a in range(0,len(disease)):
        if(predicted == a):
            h='yes'
            break


    if (h=='yes'):
        t1.delete("1.0", END)
        t1.insert(END, disease[a])
    else:
        t1.delete("1.0", END)
        t1.insert(END, "Not Found")


def randomforest():
    from sklearn.ensemble import RandomForestClassifier
    clf4 = RandomForestClassifier()
    clf4 = clf4.fit(X,np.ravel(y))

    # calculating accuracy
    from sklearn.metrics import accuracy_score
    y_pred=clf4.predict(X_test)
    print(accuracy_score(y_test, y_pred))
    print(accuracy_score(y_test, y_pred,normalize=False))

    psymptoms = [Symptom1.get(),Symptom2.get(),Symptom3.get(),Symptom4.get(),Symptom5.get()]

    for k in range(0,len(l1)):
        for z in psymptoms:
            if(z==l1[k]):
                l2[k]=1

    inputtest = [l2]
    predict = clf4.predict(inputtest)
    predicted=predict[0]

    h='no'
    for a in range(0,len(disease)):
        if(predicted == a):
            h='yes'
            break

    if (h=='yes'):
        t2.delete("1.0", END)
        t2.insert(END, disease[a])
    else:
        t2.delete("1.0", END)
        t2.insert(END, "Not Found")


# GUI------------------------------------------------------------------------------------
import tkinter as tk
from tkinter import StringVar, Label, Entry, OptionMenu, Text, Button, CENTER, END
from PIL import Image, ImageTk

root = tk.Tk()
root.state('zoomed')  # Maximize the window

# Load background image
bg_image = Image.open("background.jpg")  
bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label to hold the background image
bg_label = Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Create a frame to hold all the widgets
frame = tk.Frame(root, bg='#282c34')
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Entry variables
Symptom1 = StringVar()
Symptom1.set(None)
Symptom2 = StringVar()
Symptom2.set(None)
Symptom3 = StringVar()
Symptom3.set(None)
Symptom4 = StringVar()
Symptom4.set(None)
Symptom5 = StringVar()
Symptom5.set(None)
Name = StringVar()

# Heading
w2 = Label(frame, justify=CENTER, text="Disease Predictor System", fg="#ffffff", bg="#282c34")
w2.config(font=("Cascadia Code", 30))
w2.grid(row=0, column=0, columnspan=3, pady=(0, 10))
w3 = Label(frame, justify=CENTER, text="Using Machine Learning", fg="#ffffff", bg="#282c34")
w3.config(font=("Cascadia Code", 20))
w3.grid(row=1, column=0, columnspan=3, pady=(0, 30))

# Labels
NameLb = Label(frame, text="Name of the Patient", fg="#71C671", bg="#282c34")
NameLb.grid(row=2, column=0, pady=15, sticky="e")

S1Lb = Label(frame, text="Symptom 1", fg="#71C671", bg="#282c34")
S1Lb.grid(row=3, column=0, pady=10, sticky="e")

S2Lb = Label(frame, text="Symptom 2", fg="#71C671", bg="#282c34")
S2Lb.grid(row=4, column=0, pady=10, sticky="e")

S3Lb = Label(frame, text="Symptom 3", fg="#71C671", bg="#282c34")
S3Lb.grid(row=5, column=0, pady=10, sticky="e")

S4Lb = Label(frame, text="Symptom 4", fg="#71C671", bg="#282c34")
S4Lb.grid(row=6, column=0, pady=10, sticky="e")

S5Lb = Label(frame, text="Symptom 5", fg="#71C671", bg="#282c34")
S5Lb.grid(row=7, column=0, pady=10, sticky="e")

lrLb = Label(frame, text="Decision Tree", fg="cyan", bg="#282c34")
lrLb.grid(row=8, column=0, pady=10, sticky="e")

destreeLb = Label(frame, text="Random Forest", fg="cyan", bg="#282c34")
destreeLb.grid(row=9, column=0, pady=10, sticky="e")

# Entries
OPTIONS = sorted(l1)
NameEn = Entry(frame, textvariable=Name)
NameEn.grid(row=2, column=1)

S1En = OptionMenu(frame, Symptom1, *OPTIONS)
S1En.grid(row=3, column=1)

S2En = OptionMenu(frame, Symptom2, *OPTIONS)
S2En.grid(row=4, column=1)

S3En = OptionMenu(frame, Symptom3, *OPTIONS)
S3En.grid(row=5, column=1)

S4En = OptionMenu(frame, Symptom4, *OPTIONS)
S4En.grid(row=6, column=1)

S5En = OptionMenu(frame, Symptom5, *OPTIONS)
S5En.grid(row=7, column=1)

# Buttons
dst = Button(frame, text="DecisionTree", command= DecisionTree, bg="#4b5263", fg="#FFA756")  
dst.grid(row=3, column=2, padx=10)

rnf = Button(frame, text="Randomforest", command= randomforest, bg="#4b5263", fg="#FFA756")  
rnf.grid(row=4, column=2, padx=10)


# Text fields
t1 = Text(frame, height=1, width=40, bg="#4b5263", fg="#CCCCCC")
t1.grid(row=8, column=1, padx=10)

t2 = Text(frame, height=1, width=40, bg="#4b5263", fg="#CCCCCC")
t2.grid(row=9, column=1, padx=10)

root.mainloop()