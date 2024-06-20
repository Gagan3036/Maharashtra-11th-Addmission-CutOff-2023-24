import streamlit as st
import pandas as pd
import io
import os

# List of available streams, reservation details, categories, statuses, college types, and mediums
streams = ['Arts', 'Commerce', 'Science', 'HSVC - Accounting and Office Management', 'HSVC - Electronics Technology',
           'HSVC - Medical Lab Technician', 'HSVC - Electrical Technology', 'HSVC - Banking Financial Services and Insurance',
           'HSVC - Computer Technology', 'HSVC - Construction Technology', 'HSVC - Marketing and Retails Management',
           'HSVC - Mechanical Technology', 'HSVC - Automobile Technology', 'HSVC - Tourism Hospitality Management',
           'HSVC - Logistic and Supply Chain Management', 'HSVC - Child, Old age And Health Card Services',
           'HSVC - Catering and Food Product Technology', 'HSVC - Radiology Technician', 'HSVC - Fisheries Technology']
reservations = [
    'Pure',
    'Trf. / Ex.Sr. / Ser/SPORTS (5%)',
    'PH (4%)',
    'Project / Earthquake affected (5%)',
    'Orphan (1%)',
    'Women (30%)',
    'Technical (For Bifocal & HCVC Only) (25%)'
]
categories = ['SC', 'ST', 'VJ-A', 'NT-B', 'NT-C', 'NT-D', 'OBC', 'SBC', 'EWS', 'General']
statuses = ['All', 'Self Finance', 'Aided', 'Un-Aided', 'Partially Aided (20%-80%)', 'Government', 'B.M.C.']
college_types = ['Co-Ed', 'Girls', 'Boys']
mediums = ['English', 'Marathi', 'Urdu', 'Hindi', 'Gujarati']
citys = ['Mumbai', 'Pune', 'Nashik', 'Nagpur', 'Amravati']

# Streamlit web app
st.title('Maharashtra 11th Admission Cutoff Search 2024')

# Custom CSS for modern, clean design
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #4CAF50, #2196F3);
        font-family: 'Roboto', sans-serif;
        color: #4CAF50;
    }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp p, .stApp div, .stApp span, .stApp a, .stApp label {
        color: #FFF6E9;
    }
    .stApp .css-1d391kg {  /* stButton */
        background-color: #2196F3;
        color: #FFFFFF;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
    }
    .stApp .css-1d391kg:hover {  /* stButton hover */
        background-color: #4CAF50;
    }
    .stApp .css-10trblm {  /* stNumberInput */
        background-color: linear-gradient(135deg, #4CAF50, #2196F3);
        color: #000000;
        border-radius: 5px;
    }
    .stApp .css-16idsys {  /* stSelectbox, stMultiselect */
        background-color: #FFFFFF;
        color: #000000;
        border-radius: 5px;
    }
    .stApp .css-15tx938 {  /* stMarkdown */
        padding: 20px;
        margin: 20px 0;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.2);
    }
    .stApp .css-vk3wp9 {  /* stSubheader */
        margin-top: 20px;
    }
    .stApp .css-1qgla7p {  /* stDataFrame */
        background-color: #FFFFFF;
        color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar widgets for user inputs
city_selected = st.selectbox('Select City', citys, index=0)  # Set index=0 for no default selection
marks = st.number_input('Enter Marks Out Of 500', min_value=0, max_value=500, step=1)
stream_selected = st.selectbox('Select Stream', streams)
# Assign city
city = f'{city_selected}'

# Dictionary to map round numbers to their respective file paths
def round_path(a, city):
    return f'{city}/{city}_CutOff_Round{a}.xlsx'

round_paths = {
    'Regular Round 3': round_path(3, city),
    'Special Round 1': round_path(4, city),
    'Special Round 2': round_path(5, city),
    'Special Round 3': round_path(6, city),
    'Special Round 4': round_path(7, city),
    'Special Round 5': round_path(8, city),
    'Special Round 6': round_path(9, city),
    'Special Round 7': round_path(10, city)
}

round_selected = st.selectbox('Select Round', list(round_paths.keys()))
reservation_selected = st.selectbox('Select Reservation Details', reservations)
category_selected = st.multiselect('Select Categories', categories)
status_selected = st.selectbox('Select Status', statuses)
college_type_selected = st.selectbox('Select College Type', college_types)
medium_selected = st.selectbox('Select Medium', mediums)


# Function to load data based on user inputs
def load_data(marks, stream, round_selected, reservation_selected, category_selected, status_selected, college_type_selected, medium_selected):
    round_path = round_paths[round_selected]
    st.write(f"Loading data from: {round_path}")  # Debug: Print the file path being loaded
    df = pd.read_excel(round_path)
    
    # Convert relevant columns to numeric, handling errors gracefully
    for col in category_selected:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Filter the DataFrame based on user inputs
    if status_selected == 'All':
        filtered_df = df[
            ((df[category_selected] <= marks) & df[category_selected].notna()).any(axis=1) & 
            (df['Stream'] == stream) &
            (df['Reservation Details'] == reservation_selected) &
            (df['CollegeType'] == college_type_selected) &
            (df['Medium'] == medium_selected)
        ]
    else:
        filtered_df = df[
            ((df[category_selected] <= marks) & df[category_selected].notna()).any(axis=1) & 
            (df['Stream'] == stream) &
            (df['Reservation Details'] == reservation_selected) &
            (df['Status'] == status_selected) &
            (df['CollegeType'] == college_type_selected) &
            (df['Medium'] == medium_selected)
        ]

    # Select unique columns for display
    display_columns = ['CollegeName'] + category_selected + ['Status', 'CollegeType', 'Medium']
    
    return filtered_df[display_columns]

# Display the filtered results
if st.button('Search'):
    filtered_df = load_data(marks, stream_selected, round_selected, reservation_selected, category_selected, status_selected, college_type_selected, medium_selected)
    
    # Resetting index to add a serial number column
    filtered_df.reset_index(drop=True, inplace=True)
    filtered_df.index += 1  # Adding 1 to start index from 1 for serial number

    # Displaying subheader with appropriate message
    st.subheader(f'{len(filtered_df)} Colleges in {city_selected} for {stream_selected} stream with cutoff less than or equal to {marks} in {round_selected}:')
    if filtered_df.empty:
        st.write('No colleges found matching the criteria.')
    else:
        st.dataframe(filtered_df, width=None)  # Displaying dataframe without index column

        # Create a downloadable Excel file
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            filtered_df.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)
        
        # Provide download button
        st.download_button(
            label="Download data as Excel",
            data=output,
            file_name=f'{stream_selected}_stream_cutoffs.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

# Developer Contact Information
st.markdown("***")
st.markdown("### Developer Contact Details")
st.markdown("#### Gagan Prajapati")

if st.button('Email'):
    st.markdown('**Email:** [gaganprajapati899@gmail.com](mailto:gaganprajapati899@gmail.com)')
if st.button('LinkedIn'):
    st.markdown('[Gagan Prajapati on LinkedIn](https://www.linkedin.com/in/gagan-prajapati-333791218/)')
if st.button('Twitter'):
    st.markdown('[Gagan Prajapati on Twitter](https://twitter.com/Gagan3036)')
if st.button('GitHub'):
    st.markdown('[Gagan Prajapati on GitHub](https://github.com/Gagan3036)')
