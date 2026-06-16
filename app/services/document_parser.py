
from pypdf import PdfReader
from docx import Document

class DocumentParser:

    @staticmethod
    def parse_pdf(path):

        text=""

        reader=PdfReader(path)

        for page in reader.pages:

            content=page.extract_text()

            if content:
                text += content + "\n"

        return text

    @staticmethod
    def parse_docx(path):

        doc=Document(path)

        return "\n".join(
            p.text for p in doc.paragraphs
        )

    @staticmethod
    def parse(path):

        if path.endswith(".pdf"):
            return DocumentParser.parse_pdf(path)

        if path.endswith(".docx"):
            return DocumentParser.parse_docx(path)

        raise Exception("Unsupported file type")
