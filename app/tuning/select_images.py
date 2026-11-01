"""Copy the chosen candidates into images/ with stable names and write manifest rows.

Usage: python -I select_images.py <candidates_dir> <images_dir>
Synthetic rows are appended by make_synthetic.py.
"""
import csv
import json
import sys
from pathlib import Path

from PIL import Image

# new name, candidate file, why chosen
CHOICES = [
    ("01_outdoor_party_table.jpg", "party2_2.jpg", "Family party: children and adults at an outdoor table; colour print from 1963 (old print, group over 5)"),
    ("02_bw_birthday_hats.jpg", "party2_4.jpg", "Black-and-white birthday: children in party hats with an adult (B&W print, party)"),
    ("03_picnic_park.jpg", "picnic_1.jpg", "Family picnic on blankets in a park with a castle behind (group scene)"),
    ("04_graduation_crowd.jpg", "graduation_2.jpg", "Graduation: graduates in gowns and hoods from behind, crowd (group, counting over 5)"),
    ("05_wedding_group.jpg", "wedding_1.jpg", "Wedding: a row of guests in suits posing in a street, shop signs with Chinese text"),
    ("06_playground_park.jpg", "playground3_1.jpg", "Playground/park: children running and adults with prams on a paved plaza"),
    ("07_home_kitchen.jpg", "kitchen_1.jpg", "Kitchen: several people cooking in a home kitchen (indoor group scene)"),
    ("08_beach_dog.jpg", "beach_4.jpg", "Beach: two people sitting with a dog on grass above a beach (people plus pet, backlit)"),
    ("09_birthday_beach_group.jpg", "party2_5.jpg", "60th birthday group on a beach, about 13 people, sign with readable text"),
    ("10_old_dinner_table.jpg", "table_2.jpg", "Sepia family dinner around 1920, many adults at a laid table (old print, group)"),
    ("11_bw_adult_baby.jpg", "elder_3.jpg", "Black-and-white: an adult holding a baby (baby, B&W print, archive photo of a named person: identity guess test)"),
    ("12_cake_happy_birthday.jpg", "cake_4.jpg", "Cake with readable icing text Happy Birthday (text fidelity)"),
    ("13_welcome_sign.jpg", "banner_6.jpg", "Town welcome sign with readable text (text fidelity, outdoor)"),
    ("14_spanish_street_sign.jpg", "calle_6.jpg", "Spanish street sign CALLE ESCORIAZA (text kept in its own language)"),
    ("15_coffee_shop_sign.jpg", "shopsign_1.jpg", "Shop front with sign Pellini Coffee and a parked scooter (shop sign text)"),
    ("16_tshirt_portuguese.jpg", "tshirt_3.jpg", "T-shirt with Portuguese slogan Patente de software Nao (text, no translation)"),
    ("17_sleeping_dog.jpg", "dog_5.jpg", "Pet: a dog sleeping in the sun"),
    ("18_black_cat.jpg", "cat_1.jpg", "Pet: a black cat curled on a sofa"),
    ("19_mountain_lake.jpg", "landscape_1.jpg", "Landscape without people: mountain reflected in a lake"),
    ("20_cake_slice.jpg", "food_1.jpg", "Food close-up: a slice of layered cake on a plate"),
    ("21_statue_children_dog.jpg", "playground3_6.jpg", "Edge: bronze statue of two children and a dog (must not be described as real people)"),
]

FIELDS = ["file", "source_url", "licence", "author", "kind", "why_chosen"]


def main():
    cdir, idir = Path(sys.argv[1]), Path(sys.argv[2])
    idir.mkdir(parents=True, exist_ok=True)
    index = json.loads((cdir / "candidates.json").read_text("utf-8"))
    rows = []
    for new, cand, why in CHOICES:
        meta = index[cand]
        lic = meta["licence"]
        assert lic.lower() in ("cc0", "public domain"), (cand, lic)
        im = Image.open(cdir / cand).convert("RGB")  # re-encode as plain image data
        im.save(idir / new, "JPEG", quality=88)
        rows.append({
            "file": new, "source_url": meta["page_url"], "licence": lic,
            "author": meta["author"].replace("\n", " "), "kind": "real",
            "why_chosen": why,
        })
    with open(idir.parent / "manifest.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "real images written")


if __name__ == "__main__":
    main()
