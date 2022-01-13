import sys
sys.path.insert(0, 'E:/Project/ML_and_DL/CBD/ChatBot/~/ParlAI/')

import os
from fpdf import FPDF
from datetime import datetime, timedelta
from parlai_internal.agents.laptopbot.Configuration.parameter_constants import *
from parlai_internal.agents.laptopbot.Configuration.notification import *



def create_header(day, pdf):
    pdf.set_font('Arial', style='B', size=18)
    pdf.set_text_color(0, 153, 255)
    pdf.ln(15)
    pdf.cell(50)  # Padding
    pdf.cell(w=80, h=20, txt="Analytical Report",
             border=0, ln=0, align='C')    # Align center

    pdf.ln(20)
    pdf.set_font('Arial', style='B', size=14)
    pdf.set_text_color(0, 153, 255)
    pdf.cell(78)  # Padding
    pdf.write(h=3, txt=f'{day}')


def create_analytic_report(day, filename="Analytical Report.pdf"):
    pdf = FPDF()

    ''' First Page '''
    # Header and title
    pdf.add_page()
    pdf.image("./parlai_internal/agents/laptopbot/Resources/header_report.png", 0, 0, WIDTH)
    create_header(day, pdf)
    # Table
    pdf.ln(16)
    pdf.set_font('Arial', size=15)
    pdf.set_text_color(0, 0, 5)
    pdf.cell(12)
    pdf.write(h=4, txt="Total Revenue - " + datetime.today().strftime("%B"))
    pdf.image("./parlai_internal/agents/laptopbot/Temp/table.png", 0, 65, WIDTH-20)
    # Chart
    pdf.image("./parlai_internal/agents/laptopbot/Temp/Type_Price_chart.png", 0, 125, WIDTH/2-10)
    pdf.image("./parlai_internal/agents/laptopbot/Temp/Type_Quant_chart.png", 105, 125, WIDTH/2-10)
    pdf.output("./parlai_internal/agents/laptopbot/Report/"+filename, 'F')
    ''' Second Page '''


if __name__ == '__main__':
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%d/%m/%Y")
    noti_rp_gen()
    create_analytic_report(yesterday)
    noti_rp_complete()
