from model.image import Image
import utils.constants.constants as constants
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
        if self.image_links:
            if "smallThumbnail" in self.image_links:
                image_link = self.image_links["smallThumbnail"]
            elif "thumbnail" in self.image_links:
                image_link = self.image_links["thumbnail"]
        self.image = Image(image_link) if image_link else None

    def get_authors(self):
        return f"{constants.FROM} {constants.UNKNOWN if not self.authors else ", ".join(self.authors)}"

    def get_publisher(self):
        return (
            f"{constants.PUBLISHED_BY} {self.publisher}"
            if self.publisher
            else constants.UNKNOWN_PUBLISHER
        )

    def get_published_date(self):
        return (
            f"{constants.PUBLISHED_DATE} {self.published_date}"
            if self.published_date
            else constants.UNKNOWN_PUBLISHED_DATE
        )

    def get_number_of_pages(self):
        return (
            f"{self.page_count} {constants.PAGES}"
            if self.page_count
            else constants.UNKNOWN_PAGES
        )

    def get_description(self):
        if not self.description:
            return constants.UNKNOWN_DESCRIPTION
        # There are some reviews in the description, beutifiy the text to make it more readable
        description = self.split_reviews(constants.REVIEWS_BY_REGEX, constants.BY)
        # Split the english description
        math = re.search("ENGLISH DESCRIPTION", self.description)
        if math:
            description = f"{self.description[:math.start()]}\n{self.description[math.start():math.end()]}{self.description[math.end():]}"
        return description

    def split_reviews(self, search_input, by_text):
        match = re.search(search_input, self.description)
        if match:
            description = self.description[: match.end()] + "\n"
            # Retrieve each review and add a new line before it
            index = match.end()
            reviews = self.description[index:].split('"')
            # Reviews are between quotes, whereas after that is the author of the review
            author = False
            for review in reviews:
                review = review.strip()
                if review:
                    if author:
                        description += f"{by_text} {review}.\n"
                        author = False
                    else:
                        description += f'"{review}" '
                        author = True
            return description
        else:
            return self.description

    def get_categories(self):
        return f"{constants.CATEGORIES} {constants.UNKNOWN if not self.categories else ", ".join(self.categories)}"

    def get_language(self):
        return (
            f"{constants.LANGUAGE} {self.language}"
            if self.language
            else constants.UNKNOWN_LANGUAGE
        )
