from PIL import Image
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import streamlit.components.v1 as components

def display_vessel_info(group_data):
    st.subheader("Vessel Information")
    col1, col2, col3, col4 = st.columns(4)
    col1.info(f"**Vessel Name:** {group_data['name'].iloc[0]}")
    col2.info(f"**Vessel Type:** {group_data['type_specific'].iloc[0]}")
    col3.info(f"**Avg Vessel Speed:** {round(group_data['speed'].mean(), 2)} m/s")
    
    col4.info(f"**Avg Wind Pressure:** {round(group_data['main.pressure'].mean(), 2)} hPa")
    col5, col6, col7, col8 = st.columns(4)
    col5.info(f"**Avg Wind Speed:** {round(group_data['wind.speed'].mean(), 2)} m/s")
    col6.info(f"**Vessel IMOs:** {group_data['imo'].iloc[0]}")
    
    col7.info(f"**Vessel MMSIs:** {group_data['mmsi'].iloc[0]}")
    col8.info(f"**Country Code:** {group_9454462_r1['country_iso'].iloc[0]}")
    
    col9, col10 = st.columns(2)
    col9.info(f"**Departure:** {group_data['departure'].iloc[0]}")
    col10.info(f"**Arrival:** {group_data['destination'].iloc[0]}")
    
def display_html_map(file_path, height=700):
    with open(file_path, 'r') as f:
        html_data = f.read()

    st.subheader("Vessel Locator Map")
    components.html(html_data, height=height)
    
def plot_speed_histogram(plot1):
    speed_fig = px.histogram(plot1, x="speed")
    speed_fig.update_layout(
        bargap=0.2,
        width=900,
        height=400,
        title='Speed Distribution',
        title_x=0.3,
        title_font=dict(size=24)
    )
    speed_fig.update_traces(marker=dict(color='skyblue'))
    st.plotly_chart(speed_fig, theme="streamlit")

def plot_speed_wind_speed(plot2):
    speed_time = plt.figure(figsize=(9, 4))
    
    sns.lineplot(data=plot2[['speed', 'wind.speed']])
    plt.xlabel('Time', color='white')
    plt.ylabel('Speed (m/s)', color='white')

    # Change legend text color
    plt.legend(['Vessel Speed', 'Wind Speed'])
    leg = plt.gca().get_legend()
    text_color = 'white'
    for text in leg.get_texts():
        plt.setp(text, color=text_color)

    # Change ticks color
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')
    plt.title('                                                             Vessel Speed vs Wind Speed', color='white', fontsize=24, loc='center')
    st.plotly_chart(speed_time, theme="streamlit")

def plot_kpi(plot3):
    kpi_chart = plt.figure(figsize=(9, 4))

    # Assuming group_9454462_r1 is your DataFrame
    sns.lineplot(data=plot3[['main.temp', 'main.humidity', "main.pressure"]])
    plt.xlabel('Time', color='white')
    plt.ylabel('Value', color='white')

    # Change legend text color
    plt.legend(['Temperature(K)', 'Humidity', 'Pressure(hPA)'])
    leg = plt.gca().get_legend()
    text_color = 'white'
    for text in leg.get_texts():
        plt.setp(text, color = text_color)

    # Change ticks color
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')
    #plt.suptitle('Environmental Conditions Along Vessel Routes', color='white', fontsize=24)
    plt.title('                                            Environmental Conditions Along Vessel Routes', color='white', fontsize=24)
    st.plotly_chart(kpi_chart, theme="streamlit")

def plot_cloud_cover(plot4):
    cloud_cover = px.histogram(plot4, x="description")
    cloud_cover.update_layout(bargap=0.2, width=900, height=400, title='Cloud Condition', title_x=0.3, title_font=dict(size=24))  # Set width and height
    cloud_cover.update_traces(marker=dict(color='skyblue'))  # Change 'green' to your desired color
    cloud_cover.update_xaxes(tickangle=-45)
    st.plotly_chart(cloud_cover, theme="streamlit")

Route = pd.read_csv(r"Marine_routes.csv")

trip_option = Route["routes"].unique()
imo_options = Route["imo"].unique().tolist()
grouped_data = Route.groupby(['imo', 'routes'])

group_9454462_r1 = grouped_data.get_group((9454462, 'route01'))
group_9454462_r2 = grouped_data.get_group((9454462, 'route02'))
group_9454462_r3 = grouped_data.get_group((9454462, 'route03'))
group_9301201_r1 = grouped_data.get_group((9301201, 'route01'))
group_9301201_r2 = grouped_data.get_group((9301201, 'route02'))
group_9301201_r3 = grouped_data.get_group((9301201, 'route03'))

st.set_page_config(page_title="Vessels", 
                   page_icon=":ship:", 
                   layout="wide",
                   initial_sidebar_state="expanded")
ship_path = "ship.jpg"

st.sidebar.image(ship_path, width=100, use_column_width=True)
st.sidebar.header("Vessel Dashboard")

Selected_IMO = st.sidebar.selectbox("Select IMO", imo_options, 0)
Routes = st.sidebar.selectbox("Select Route", trip_option, 0)

# Additional description in red color
additional_description1 = """
<div style='border: 3px solid #3f3f3f; padding: 10px; background-color: #29465B;'>
<span style='color: red'>
<b>Main Route (Bad Weather)</b><br>
Estimated Arrival time:<br>
03-03-2024 14:20 +00:00<br>
Distance: 4919.9nm<br>
Fuel Consumption: 1410.4mt<br>
CO2 Emission: 250t
</span>
</div>
"""
st.sidebar.markdown(additional_description1, unsafe_allow_html=True)
# Additional description in red color
additional_description2 = """
<div style='border: 3px solid #3f3f3f; padding: 10px; background-color: #29465B;'>
<span style='color: green'>
<b>Alternate Route</b><br>
Estimated Arrival time<br>
03-03-2024 03:20 +00:00<br>
Distance: 4911.8nm<br>
Fuel Consumption: 1396.4mt<br>
CO2 Emission: 205t
</span>
</div>
"""
st.sidebar.markdown(additional_description2, unsafe_allow_html=True)
# Additional description in red color
additional_description3 = """
<div style='border: 3px solid #3f3f3f; padding: 10px; background-color: #29465B;'>
<span style='color: Marble Blue'>
<b>Fuel Efficient</b><br>
Estimated Arrival time<br>
02-03-2024 23:47 +00:00<br>
Distance: 4913.8nm<br>
Fuel Consumption: 1296.4mt<br>
CO2 Emission: 195t<br>
Average Speed: 22.4Kn
</span>
</div>
"""
st.sidebar.markdown(additional_description3, unsafe_allow_html=True)

st.title("Marine Route Info")
# st.header("Fuse ship paths with dynamic weather, creating a captivating visual blend!")
# Sample Data
waypoints = ['Port A', 'Port B', 'Port C', 'Port D', 'Port E']
distances_nm = [1000, 1500, 1200, 800, 2000]  # Distance in nautical miles
vessel_cii = [0.2, 0.25, 0.18, 0.22, 0.15]  # Vessel's Carbon Intensity Indicator

if  Selected_IMO == 9454462 and Routes == 'route01':
    
    display_vessel_info(group_9454462_r1)

    file_path = r'(9454462)route01.html'
    display_html_map(file_path, height=700)
    
    st.subheader("Plots")

    col1, col2 = st.columns(2)

        # Load and display images in columns
    with col1:
        plot_speed_histogram(group_9454462_r1)
        plot_cloud_cover(group_9454462_r1)
    
    with col2:

        plot_speed_wind_speed(group_9454462_r1)
        plot_kpi(group_9454462_r1)

elif  Selected_IMO == 9454462 and Routes == 'route02':

    display_vessel_info(group_9454462_r2)

    file_path = r'(9454462)route02.html'
    display_html_map(file_path, height=700)
    
    
    st.subheader("Plots")

    col1, col2 = st.columns(2)

        # Load and display images in columns
    with col1:
        plot_speed_histogram(group_9454462_r2)
        plot_cloud_cover(group_9454462_r2)
    
    with col2:

        plot_speed_wind_speed(group_9454462_r2)
        plot_kpi(group_9454462_r2)

elif  Selected_IMO == 9454462 and Routes == 'route03':

    display_vessel_info(group_9454462_r3)

    file_path = r'(9454462)route03.html'
    display_html_map(file_path, height=700)

    st.subheader("Plots")
    
    col1, col2 = st.columns(2)

        # Load and display images in columns
    with col1:
        plot_speed_histogram(group_9454462_r3)
        plot_cloud_cover(group_9454462_r3)
    
    with col2:

        plot_speed_wind_speed(group_9454462_r3)
        plot_kpi(group_9454462_r3)

elif Selected_IMO == 9301201 and Routes == 'route01':

    display_vessel_info(group_9301201_r1)

    file_path = r'(9301201)route01.html'
    display_html_map(file_path, height=700)

    st.subheader("Plots")
    
    col1, col2 = st.columns(2)

        # Load and display images in columns
    with col1:
        plot_speed_histogram(group_9301201_r1)
        plot_cloud_cover(group_9301201_r1)
    
    with col2:

        plot_speed_wind_speed(group_9301201_r1)
        plot_kpi(group_9301201_r1)

        # Sample Data for Plotly graph
    waypoints = ['Port A', 'Port B', 'Port C', 'Port D', 'Port E']
    distances_nm = [1000, 1500, 1200, 800, 2000]  # Distance in nautical miles
    vessel_cii = [0.2, 0.25, 0.18, 0.22, 0.15]  # Vessel's Carbon Intensity Indicator

    # Create a Plotly figure
    fig = go.Figure()

    # Add bar trace for distance
    fig.add_trace(go.Bar(
        x=waypoints,
        y=distances_nm,
        name='Distance (nm)',
        marker_color='skyblue'
    ))

    # Add scatter trace for Vessel CII
    fig.add_trace(go.Scatter(
        x=waypoints,
        y=vessel_cii,
        mode='lines+markers',
        name='Vessel CII',
        yaxis='y2',
        line=dict(color='orange', width=2)
    ))

    # Update layout
    fig.update_layout(
        title='Voyage Distance and Vessel CII Along Route',
        xaxis=dict(title='Waypoints'),
        yaxis=dict(title='Distance (nm)'),
        yaxis2=dict(title='Vessel CII', overlaying='y', side='right'),
        legend=dict(y=1.1, orientation='h', x=0.3, yanchor='bottom')
    )

    # Display Plotly graph
    st.plotly_chart(fig)

                 
elif Selected_IMO == 9301201 and Routes == 'route02':

    display_vessel_info(group_9301201_r2)

    file_path = r'(9301201)route02.html'
    display_html_map(file_path, height=700)

    st.subheader("Plots")
    
    col1, col2 = st.columns(2)

    # Load and display images in columns
    with col1:
        plot_speed_histogram(group_9301201_r2)
        plot_cloud_cover(group_9301201_r2)
    
    with col2:

        plot_speed_wind_speed(group_9301201_r2)
        plot_kpi(group_9301201_r2)

elif Selected_IMO == 9301201 and Routes == 'route03':

    display_vessel_info(group_9301201_r3)

    file_path = r'(9301201)route03.html'
    display_html_map(file_path, height=700)

    st.subheader("Plots")
    
    col1, col2 = st.columns(2)

    # Load and display images in columns
    with col1:
        plot_speed_histogram(group_9301201_r3)
        plot_cloud_cover(group_9301201_r3)
    
    with col2:

        plot_speed_wind_speed(group_9301201_r3)
        plot_kpi(group_9301201_r3)

else:
    st.write("Data Not Available")


#cd C:\Users\WAQSA\anaconda3\Scripts
# streamlit run "C:\Users\WAQSA\Downloads\final_Demo_1 (2)\final_Demo_1\fin_demo.py"
