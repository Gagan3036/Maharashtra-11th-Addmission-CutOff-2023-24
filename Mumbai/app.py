import streamlit as st
import pandas as pd

# Dictionary to map round numbers to their respective file paths
round_paths = {
    'Round3': 'C:/Users/gagan/Desktop/Maharashtra 11th Addmission CutOff 2023-24/Mumbai/Mumbai_CutOff_Round3.xlsx',
    'Round4': 'C:/Users/gagan/Desktop/Maharashtra 11th Addmission CutOff 2023-24/Mumbai/Mumbai_CutOff_Round4.xlsx',
    'Round5': 'C:/Users/gagan/Desktop/Maharashtra 11th Addmission CutOff 2023-24/Mumbai/Mumbai_CutOff_Round5.xlsx',
    'Round6': 'C:/Users/gagan/Desktop/Maharashtra 11th Addmission CutOff 2023-24/Mumbai/Mumbai_CutOff_Round6.xlsx',
    'Round7': 'C:/Users/gagan/Desktop/Maharashtra 11th Addmission CutOff 2023-24/Mumbai/Mumbai_CutOff_Round7.xlsx',
    'Round8': 'C:/Users/gagan/Desktop/Maharashtra 11th Addmission CutOff 2023-24/Mumbai/Mumbai_CutOff_Round8.xlsx',
    'Round9': 'C:/Users/gagan/Desktop/Maharashtra 11th Addmission CutOff 2023-24/Mumbai/Mumbai_CutOff_Round9.xlsx',
    'Round10': 'C:/Users/gagan/Desktop/Maharashtra 11th Addmission CutOff 2023-24/Mumbai/Mumbai_CutOff_Round10.xlsx'
}

# List of available streams, reservation details, and categories
streams = ['Arts', 'Commerce', 'Science']
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

# Streamlit web app
st.title('Maharashtra HSC 11th Admission Cutoffs 2023-24')

# Sidebar widgets for user inputs
marks = st.number_input('Enter Marks Out Of 500', min_value=0, max_value=500, step=1)
stream_selected = st.selectbox('Select Stream', streams)
round_selected = st.selectbox('Select Round', list(round_paths.keys()))
reservation_selected = st.selectbox('Select Reservation Details', reservations)
category_selected = st.multiselect('Select Categories', categories)

# Function to load data based on user inputs
def load_data(marks, stream, round_selected, reservation_selected, category_selected):
    round_path = round_paths[round_selected]
    df = pd.read_excel(round_path)
    
    # Convert relevant columns to numeric, handling errors gracefully
    for col in category_selected:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Filter the DataFrame based on user inputs
    filtered_df = df[((df[category_selected] <= marks) & df[category_selected].notna()).any(axis=1) & 
                 (df['Stream'] == stream) &
                 (df['Reservation Details'] == reservation_selected)]

    
    # Select unique columns for display
    display_columns = ['CollegeName'] + category_selected + ['Status']
    
    return filtered_df[display_columns]

# Display the filtered results
if st.button('Search'):
    filtered_df = load_data(marks, stream_selected, round_selected, reservation_selected, category_selected)
    
    # Resetting index to add a serial number column
    filtered_df.reset_index(drop=True, inplace=True)
    filtered_df.index += 1  # Adding 1 to start index from 1 for serial number

    # Displaying subheader with appropriate message
    st.subheader(f'{len(filtered_df)} Colleges for {stream_selected} stream with cutoff less than or equal to {marks} in {round_selected}:')
    if filtered_df.empty:
        st.write('No colleges found matching the criteria.')
    else:
        st.dataframe(filtered_df, width=None)  # Displaying dataframe without index column