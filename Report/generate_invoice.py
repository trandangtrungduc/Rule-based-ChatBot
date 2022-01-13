import sys
sys.path.insert(0, 'E:/Project/ML_and_DL/CBD/ChatBot/~/ParlAI/')

from fpdf import FPDF
from datetime import datetime, timedelta
from parlai_internal.agents.laptopbot.Configuration.parameter_constants import *
from parlai_internal.agents.laptopbot.Configuration.notification import *





def create_invoice(filename="Invoice.pdf"):
    pdf = FPDF()

    ''' First Page '''
    # Header 
    pdf.add_page()
    pdf.image("./parlai_internal/agents/laptopbot/Resources/header_invoice.png", 0, 0, WIDTH)
    # Due date, invoice date, invoice no
    pdf.set_font('Arial', size=8, style='b')
    pdf.set_text_color(255, 255, 255)
    pdf.cell(176)
    pdf.write(h=4, txt="111")
    pdf.ln(4.5)
    pdf.cell(172)
    pdf.write(h=4, txt=datetime.today().strftime("%d/%m/%Y"))
    pdf.ln(4.5)
    pdf.cell(172)
    pdf.write(h=4, txt=(datetime.today() + timedelta(days=10)).strftime("%d/%m/%Y"))
    # Customer info and table
    pdf.ln(20)
    pdf.set_font('Arial', size=13)
    pdf.set_text_color(0, 0, 5)
    pdf.cell(15)
    pdf.write(h=4, txt="Customer information")
    pdf.image("./parlai_internal/agents/laptopbot/Resources/bill_ship.png", 25, 50, WIDTH-45)
    # Invoice info and table
    pdf.ln(52)
    pdf.set_font('Arial', size=13)
    pdf.set_text_color(0, 0, 5)
    pdf.cell(16)
    pdf.write(h=4, txt="Purchase information")
    pdf.image("./parlai_internal/agents/laptopbot/Temp/table_invoice.png", 0, 95, WIDTH)
    # Footer 
    pdf.image("./parlai_internal/agents/laptopbot/Resources/footer_invoice.png", 0, 245, WIDTH)
    # Terms and Conditions
    # pdf.rect(5, 212, WIDTH-110, HEIGHT-255, style='D')
    pdf.image("./parlai_internal/agents/laptopbot/Resources/terms.png", 10, 220, WIDTH-125)
    pdf.output("./parlai_internal/agents/laptopbot/Report/"+filename, 'F')

if __name__ == '__main__':
    noti_rp_gen()
    create_invoice()
    noti_rp_complete()
