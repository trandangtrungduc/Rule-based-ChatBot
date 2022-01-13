import sys
sys.path.insert(0, 'E:/Project/ML_and_DL/CBD/ChatBot/~/ParlAI/')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from parlai_internal.agents.laptopbot.Configuration.parameter_constants import *
from parlai_internal.agents.laptopbot.Database.function_retrieve_data import Query


def render_table_invoice(data, col_width=8.0, row_height=0.7, font_size=14,
                header_color='#3366CC', row_colors=['#f1f1f2', 'w'], edge_color='black',
                bbox=[0, 0, 1, 1], header_columns=0, ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        _, ax = plt.subplots(figsize=size)
        ax.axis('off')
    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs, cellLoc='center')
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in mpl_table._cells.items():
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w', wrap=True)
            cell.set_facecolor(header_color)
    return ax.get_figure(), ax

 
def create_plot_invoice(invoice_df):
    # Invoice details
    invoice_df = invoice_df.assign(Amount=round(invoice_df["Price"].apply(float)*invoice_df["Quantity"].apply(int),3))
    row_Discount = ['','','','Discount:','']
    row_Tax = ['','','','Tax:','']
    row_Total = ['','','','Total:']
    Total = str(round(invoice_df["Amount"].sum(), 3)) + " Euro"
    row_Total.append(Total)
    invoice_df.loc[str(invoice_df.shape[0])] = row_Discount
    invoice_df.loc[str(invoice_df.shape[0])] = row_Tax
    invoice_df.loc[str(invoice_df.shape[0])] = row_Total
    fig, ax = render_table_invoice(invoice_df, header_columns=0, col_width=3.0)
    fig.savefig("./parlai_internal/agents/laptopbot/Temp/table_invoice.png")
    

if __name__ == '__main__':
    pass
    """  Database 2  """
    

    


