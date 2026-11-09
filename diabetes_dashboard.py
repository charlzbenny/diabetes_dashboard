import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Diabetes Analytics Dashboard")
st.header("Healthcare Data Analysis")

try:
    df = pd.read_csv("diabetes_prediction_dataset.csv")
except:
    np.random.seed(42)
    n = 300
    df = pd.DataFrame({
        'gender': np.random.choice(['Female', 'Male'], n),
        'age': np.random.randint(18, 80, n),
        'smoking_history': np.random.choice(['never', 'former', 'current', 'No Info'], n),
        'bmi': np.round(np.random.uniform(18.5, 40.0, n), 2),
        'blood_glucose_level': np.random.randint(80, 250, n),
        'diabetes': np.random.choice([0, 1], n, p=[0.8, 0.2])
    })

st.sidebar.header("Filter Options")

gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["gender"].unique(),
    default=list(df["gender"].unique())
)

smoking = st.sidebar.selectbox(
    "Select Smoking History",
    ["All"] + list(df["smoking_history"].unique())
)

age = st.sidebar.slider("Select Age", 0, 80, (0, 80))

data = df[
    (df["gender"].isin(gender)) &
    (df["age"].between(age[0], age[1]))
]

if smoking != "All":
    data = data[data["smoking_history"] == smoking]

st.subheader("Dashboard Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Records", len(data))
col2.metric("Diabetes Cases", int(data["diabetes"].sum()) if len(data) > 0 else 0)
col3.metric("Average BMI", round(data["bmi"].mean(), 2) if len(data) > 0 else 0)

col4, col5 = st.columns(2)
col4.metric("Average Age", round(data["age"].mean(), 2) if len(data) > 0 else 0)
col5.metric("Average Glucose", round(data["blood_glucose_level"].mean(), 2) if len(data) > 0 else 0)

tab1, tab2, tab3, tab4 = st.tabs(["Dataset", "Analysis", "Graphs", "Insights"])

with tab1:
    st.subheader("Dataset Information")
    st.write("Total Rows:", data.shape[0])
    st.write("Total Columns:", data.shape[1])
    
    st.dataframe(data.head(20))
    
    with st.expander("Statistical Summary"):
        st.write(data.describe())

with tab2:
    st.subheader("Category-wise Analysis")
    category = st.selectbox(
        "Select Category",
        ["gender", "smoking_history", "diabetes"]
    )
    result = data.groupby(category).size()
    st.write(result)

    st.subheader("Numerical Analysis")
    column = st.selectbox(
        "Select Numerical Column",
        ["age", "bmi", "blood_glucose_level"]
    )
    st.write("Sum:", data[column].sum())
    st.write("Average:", data[column].mean())


with tab3:

    # 1. Bar Chart
    st.subheader("Diabetes Cases by Smoking History")

    bar_data = data.groupby("smoking_history")["diabetes"].sum()

    fig, ax = plt.subplots()
    ax.bar(bar_data.index, bar_data.values,
           color=["skyblue", "orange", "lightgreen", "coral", "violet", "gold"])

    ax.set_title("Diabetes Cases by Smoking History")
    ax.set_xlabel("Smoking History")
    ax.set_ylabel("Number of Diabetes Cases")
    ax.tick_params(axis="x", rotation=30)

    st.pyplot(fig)
    plt.close(fig)

    # 2. Line Chart
    st.subheader("Average Blood Glucose at Different Ages")

    line_data = data.groupby("age")["blood_glucose_level"].mean()

    fig, ax = plt.subplots()
    ax.plot(line_data.index, line_data.values,
            color="green", marker="o", linewidth=2)

    ax.set_title("Age vs Average Blood Glucose")
    ax.set_xlabel("Age")
    ax.set_ylabel("Average Blood Glucose Level")
    ax.grid(True, linestyle="--", alpha=0.5)

    st.pyplot(fig)
    plt.close(fig)

    # 3. Scatter Plot
    st.subheader("Relationship Between BMI and Blood Glucose")

    fig, ax = plt.subplots()
    ax.scatter(data["bmi"], data["blood_glucose_level"],
               color="purple", alpha=0.4)

    ax.set_title("BMI vs Blood Glucose Level")
    ax.set_xlabel("BMI")
    ax.set_ylabel("Blood Glucose Level")
    ax.grid(True, linestyle="--", alpha=0.4)

    st.pyplot(fig)
    plt.close(fig)



with tab4:
    st.subheader("Key Insights")

    if len(data) > 0:

        st.write("Total Diabetes Cases:", data["diabetes"].sum())

        st.write("Average BMI:", round(data["bmi"].mean(), 2))

        st.write("Average Age:", round(data["age"].mean(), 2))

        st.write("Average Blood Glucose:",
                 round(data["blood_glucose_level"].mean(), 2))

        st.write("Diabetes Cases by Smoking History:")
        st.write(data.groupby("smoking_history")["diabetes"].sum())

    else:
        st.warning("No data available. Change the filters.")

    st.info("Dashboard created for MCA411-2 Python Lab Exercise 6.")

st.sidebar.write("MCA411-2 Python Programming")