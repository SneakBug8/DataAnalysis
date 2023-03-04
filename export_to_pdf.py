import pandas as pd
import plotly.express as px
from xhtml2pdf import pisa             # import python module
import base64
import os

# Utility function
def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return True on success and False on errors
    return pisa_status.err

width = 600
height = 400

template = (''
    '<img src="data:image/png;base64,{image}">'
    '{caption}'                              # Optional caption to include below the graph
    '<br>'
    '<hr>'
'')

def export_to_pdf(figures, outputname):
    if not os.path.exists("images"):
        os.mkdir("images")

    # Generate their images using `py.image.get`
    images = [base64.b64encode(figure.to_image(format="png")).decode('utf-8') for figure in figures]

    report_html = ''
    for image in images:
        _ = template
        _ = _.format(image=image, caption='', width=width, height=height)
        report_html += _

    # display(HTML(report_html))
    convert_html_to_pdf(report_html, outputname)