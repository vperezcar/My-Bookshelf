from openpyxl import Workbook
from openpyxl.cell.text import InlineFont
from openpyxl.cell.rich_text import TextBlock, CellRichText
from utils.globals import get_data
from utils.constants.constants import USER_BOOK_TABS, EXCEL_HEADERS


def export_to_excel(filename):
    user_books, years = get_data()
    wb = Workbook()
    for year in years:
        wb.create_sheet(title=year)
        ws = wb[year]
        ws.append(
            [
                CellRichText(TextBlock(InlineFont(b=True, sz=14), EXCEL_HEADERS[0])),
                CellRichText(TextBlock(InlineFont(b=True, sz=14), EXCEL_HEADERS[1])),
                CellRichText(TextBlock(InlineFont(b=True, sz=14), EXCEL_HEADERS[2])),
                CellRichText(TextBlock(InlineFont(b=True, sz=14), EXCEL_HEADERS[3])),
                CellRichText(TextBlock(InlineFont(b=True, sz=14), EXCEL_HEADERS[4])),
                CellRichText(TextBlock(InlineFont(b=True, sz=14), EXCEL_HEADERS[5])),
                CellRichText(TextBlock(InlineFont(b=True, sz=14), EXCEL_HEADERS[6])),
                CellRichText(TextBlock(InlineFont(b=True, sz=14), EXCEL_HEADERS[7])),
                CellRichText(TextBlock(InlineFont(b=True, sz=14), EXCEL_HEADERS[8])),
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
