import git
from git.repo import Repo
import pandas as pd
import os
import streamlit as st
import pymysql as sql
import matplotlib.pyplot as plt
import json
from streamlit_option_menu import option_menu
from PIL import Image
from geopy.geocoders import Nominatim
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from st_btn_select import st_btn_select
from streamlit_pills import pills

def get_lat_long():
    geolocator=Nominatim(user_agent='my_geocoder')
    try:
        geolocator.geocode("Chennai",country_codes='India')
    except:
        pass

def remove_district(word):
    words=list(word.split())
    words=' '.join(words[:-1])
    return words


os.environ["GIT_PYTHON_REFRESH"] = "quiet"

def store_data():
    #AGGREGATED TRANSACTION

    path_t=r'C:/Users/jonna/PycharmProjects/pulse-master/data/aggregated'
    data1= {
                'State':[],'Year':[],'Quarter':[],'Transaction_type':[],'Transaction_count':[],'Transaction_amount':[]
                }
    data2={
                'State': [], 'Year': [], 'Quarter': [], 'Brands': [], 'Count': [], 'Percentage': []
                }

    #AGGREGATE CONTENT

    for i in os.listdir(path_t):
        path1=path_t + str(i) +'/country/india/state'
        content_list=os.listdir(path1)

        for state in content_list:
            st_path=path1 + '/' + state
            yr_list=os.listdir(st_path)
            for year in yr_list:
                yr_path= st_path +'/'+ year
                qtr_list=os.listdir(yr_path)

                for quarter in qtr_list:
                    qtr_path=os.path.join(yr_path,quarter)
                    with open(qtr_path,'r') as file:
                        A=json.load(file)
                    if i=='transaction':
                        try:
                            for j in A['data']['transactionData']:
                                name = j['name']
                                count = j['paymentInstruments'][0]['count']
                                amount = j['paymentInstruments'][0]['amount']
                                data1['Transaction_type'].append(name)
                                data1['Transaction_count'].append(count)
                                data1['Transaction_amount'].append(amount)
                                data1['State'].append(state)
                                data1['Year'].append(year)
                                data1['Quarter'].append(quarter[0])
                        except:
                            pass
                    elif i=='user':
                        try:
                            for j in A['data']['usersByDevice']:
                                brand_name = j["brand"]
                                counts = j["count"]
                                percents = j["percentage"]
                                data2["Brands"].append(brand_name)
                                data2["Count"].append(counts)
                                data2["Percentage"].append(percents)
                                data2["State"].append(state)
                                data2["Year"].append(year)
                                data2["Quarter"].append(quarter[0])
                        except:
                            pass

    agg_transact=pd.DataFrame(data1)
    agg_usedata=pd.DataFrame(data2)

    #MAP CONTENT

    path_m=r'C:/Users/jonna/PycharmProjects/pulse-master/data/map'

    data3= {
                'State':[],'Year':[],'Quarter':[],'District':[],'Transaction_count':[],'Transaction_amount':[]
                }
    data4={
                'State': [], 'Year': [], 'Quarter': [], 'District': [], 'RegisteredUser': [], 'AppOpens': []
                }

    for i in os.listdir(path_m):
        path1=path_m + str(i) +'/hover/country/india/state'
        content_list=os.listdir(path1)

        for state in content_list:
            st_path=path1 + '/' + state
            yr_list=os.listdir(st_path)
            for year in yr_list:
                yr_path= st_path +'/'+ year
                qtr_list=os.listdir(yr_path)

                for quarter in qtr_list:
                    qtr_path=os.path.join(yr_path,quarter)
                    with open(qtr_path,'r') as file:
                        A=json.load(file)
                    if i=='transaction':
                        try:
                            for j in A['data']['hoverDataList']:
                                district = remove_district(j['name'])
                                count = j['metric'][0]['count']
                                amount = j['metric'][0]['amount']
                                data3['District'].append(district)
                                data3['Transaction_count'].append(count)
                                data3['Transaction_amount'].append(amount)
                                data3['State'].append(state)
                                data3['Year'].append(year)
                                data3['Quarter'].append(quarter[0])
                        except:
                            pass
                    elif i=='user':
                            for j in A['data']['hoverData'].items():
                                district = remove_district(j[0])
                                registereduser = j[1]['registeredUsers']
                                appOpens= j[1]["appOpens"]
                                data4["District"].append(district)
                                data4["RegisteredUser"].append(registereduser)
                                data4['AppOpens'].append(appOpens)
                                data4["State"].append(state)
                                data4["Year"].append(year)
                                data4["Quarter"].append(quarter[0])

    map_transact=pd.DataFrame(data3)
    map_usedata=pd.DataFrame(data4)


    #TOP

    path_top=r'C:/Users/jonna/PycharmProjects/pulse-master/data/top'

    data5={'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Transaction_count': [],
                'Transaction_amount': []}

    data6={'State': [], 'Year': [], 'Quarter': [], 'Pincode': [],
                'RegisteredUsers': []}
    for i in os.listdir(path_top):
        path1=path_top + str(i) +'/country/india/state'
        content_list=os.listdir(path1)

        for state in content_list:
            st_path=path1 + '/' + state
            yr_list=os.listdir(st_path)
            for year in yr_list:
                yr_path= st_path +'/'+ year
                qtr_list=os.listdir(yr_path)

                for quarter in qtr_list:
                    qtr_path=os.path.join(yr_path,quarter)
                    with open(qtr_path,'r') as file:
                        A=json.load(file)
                    if i=='transaction':
                        try:
                            for j in A['data']['pincodes']:
                                pin = j['entityName']
                                count = j['metric']['count']
                                amount = j['metric']['amount']
                                data5['Pincode'].append(pin)
                                data5['Transaction_count'].append(count)
                                data5['Transaction_amount'].append(amount)
                                data5['State'].append(state)
                                data5['Year'].append(year)
                                data5['Quarter'].append(quarter[0])
                        except:
                            pass
                    elif i=='user':
                            for j in A['data']['pincodes']:
                                name = j['name']
                                registereduser = j['registeredUsers']
                                data6["Pincode"].append(name)
                                data6["RegisteredUsers"].append(registereduser)
                                data6["State"].append(state)
                                data6["Year"].append(year)
                                data6["Quarter"].append(quarter[0])

    top_transact=pd.DataFrame(data5)
    top_usedata=pd.DataFrame(data6)

    agg_transact.to_csv('agg_trans.csv',index=False)
    agg_usedata.to_csv('agg_user.csv',index=False)
    map_transact.to_csv('map_trans.csv',index=False)
    map_usedata.to_csv('map_user.csv',index=False)
    top_transact.to_csv('top_trans.csv',index=False)
    top_usedata.to_csv('top_user.csv',index=False)


    #SQL part
    import mysql.connector as sql

    conn=sql.connect(host='localhost',user='root',port=3306,password='Mahesh2005',database='phonepepulse')
    cursor = conn.cursor(buffered=True)

    # Creating agg_trans table
    cursor.execute("create table agg_trans (State varchar(100), Year int, Quarter int, Transaction_type varchar(100), Transaction_count int, Transaction_amount double)")

    for i,row in agg_transact.iterrows():
        sql = "INSERT INTO agg_trans VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, tuple(row))
        conn.commit()

    # Creating agg_user table
    cursor.execute("create table agg_user (State varchar(100), Year int, Quarter int, Brands varchar(100), Count int, Percentage double)")

    for i,row in agg_usedata.iterrows():
        sql = "INSERT INTO agg_user VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, tuple(row))
        conn.commit()

    # Creating map_trans table
    cursor.execute("create table map_trans (State varchar(100), Year int, Quarter int, District varchar(100), Count int, Amount double)")

    for i,row in map_transact.iterrows():
        sql = "INSERT INTO map_trans VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, tuple(row))
        conn.commit()

    #Creating map_user table
    cursor.execute("create table map_user (State varchar(100), Year int, Quarter int, District varchar(100), Registered_user int, App_opens int)")

    for i,row in map_usedata.iterrows():
        sql = "INSERT INTO map_user VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, tuple(row))
        conn.commit()

    #Creating top_trans table
    cursor.execute("create table top_trans (State varchar(100), Year int, Quarter int, Pincode int, Transaction_count int, Transaction_amount double)")

    for i,row in top_transact.iterrows():
        sql = "INSERT INTO top_trans VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, tuple(row))
        conn.commit()

    #Creating top_user table
    cursor.execute("create table top_user (State varchar(100), Year int, Quarter int, Pincode int, Registered_users int)")

    for i,row in top_usedata.iterrows():
        sql = "INSERT INTO top_user VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, tuple(row))
        conn.commit()

#THE STREAMLIT PART
icon=Image.open("C:/Users/jonna/PycharmProjects/pulse-master/phone.jpg")
st.set_page_config(page_title='Phonepe Pulse Data Visualization and Exploration',page_icon=icon,layout='wide')
with st.sidebar:

    selected = option_menu("Menu", ["Home","Top Charts","Map"],
                icons=["house","graph-up-arrow","compass"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})

# MENU 1 - HOME
if selected == "Home":
    st.markdown("# :violet[Phonepe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="large")
    with col1:
        st.write("\n")
        st.write("\n")
        st.write("\n ")
        st.write("\n")
        st.markdown("##### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    with col2:
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.image(icon,width=400)


conn=sql.connect(host='localhost',user='root',port=3306,password='Mahesh2005',database='phonepepulse')
cursor = conn.cursor()

if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))

    #TRANSACTION
    if Type =="Transactions":
        col1,col2=st.columns([1,1],gap='large')
        with col1:
            Year=pills('Select desired Year',['2019','2020','2021','2022','2023'])
        with col2:
            if Year=='2023':
                Quarter=pills('Select Quarter',['1','2','3'])
            else:
                Quarter=pills('Select Quarter',['1','2','3','4'])
        st.write("\n ")
        st.write("\n")
        st.write("\n ")
        st.write("\n")

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('# :violet[State]')
            cursor.execute(f"SELECT state, sum(Transaction_count) as Total_transact,CAST(sum(Transaction_amount) AS SIGNED) as Total_amount from agg_trans where Year={Year} and Quarter= {Quarter} GROUP by state order by Total_Amount desc limit 10")
            df1=pd.DataFrame(cursor.fetchall(),columns=['State','Transaction Count', 'Transaction Amount']).reset_index(drop=True)
            df1.index+=1
            st.dataframe(df1)
            fig1=px.pie(df1,values='Transaction Amount',names='State',hover_data=['State','Transaction Amount','Transaction Count'])
        with col2:
            st.markdown('### TOP 10 States with Highest Transaction Amount')
            st.plotly_chart(fig1,use_container_width=True)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('# :violet[District]')
            cursor.execute(f"SELECT district,sum(Count) AS Count, CAST(sum(Amount) AS SIGNED) AS Amount from map_trans where Year={Year} and Quarter={Quarter} Group BY district order by Amount DESC limit 10")
            df2=pd.DataFrame(cursor.fetchall(),columns=['District','Transaction Count','Transaction Amount']).reset_index(drop=True)
            df2.index+=1
            st.dataframe(df2)
            fig2=px.pie(df2,values='Transaction Amount',names='District',hover_data=['District','Transaction Amount','Transaction Count'])
        with col2:
                st.markdown('### TOP 10 Districts with Highest Transaction Amount')
                st.plotly_chart(fig2,use_container_width=True)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('# :violet[Pincode]')
            cursor.execute(f"SELECT pincode, sum(Transaction_count), CAST(sum(Transaction_amount) AS SIGNED) AS Amount from top_trans where Year={Year} and Quarter={Quarter} Group by pincode order by Amount DESC limit 10")
            df3=pd.DataFrame(cursor.fetchall(),columns=['Pincode','Transaction Count', "Transaction Amount"]).reset_index(drop=True)
            df3.index+=1
            st.dataframe(df3)
            fig3=px.pie(df3,values='Transaction Amount', names='Pincode',hover_data=['Pincode','Transaction Amount','Transaction Count'])

        with col2:
                st.markdown('### TOP 10 Pincodes with Highest Transaction Amount')
                st.plotly_chart(fig3,use_container_width=True)


    #USERS
    elif Type=='Users':
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        if Year==2023:
            Quarter = st.slider("Quarter", min_value=1, max_value=3)
        else:
            Quarter = st.slider("Quarter", min_value=1, max_value=4)
        st.write("\n ")
        st.write("\n")
        st.write("\n ")
        st.write("\n")
        color='#aa75f4'

        col1,col2=st.columns([1,1],gap='large')
        if Year==2023:
            pass
        else:

            with col1:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('# :violet[Brands]')
                cursor.execute(f"SELECT brands, sum(Count) as Count, avg(Percentage) as percent from agg_user where Year={Year} and Quarter= {Quarter} GROUP by brands order by Count desc limit 10")
                df1=pd.DataFrame(cursor.fetchall(),columns=['Brands','Transaction Count', 'Percentage']).reset_index(drop=True)
                df1.index+=1
                st.dataframe(df1)
                fig1=px.bar(df1,x="Brands",y="Transaction Count",color='Brands',hover_data=['Brands','Transaction Count','Percentage'])
            with col2:
                st.markdown(f'<H2 style="text-align:center; color: {color}">Transaction Count with Different Brands</H2>',unsafe_allow_html=True)
                st.plotly_chart(fig1,use_container_width=True)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('# :violet[District]')

            cursor.execute(f"SELECT district,sum(Registered_user) As registered, sum(App_opens) AS opens from map_user where Year={Year} and Quarter={Quarter} Group BY district order by registered DESC limit 10")
            df2=pd.DataFrame(cursor.fetchall(),columns=['District','Users','App Opens']).reset_index(drop=True)
            df2.index+=1
            if Year==2018 or (Year==2019 and Quarter==1):
                df_edit=df2[['District','Users']]
                st.dataframe(df_edit)

            else:
                st.dataframe(df2)
            fig2=px.bar(df2,x='District',y='Users',color='District',hover_data=['District','Users','App Opens'])
            fig2.update_xaxes(tickmode='array',tickvals=[])
            fig2.update_traces(textposition='inside')

        with col2:
                st.markdown(f'<H2 style="text-align:center; color: {color}">Top Users based on Districts</H2>',unsafe_allow_html=True)
                st.plotly_chart(fig2,use_container_width=True)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('# :violet[Pincode]')
            cursor.execute(f"SELECT State, CAST(pincode AS char) AS pincode , sum(Registered_users) AS Users from top_user where Year={Year} and Quarter={Quarter} Group by pincode,State order by Users DESC limit 20")
            df3=pd.DataFrame(cursor.fetchall(),columns=['State','pincode',"Users"]).reset_index(drop=True)
            df3['pincode']=df3['pincode'].astype(str)
            df3.index+=1
            st.dataframe(df3)
            fig3=px.pie(df3,values='Users',names='pincode')
        with col2:
                st.markdown(f'<H2 style="text-align:center; color: {color}">Top Users based on Pincode</H2>',unsafe_allow_html=True)
                st.plotly_chart(fig3,use_container_width=True)

if selected=='Map':
    color='#aa75f4'
    select=st.selectbox('Select Map',('OPTIONS','Choropleth', 'Map'))

    if select=="Map":
        number=st.selectbox('Select Option',('OPTIONS ','Top 10','Top 20','Top 30','Top 40','Top 50'))
        st.warning('Disclaimer: The data beyond Top 20 might take more time!')
        try:
            number=number.split(' ')[1]
            number=int(number)

            col1,col2=st.columns([4,4],gap='large')

            with col1:
                st.markdown('<br>',unsafe_allow_html=True)
                st.write('\n')
                st.write('\n')
                st.write('\n')

                m=folium.Map(location=[20.5937,78.9629],zoom_start=4)
                cursor.execute(f'SELECT District,State,sum(Count) as Count,CAST(sum(Amount) AS SIGNED) as Amount from map_trans group by District,State order by Amount DESC limit {number}')
                dfm=pd.DataFrame(cursor.fetchall(),columns=['District','State','Count','Amount']).reset_index(drop=True)
                dfm.index+=1
                Markerclt=MarkerCluster().add_to(m)
                for index,row in dfm.iterrows():
                    district=row['District']
                    state=row['State']
                    count=row['Count']
                    amount=row['Amount']
                    geolocator=Nominatim(user_agent='my_geocoder')
                    try:
                        location=geolocator.geocode(f"{district}",country_codes='India')
                        lat,long=location.latitude,location.longitude
                        marker=[lat,long]
                        folium.Marker(marker,popup=f'District:{district} \n Count: {count} \n Amount:{amount}',tooltip=f"{district},{state}").add_to(Markerclt)
                    except:
                        pass
                st_folium(m,width=725)
                st.write(f'<H4 style="text-align:center;">This is a MAP representation of the Top {number} Districts for Highest Transaction Amount </H4> ',unsafe_allow_html=True)

            with col2:
                st.write('\n')
                st.write('\n')
                st.write('\n')


                st.table(dfm)


        except:
            pass

    if select== "Choropleth":
        col1,col2=st.columns([1,1],gap='large')

        with col1:
            st.write('<br>',unsafe_allow_html=True)
            st.write('\n')
            st.write('\n')
            st.write('\n')
            cursor.execute(f"SELECT State,sum(Registered_user) As registered, sum(App_opens) AS opens from map_user Group BY State order by opens DESC")
            dfc=pd.DataFrame(cursor.fetchall(),columns=['State','Users','App Opens']).reset_index(drop=True)
            dfc.index+=1
            dfc['State'].update(dfc['State'].str.replace('-',' ',regex=True))
            dfc['State']=dfc['State'].apply(lambda x:' '.join([word.capitalize() for word in x.split()]))
            st.table(dfc)

        with col2:
            st.write('\n')
            st.write('\n')

            dfc['App Opens']=dfc['App Opens'].astype(float)
            dfc['Users']=dfc['Users'].astype(float)

            st.markdown('## Indian Statewise App Opens Distribution: A Choropleth Analysis')
            figc=px.choropleth(data_frame=dfc,locations=dfc['State'],geojson='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson',color=dfc['App Opens'],color_continuous_scale='plasma',featureidkey='properties.ST_NM',hover_data=['App Opens','Users','State'])
            figc.update_geos(fitbounds="locations", visible=True)
            st.plotly_chart(figc,use_container_width=True)
            st.write('\n')
            st.markdown('## Indian Statewise User Distribution: A Choropleth Analysis')

            figc=px.choropleth(data_frame=dfc,locations=dfc['State'],geojson='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson',color=dfc['Users'],color_continuous_scale='viridis',featureidkey='properties.ST_NM',hover_data=['Users','App Opens','State'])
            figc.update_geos(fitbounds="locations", visible=True)
            st.plotly_chart(figc,use_container_width=True)
