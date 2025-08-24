import mysql.connector
import pandas as pd
import streamlit as st
import matplotlib. pyplot as plt

mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "12345",
        database = "Phone_Pay",
        autocommit = True)
mycursor = mydb.cursor()


# State_Wise_Overall_Transaction_Trend 
Case_Study = ['Decoding Transaction Dynamics on PhonePe','Transaction Analysis for Market Expansion',
              'Transaction Analysis Across States and Districts','User Registration Analysis',
              'Insurance Engagement Analysis']

selected_Case_study = st.selectbox("Select a case study",Case_Study,key = "Case_Study")


if selected_Case_study == "Decoding Transaction Dynamics on PhonePe":
    def State_Wise_Transaction_Trend(State_Name): # Function Definition
        Query = f"""SELECT state, year, quater, 
            SUM(Transacion_amount) as Total_Transaction_Amount 
            FROM agg_trans 
            WHERE state = %s
            GROUP BY state, year, quater
            ORDER BY year, quater;"""
        mycursor.execute(Query,(State_Name,))
        Data = mycursor.fetchall()
        df = pd.DataFrame(Data,columns=['State','Year','Quater','Total_Transaction_Amount'])
        df['Yearly_Quaterly'] = df['Year'].astype(str) + '_Q' + df['Quater'].astype(str)
        return df
    st.title('State_Wise_Transaction_Trend')
    mycursor.execute("Select Distinct State from agg_trans Order by State")
    states = [i[0] for i in mycursor.fetchall()]
    selected_state = st.selectbox("Select a State", states)
    df = State_Wise_Transaction_Trend (selected_state) # Function calling
    st.dataframe(df)
    years = df['Year'].unique()
    selected_year = st.multiselect(" Filter by Year", years, default= years)
    filtered_df = df[df['Year'].isin(selected_year)]
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(filtered_df['Yearly_Quaterly'], filtered_df['Total_Transaction_Amount'], marker='o')
    ax.set_title(f"Transaction Trend for {selected_state.title()}")
    ax.set_xlabel("Year_Quarter")
    ax.set_ylabel("Total Transaction Amount")
    plt.xticks(rotation=90)
    st.pyplot(fig)

elif selected_Case_study == "Transaction Analysis for Market Expansion":
    def State_Wise_Transaction_Type_Trend(State_Name,Transaction_Type):
        Query = f"""select state,year,quater,Transacion_type,sum(Transacion_amount)
        as Total_Transaction_Amount from agg_trans 
        where Transacion_type = %s and state = %s group by 
        state,year,quater,Transacion_type ; """
        mycursor.execute(Query,(Transaction_Type,State_Name))
        Data = mycursor.fetchall()
        df = pd.DataFrame(Data,columns=['State','Year','Quater','Transacion_type','Total_Transaction_Amount'])
        df['Yearly_Quaterly'] = df['Year'].astype(str) + '_Q' + df['Quater'].astype(str)
        return df
    st.title("State_Wise_Tansaction_Type_Trend")
    mycursor.execute("Select Distinct State from agg_trans Order by State")
    states = [i[0] for i in mycursor.fetchall()]
    selected_state = st.selectbox("Select a State", states,key = "state_Select")
    mycursor.execute("Select distinct Transacion_type from agg_trans order by Transacion_type")
    Transaction_Type = [i[0] for i in mycursor.fetchall()]
    Selected_Transaction_Type = st.selectbox("Select Transaction Type", Transaction_Type,key = "Type_Select")
    df = State_Wise_Transaction_Type_Trend (selected_state,Selected_Transaction_Type) # Function calling
    st.dataframe(df)
    years = df['Year'].unique()
    selected_year = st.multiselect(" Filter by Year", years, default= years,key = "Years_Filter")
    filtered_df = df[df['Year'].isin(selected_year)]
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(filtered_df['Yearly_Quaterly'], filtered_df['Total_Transaction_Amount'], marker='o')
    ax.set_title(f"Transaction Trend for {selected_state.title()}")
    ax.set_xlabel("Year_Quarter")
    ax.set_ylabel("Total Transaction Amount")
    plt.xticks(rotation=90)
    st.pyplot(fig)

elif selected_Case_study == "Transaction Analysis Across States and Districts":
        mycursor.execute("select state,sum(Top_Transacion_amount) as Total_Transaction_Amount from top_trans group by state order by Total_Transaction_Amount DESC")
        Data = mycursor.fetchall()
        df = pd.DataFrame(Data,columns=['State','Total_Transaction_Amount'])
        df.index = range(1,len(df)+1)
        st.title("Top_10_States_Transaction")
        Top_10 = df.head(10)
        st.dataframe(Top_10)
        fig,ax = plt.subplots(figsize = (10,5))
        ax.barh(Top_10['State'],Top_10['Total_Transaction_Amount'])
        ax.set_xlabel('Total_Transaction_Amount')
        ax.set_ylabel('State')
        plt.xticks(rotation = 90)
        st.pyplot(fig)
        mycursor.execute("select Top_Transacion_District_Name , sum(Top_Transacion_amount) as Total_Transaction_Amount from top_trans group by Top_Transacion_District_Name order by Total_Transaction_Amount DESC")
        Data = mycursor.fetchall()
        df = pd.DataFrame(Data,columns=['Districts','Total_Transaction_Amount'])
        df.index = range(1,len(df)+1)
        st.title("Top_10_District_Transaction")
        Top_10 = df.head(10)
        st.dataframe(Top_10)
        fig,ax = plt.subplots(figsize = (10,5))
        ax.barh(Top_10['Districts'],Top_10['Total_Transaction_Amount'])
        ax.set_xlabel('Total_Transaction_Amount')
        ax.set_ylabel('Districts')
        plt.xticks(rotation = 90)
        st.pyplot(fig)

elif selected_Case_study == 'User Registration Analysis':
    st.title ("User Registration Analysis")
    mycursor.execute("select DISTINCT year from top_users group by year")
    years = [i[0] for i in mycursor.fetchall()]
    selected_year = st.selectbox ("Select Year",years,key = "years_Filtered")
    mycursor.execute("select distinct quater from top_users group by quater")
    quaters = [i[0] for i in mycursor.fetchall()]
    selected_quater = st.selectbox("Select Year",quaters,key = "Quaters_Filtered")
    mycursor.execute("""
        SELECT State, SUM(Top_registered_Users) AS Total_Register_users
        FROM top_users 
        WHERE year = %s AND quater = %s
        GROUP BY State
        ORDER BY Total_Register_users DESC
        LIMIT 10 """, (selected_year,selected_quater))
    state_Data = mycursor.fetchall()
    df_states = pd.DataFrame(state_Data,columns = ['State','Total_Register_users'])
    st.subheader(f"Top_10_Registerd_Users ({selected_year} Q {selected_quater})")
    st.dataframe(df_states)
    fig1,ax1 =plt.subplots(figsize=(10,5))
    ax1.barh(df_states['State'],df_states['Total_Register_users'],color = "skyblue")
    ax1.set_xlabel("Total_Register_users")
    ax1.set_ylabel("State")
    ax1.set_title(f"Top 10 States by Registered Users ({selected_year} Q{selected_quater})")
    st.pyplot(fig1)
    mycursor.execute("""
        SELECT Top_User_District_Name, SUM(Top_registered_Users) AS Total_Register_users
        FROM top_users 
        WHERE year = %s AND quater = %s
        GROUP BY Top_User_District_Name
        ORDER BY Total_Register_users DESC
        LIMIT 10 """, (selected_year,selected_quater))
    District_Data = mycursor.fetchall()
    df_Districts = pd.DataFrame(District_Data,columns = ['District_Name','Total_Register_users'])
    st.subheader(f"Top_10_Registerd_Users_District ({selected_year} Q {selected_quater})")
    st.dataframe(df_Districts)
    fig2,ax2 =plt.subplots(figsize=(10,5))
    ax2.barh(df_Districts['District_Name'],df_Districts['Total_Register_users'],color = "skyblue")
    ax2.set_xlabel("Total_Register_users")
    ax2.set_ylabel("District_Name")
    ax2.set_title(f"Top 10 States by Registered Users ({selected_year} Q{selected_quater})")
    st.pyplot(fig2)

    
elif selected_Case_study == 'Insurance Engagement Analysis':
    st.title ("Insurance Engagement Analysis")
    mycursor.execute("select DISTINCT year from top_insurance group by year")
    years = [i[0] for i in mycursor.fetchall()]
    selected_year = st.selectbox ("Select Year",years,key = "years_Filtered")
    mycursor.execute("select distinct quater from top_insurance group by quater")
    quaters = [i[0] for i in mycursor.fetchall()]
    selected_quater = st.selectbox("Select Year",quaters,key = "Quaters_Filtered")
    mycursor.execute("select state,sum(Top_Insurance_Amount) as Total_insurance_Amount from top_insurance group by state order by Total_insurance_Amount DESC limit 10;")
    State_Data = mycursor.fetchall()
    df_state = pd.DataFrame(State_Data,columns = ['State','Total_insurance_Amount'])
    st.subheader(f"Top 10 States ({selected_year} Q{selected_quater})")
    st.dataframe(df_state)
    fig1,ax1=plt.subplots(figsize=(10,5))
    ax1.barh(df_state['State'],df_state['Total_insurance_Amount'],color = "skyblue")
    ax1.set_xlabel("Total_insurance_Amount")
    ax1.set_ylabel("State")
    ax1.set_title(f"Top 10 States by Registered Users ({selected_year} Q{selected_quater})")
    st.pyplot(fig1)

    mycursor.execute("select Top_Insurance_District_Name,sum(Top_Insurance_Amount) as Total_insurance_Amount from top_insurance group by Top_Insurance_District_Name order by Total_insurance_Amount DESC LIMIT 10;")
    District_Data = mycursor.fetchall()
    df_District = pd.DataFrame(District_Data,columns = ['District','Total_insurance_Amount'])
    st.subheader(f"Top 10 States ({selected_year} Q{selected_quater})")
    st.dataframe(df_District)
    fig2,ax2=plt.subplots(figsize=(10,5))
    ax2.barh(df_District['District'],df_District['Total_insurance_Amount'],color = "skyblue")
    ax2.set_xlabel("Total_insurance_Amount")
    ax2.set_ylabel("District")
    ax1.set_title(f"Top 10 States by Registered Users ({selected_year} Q{selected_quater})")
    st.pyplot(fig2)

