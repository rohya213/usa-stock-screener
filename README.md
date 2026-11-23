im working on a personal project to create a visualisation tool that uses data from usaspending.gov api endpoints and another website that provides stock market data to see the impact the newly awarded contracts have on company's stock price.

# next
# overall
- find out what are the steps for my personal project (DOING NOW)
- create github project repo
- Steps...
    1)
    - END PRODUCT (rough sketch and description) ✅

    2)
    - DB SCHEMA DESIGN (researching how to do it) 🔄
        - create a db schema (sql server)
        - tables with cols >> apply the constraints and dtype (primary key and for key) >> define relationships between the table (claude)
        - research, prepare and extract the necessary fields for the end product
        - visualize by sketching an ERD
        - create a database in sql too

    3)
- fix the python ETL pipeline script (fetch clean and load to sql server) >> company name to stock ticker mapping script etc.

    4)
- BACK-END API layer (python) >> req data from sql server w/o exposing db credentials
    - choose api framework
    - create endpoints

    5)
- front-end UI (tbc)

# in ssms
- refresh memory of sql data relationships (1-1, 1-n, m-n); primary and foreign key 
- join based on which col?
- refreshing mem on sql
- optimize etl script 
- automate the pipeline (main.py is root)
- find out what the schema folder should be for