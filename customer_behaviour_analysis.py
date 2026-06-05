import pandas as pd
from sqlalchemy import create_engine


# LOAD DATASET

df = pd.read_csv("customer_shopping_behavior.csv")


# DATA UNDERSTANDING

print(df.info())
print(df.describe())

# HANDLE MISSING VALUES
print(df.isnull().sum())



df['Review Rating'] = (
    df.groupby('Category')['Review Rating']
    .transform(lambda x: x.fillna(x.median()))
)


# RENAME COLUMNS (Snake Case)


df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')

df = df.rename(
    columns={
        'purchase_amount_(usd)': 'purchase_amount'
    }
)

# CREATE AGE GROUP COLUMN


labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']

df['age_group'] = pd.qcut(
    df['age'],
    q=4,
    labels=labels
)


# CREATE PURCHASE FREQUENCY DAYS


frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}

df['purchase_frequency_days'] = (
    df['frequency_of_purchases']
    .map(frequency_mapping)
)


# DROP DUPLICATE COLUMN


# print(
#     (df['discount_applied'] ==
#      df['promo_code_used']).all()
# )

# df = df.drop('promo_code_used', axis=1)


# CHECK CLEANED DATA


# print(df.head())

# print(df.columns)


# CONNECT MYSQL


engine = create_engine(
    "mysql+pymysql://root:Aditya%40123@localhost/customer_shopping_behaviour"
)


# UPLOAD CLEANED DATA TO MYSQL


df.to_sql(
    name='customer_shopping_behaviour',
    con=engine,
    if_exists='replace',
    index=False
)

# print("Cleaned data uploaded successfully!")