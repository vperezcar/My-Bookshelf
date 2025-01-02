from model.image import Image
import re

class Book:
    book_id: int
    id: str
    title: str
    authors: list
    publisher: str
    published_date: str
    description: str
    page_count: int
    categories: list
    image_links: dict
    image: Image
    language: str

    def __init__(
        self,
        id,
        title,
        authors,
        publisher,
        published_date,
        description,
        page_count,
        categories,
        image_links,
        language,
    ):
        self.id = id
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.published_date = published_date
        self.description = description
        self.page_count = page_count
        self.categories = categories
        self.image_links = image_links
        self.language = language
        image_link = None
        if "smallThumbnail" in self.image_links:
            image_link = self.image_links["smallThumbnail"]
        elif "thumbnail" in self.image_links:
            image_link = self.image_links["thumbnail"]
        self.image = Image(image_link) if image_link else None

    def get_authors(self):
        return f"De: {"Desconocido" if not self.authors else ", ".join(self.authors)}"

    def get_publisher(self):
        return f"Publicado por: {self.publisher}" if self.publisher else "Editorial desconocida"

    def get_published_date(self):
        return f"Fecha de publicación: {self.published_date}" if self.published_date else "Fecha de publicación desconocida"
        
    def get_number_of_pages(self):
        return f"{self.page_count} páginas" if self.page_count else "Número de páginas desconocido"
    
    def get_description(self):
        # There are some reviews in the description, beutifiy the text to make it more readable
        if not self.description:
            return "Descripción no disponible"
        match = re.search("Reseñas de .*:", self.description)
        if match:
            description = self.description[:match.end()] + "\n"
            # Retrieve each review and add a new line before it
            index = match.end()
            reviews = self.description[index:].split("\"")
            # Reviews are between quotes, whereas after that is the author of the review
            author = False
            for review in reviews:
                review = review.strip()
                if review:
                    if author:
                        description += f"por {review}.\n"
                        author = False
                    else:
                        description += f"\"{review}\" "
                        author = True
            return description
        else:
            return self.description
        
    def get_categories(self):
        return f"Categorías: {"Desconocidas" if not self.categories else ", ".join(self.categories)}"
    
    def get_language(self):
        return f"Idioma: {self.language}" if self.language else "Idioma desconocido"