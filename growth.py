import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="📀 Data Sweeper", layout='wide')

#Custom css
st.markdown(
    """
    <style>
   .stApp{
   background-color: black:
   color: white;
   
   }
   </style>
""",
unsafe_allow_html=True
)

#Title  and description
st.title("📀 Data Sweeper Sterling Integrator By Noor Anum")

st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization creating the project for quarter 3!")

#file uploader
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):",type=["CVS", "XLSX"], accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file format. Please upload either CSV or Excel files: {file_ext}")
            continue

         #Display file size / Name
        st.write(f"**File Name:** {file.name}")
        st.write(f"**📦 File size:** {file.size} bytes")

        #File details
        st.write("🔍 Preview the head of the dataframe")
        st.dataframe(df.head())

        #Data cleaning
        st.subheader("🗑🧹🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            coll, col2 = st.columns(2)

            with coll:
                if st.button(f"Remove duplicates from the file: {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed")
             

                with col2:
                    if st.button(f"Remove missing values from the file: {file.name}"):
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("✅ Missing values have been filled!")
     
            st.subheader("🎯  Select Columns to keep")
            columns = st.multiselect("Choose columns for {file.name}", df.columns, default=df.columns)

            #data visualization
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"Show visualization for {file.name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

                #Conversion Options
                st.subheader("🔄 Conversion Options")
                conversion_type = st.radio(f"Convert {file.name} to:", ['CSV', 'Excel'], key=file.name)
                if st.button(f"Convert{file.name}"):
                    buffer = BytesIO()
                    if conversion_type == 'CSV':
                        df.to_csv(buffer, index=False)
                   
                        file_name = file.name.replace(file_ext, "csv")
                        mime_type = "text/csv" 
                       
                    elif conversion_type == "Excel":
                        df.to_excel(buffer, index=False)
                        file_name = file.name.replace(file_ext, "xlsx")
                        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    buffer.seek(0)
                    st.download_button(
                        label=f"📥Click here to download {file_name} as {conversion_type}",
                        data=buffer,
                        file_name=file_name,
                        mime=mime_type,
                    )
                           
st.success("🎉🥳 All files Processed successfully!")           
                