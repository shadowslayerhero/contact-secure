import pandas as pd
import streamlit as st
import plotly_express as px
from sklearn.cluster import DBSCAN
from PIL import Image

# configuration
st.set_option('deprecation.showfileUploaderEncoding', False)

logo = Image.open('cslogocropped.png')
st.image(logo, use_column_width=True)

st.sidebar.title("Directory")
user_guide = st.sidebar.radio("", ("Home", "User Guide", "Contact-Secure"))

if user_guide == 'Home':
    st.markdown('---')
    st.markdown("<h2 style='text-align: center;'>What is Contact-Secure</h2>", unsafe_allow_html=True)
    st.markdown('---')
    st.markdown("<p style='text-align: center;'>Contact-Secure is a prototype contact tracing web application based on an Unsupervised Machine Learning method. This application utilizes the Density-Based Spatial Clustering of Applications with Noise (DBSCAN) algorithm. It can discover clusters of different shapes and sizes from a large amount of data, which is containing noise and outliers and in turn can be used to trace contacts of a person.</p>", unsafe_allow_html=True)
    st.markdown('---')
    
elif user_guide == 'User Guide':
    st.markdown('---')
    st.markdown("<h2 style='text-align: center;'>How to use Contact-Secure</h2>", unsafe_allow_html=True)
    st.markdown('---')
    
    col1, col2 = st.beta_columns(2)
    #image1 = Image.open('htu1.png')
    col1.image('htu4.PNG')
    col2.subheader('Step 1')
    col2.write('From the sidebar, click on Contact-Secure to get started with the application. Using the dropdown menu select a file to explore.')
    st.markdown('---')
    
    col1, col2 = st.beta_columns(2)
    image2 = Image.open('htu3.PNG')
    col2.image(image2)
    col1.subheader('Step 2')
    col1.write('After uploading a file to the application, the dataframe will display. It also comes with filter options as to which column you wish to sort.')
    st.markdown('---')
    
    col1, col2 = st.beta_columns(2)
    image3 = Image.open('htu2.png')
    col1.image(image3)
    col2.subheader('Step 3')
    col2.write('With the dataframe onhand, you can now use the search bar to enter the name of the person of interest and display the names of those who came in contact.')

else:
    st.markdown('---')
    st.sidebar.markdown("---")
    st.sidebar.header("Visualization Settings")

    global df
    st.markdown("<h2 style='text-align: center;'>Select file:</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.beta_columns([1,2.05,1])
    file_uploader = col2.selectbox('', ['Travel_Data_1.csv', 'Travel_Data_2.csv'])
    if file_uploader == 'Travel_Data_1.csv':
            df = pd.read_json('TravelData_1.json')
            col1, col2, col3 = st.beta_columns([1,2.05,1])
            col2.success('Travel_Data_1.csv successfully uploaded!')
    else:
            df = pd.read_json('TravelData_2.json')
            col1, col2, col3 = st.beta_columns([1,2.05,1])
            col2.success('Travel_Data_2.csv successfully uploaded!')
            
    #model
    def get_pui(enter_user):
                        epsilon = 0.0018288 # a radial distance of 6 feet in kilometers
                        model = DBSCAN(eps=epsilon, min_samples=2, metric='haversine').fit(df[['latitude', 'longitude']])
                        df['cluster'] = model.labels_.tolist()
                    
                        enter_user_clusters = []
                        for i in range(len(df)):
                            if df['id'][i] == enter_user:
                                if df['cluster'][i] in enter_user_clusters:
                                    pass
                                else:
                                    enter_user_clusters.append(df['cluster'][i])
                    
                        pos_users = []
                        for cluster in enter_user_clusters:
                            if cluster != -1:
                                ids_in_cluster = df.loc[df['cluster'] == cluster, 'id']
                                for i in range(len(ids_in_cluster)):
                                    user_id = ids_in_cluster.iloc[i]
                                    if (user_id not in pos_users) and (user_id != enter_user):
                                        pos_users.append(user_id)
                                    else:
                                        pass
                        return pos_users
                        
                
    #print names
    def print_infected(get_pui):
                        st.markdown('---')
                        a = st.text_input("Enter person of interest: ", 'Kristian Paule')
                        b = get_pui(a)
                        
                        st.write("Under investigation: ", b)
                        st.markdown('---')
                        """
                        ## Travel History
                        """
    print_infected(get_pui)

    global numeric_columns
    global non_numeric_columns
    try:
            numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
            non_numeric_columns = list(df.select_dtypes(['object']).columns)
            non_numeric_columns.append(None)
            print(non_numeric_columns)
            col1, col2 = st.beta_columns([1, 3])
            selectbox_options = col1.selectbox('Choose filter', ['Default', 
                                                                 'Alphabetically','Timestamp', 
                                                                 'Latitude','Longitude', 
                                                                 'ID and Timestamp'])
            if selectbox_options == 'Default':
                st.write(df.sort_index())
            elif selectbox_options == 'Alphabetically':
                st.write(df.sort_values('id'))
            elif selectbox_options == 'Timestamp':
                st.write(df.sort_values('timestamp'))
            elif selectbox_options == 'Latitude':
                st.write(df.sort_values('latitude'))
            elif selectbox_options == 'Longitude':
                st.write(df.sort_values('longitude'))
            elif selectbox_options == 'ID and Timestamp':
                st.write(df.sort_values(['id', 'timestamp'], kind='mergesort'))   
            st.markdown('---')
    except Exception as e:
            print(e)
            
    #add a select widget to the side bar
    chart_select = st.sidebar.selectbox(
            label="Select the chart type",
            options=['Scatterplots', 'Boxplot']
        )
        
    scatter_options = ['latitude', 'longitude']
    default_ix = scatter_options.index('longitude')
        
    if chart_select == 'Scatterplots':
            st.sidebar.markdown("<h3>Scatterplot Settings</h3>", unsafe_allow_html=True)
            try:
                x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
                y_values = st.sidebar.selectbox('Y axis', options=numeric_columns, index=default_ix)
                color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
                plot = px.scatter( data_frame=df, x=x_values, y=y_values, color=color_value)
                # display the chart
                st.plotly_chart(plot)
            except Exception as e:
                print(e)
        
    if chart_select == 'Boxplot':
            st.sidebar.subheader("Boxplot Settings")
            try:
                y = st.sidebar.selectbox("Y axis", options=numeric_columns)
                x = st.sidebar.selectbox("X axis", options=non_numeric_columns)
                color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
                plot = px.box(data_frame=df, y=y, x=x, color=color_value)
                st.plotly_chart(plot)
            except Exception as e:
                print(e)
