# PhonePe_Analytics_Dashboard
Interactive Streamlit dashboard analyzing PhonePe transactions, user registrations, and insurance engagement across states and districts.
# PhonePe Analytics Dashboard

A Streamlit app to analyze PhonePe data with interactive visualizations. This project provides insights on:

- **State-wise Transaction Trends:** Visualize transactions over time by state.
- **Transaction Analysis by Type:** Explore trends by different transaction types.
- **Top States and Districts:** Identify regions with highest transactions and user registrations.
- **User Registration Analysis:** Track top states and districts for user sign-ups.
- **Insurance Engagement Analysis:** Analyze insurance participation across regions.

## Features
- Interactive charts and dashboards
- Filter data by year and quarter
- Bar plots and line charts for trends
- Easy to run locally with Streamlit

## Data Extraction
This data has been structured to provide details of following three sections with data cuts on Transactions, Users and Insurance of PhonePe Pulse - Explore tab.

1) Aggregated - Aggregated values of various payment categories as shown under Categories section
2) Map - Total values at the State and District levels.
3) Top - Totals of top States / Districts /Pin Codes
All the data provided in these folders is of JSON format.
Syntax :
data
|___ aggregated
    |___ transactions
        |___ country
            |___ india
                |___ 2018
                |    1.json
                |    2.json
                |    3.json
                |    4.json

                |___ 2019
                |    ...
                |___ 2019
                |___ state
                    |___ andaman-&-nicobar-islands
                        |___2018
                        |   1.json
                        |   2.json
                        |   3.json
                        |   4.json

                    |___ andhra-pradesh
                    |    ...
                    |    ...

