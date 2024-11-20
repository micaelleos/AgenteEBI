
from fpdf import FPDF
import io
import re

def remove_caracteres_incompativeis(texto):
    texto.replace('\u2014', '-')
    return re.sub(r'[‘’]', "'", texto)  # Substitui os apóstrofos curvos por simples

def limpar_caracteres(dict):
    dict_limpo = {}
    for item in dict.keys():
        dict_limpo[item] = remove_caracteres_incompativeis(dict[item])
    return dict_limpo

def impressão_a4(Ebi):
    ebi = limpar_caracteres(Ebi)
    # Cria um objeto PDF
    pdf = FPDF(format="A4")
    pdf.set_creator(creator="Teófilo: Assistente de EBI")

    # Adiciona uma página ao PDF
    pdf.add_page()

    # Define a fonte (Arial, estilo normal, tamanho 12)
    pdf.set_font('Arial', 'B', 16)

    # Adiciona um título
    pdf.cell(0, 10, txt=ebi["title"], ln=True, align='C')
    pdf.ln(h = '15')
    # Define uma nova fonte para o corpo do texto
    pdf.set_font('Helvetica', '', 12)

    # Adiciona outro parágrafo
    pdf.write(5,ebi["plaintext_base"])

    pdf.ln(h = '15')
    pdf.ln(h = '15')
    pdf.set_font('Helvetica', 'B', 12)
    # Adiciona texto ao PDF
    pdf.cell(200, 10, txt="Perguntas", ln=True, align='L')

    pdf.set_font('Helvetica', '', 12)
    pdf.write(8, txt=ebi["description"])

    pdf.ln(h = '25')
    pdf.ln(h = '25')
    pdf.set_font('Helvetica', 'I', 12)
    pdf.cell(200, 10, txt="Para refletir:", ln=True, align='L')
    pdf.write(8, txt=ebi["footer"])

    nome = "EBI: "+str(ebi["title"])+".pdf"
    # Salva o arquivo PDF
    # Criar um buffer em memória
    buffer = io.BytesIO()

    # Salvar o PDF no buffer diretamente como bytes
    pdf_output = pdf.output(dest='S').encode('latin1')
    
    # Escrever no buffer
    buffer.write(pdf_output)

    # Retornar ao início do buffer
    buffer.seek(0)

    return buffer, nome

def impressão_mobile(Ebi):
    ebi = limpar_caracteres(Ebi)
    # Cria um objeto PDF
    pdf = FPDF(format=(80,500))
    pdf.set_margins(left=5, top=1, right=5)
    pdf.set_creator(creator="Teófilo: Assistente de EBI")

    # Adiciona uma página ao PDF
    pdf.add_page()

    # Define a fonte (Arial, estilo normal, tamanho 12)
    pdf.set_font('Arial', 'B', 12)

    # Adiciona um título
    pdf.write(5,ebi["title"]+'\n')
    pdf.ln(h = '15')
    #pdf.cell(40, 10, txt=ebi["title"], ln=True, align='C')

    # Define uma nova fonte para o corpo do texto
    pdf.set_font('Helvetica', '', 9)

    # Adiciona outro parágrafo
    pdf.write(5,ebi["plaintext_base"])

    pdf.ln(h = '10')
    pdf.set_font('Helvetica', 'B', 10)
    # Adiciona texto ao PDF
    pdf.cell(200, 10, txt="Perguntas", ln=True, align='L')

    pdf.set_font('Helvetica', '', 9)
    pdf.write(7, txt=ebi["description"])

    pdf.ln(h = '10')
    pdf.ln(h = '10')
    pdf.set_font('Helvetica', 'I', 9)
    pdf.cell(0, 10, txt="Para refletir:", ln=True, align='L')
    pdf.set_font('Helvetica', 'I', 9)
    pdf.write(5, txt=ebi["footer"])

    nome = "EBI: "+str(ebi["title"])+" (mobile)"+".pdf"

    # Criar um buffer em memória
    buffer = io.BytesIO()

    # Salvar o PDF no buffer diretamente como bytes
    pdf_output = pdf.output(dest='S').encode('latin1')
    
    # Escrever no buffer
    buffer.write(pdf_output)

    # Retornar ao início do buffer
    buffer.seek(0)

    return buffer, nome