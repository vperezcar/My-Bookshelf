from openpyxl import Workbook
from openpyxl.cell.text import InlineFont
from openpyxl.cell.rich_text import TextBlock, CellRichText
from utils.globals import get_data, USER_BOOK_TABS


def export_to_excel(filename):
    user_books, years = get_data()
    wb = Workbook()
    for year in years:
        wb.create_sheet(title=year)
        ws = wb[year]
        ws.append(
            [
                CellRichText(TextBlock(InlineFont(b=True, sz=14), "Estado")),
                CellRichText(TextBlock(InlineFont(b=True, sz=14), "Calificación")),
                CellRichText(TextBlock(InlineFont(b=True, sz=14), "Título")),
                CellRichText(TextBlock(InlineFont(b=True, sz=14), "Autor")),
                CellRichText(TextBlock(InlineFont(b=True, sz=14), "Editorial")),
                CellRichText(
                    TextBlock(InlineFont(b=True, sz=14), "Fecha de Publicación")
                ),
                CellRichText(TextBlock(InlineFont(b=True, sz=14), "Número de Páginas")),
                CellRichText(TextBlock(InlineFont(b=True, sz=14), "Categorías")),
                CellRichText(TextBlock(InlineFont(b=True, sz=14), "Idioma")),
            ]
        )

    for user_book in user_books:
        ws = wb[user_book.update_date.split("/")[2].split(" ")[0]]
        ws.append(
            [
                USER_BOOK_TABS[user_book.status.value],
                user_book.score,
                user_book.book.title,
                ", ".join(user_book.book.authors),
                user_book.book.publisher,
                user_book.book.published_date,
                user_book.book.page_count,
                ", ".join(user_book.book.categories),
                user_book.book.language,
            ]
        )

    # Resize columns to fit the content
    for year in years:
        ws = wb[year]
        for column_cells in ws.columns:
            length = max(len(str(cell.value)) for cell in column_cells)
            ws.column_dimensions[column_cells[0].column_letter].width = length + 10

    del wb["Sheet"]

    wb.save(filename)
