import sys
sys.path.insert(0, 'E:/Project/ML_and_DL/CBD/Chatbot/')

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from Configuration.parameter_constants import *
from Database.function_retrieve_data import Query


def render_table(data, col_width=3.0, row_height=0.625, font_size=14,
                header_color='#0066CC', row_colors=['#f1f1f2', 'w'], edge_color='w',
                bbox=[0, 0, 1, 1], header_columns=0, ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')
    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in mpl_table._cells.items():
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax.get_figure(), ax


def create_plot(month_query):
    month_Revenue = month_query.copy().rename(columns={"laptop_ID": "Laptop ID", "user_ID": "User ID"})
    row_Revenue = ['','','','Revenue:']
    Revenue = round(month_Revenue["Total"].sum(), 3)
    row_Revenue.append(Revenue)
    month_Revenue.loc[str(month_Revenue.shape[0])] = row_Revenue
    # Table
    fig, ax = render_table(month_Revenue, header_columns=0, col_width=2.0)
    fig.savefig("./Temp/table.png")
    # Chart 1
    quantity = month_query["Quantity"].apply(lambda x: int(x))
    plt.figure()
    Type_Quant_chart = sns.barplot(x="Quantity", y="laptop_ID", data=pd.concat([month_query["laptop_ID"],quantity],axis=1))
    Type_Quant_chart.set_title('Number of laptops sold by ID')
    plt.savefig('./Temp/Type_Quant_chart.png')
    # Chart 2
    plt.figure()
    Int_Price = month_query["Price"].apply(lambda x: float(x)).tolist()
    Type = month_query["laptop_ID"].tolist()
    my_explode = (0, 0.1, 0)
    Type_Price_chart = plt.pie(Int_Price,labels=Type,autopct='%1.1f%%',shadow = True, explode=my_explode)
    plt.title('Money by ID')
    plt.axis('equal')
    plt.savefig('./Temp/Type_Price_chart.png')
    

if __name__ == '__main__':

    """  Database 2  """
    DATABASE = 'order_record'
    MONTH = 1
    query = Query(SERVER, DATABASE_ORDER, USER, PASSWORD)
    month_query = query.query_auto_AR(MONTH)
    create_plot(month_query)

    


