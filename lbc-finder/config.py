from models import Search, Parameters
import lbc


def handle(ad: lbc.Ad, search_name: str):
    print(f"Nouvelles annonces pour {search_name}")
    print(f"Title : {ad.subject}")
    print(f"Price : {ad.price} €")
    print(f"URL : {ad.url}")
    print(f"status : {ad.status}")
    print(f"category_name : {ad.category_name}")
    print(f"location : {ad.location}")
    print(f"Body : {ad.body}")


location = lbc.City(lat=48.6846, lng=-1.3572, radius=50_000, city="Avranches")  # 10 km

CONFIG = [
    Search(
        name="Immeuble Avranche et peripherie",
        parameters=Parameters(
            text="immeuble",
            locations=[location],
            category=lbc.Category.IMMOBILIER,
            square=[80, 400],
            price=[0, 120_000],
        ),
        delay=60 * 5,  # Check every 5 minutes
        handler=handle,
    ),
]
