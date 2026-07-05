from dataclasses import dataclass

@dataclass
class Produit:
    id: int
    nom: str
    url: str
    actif: int
    prix_cible: float | None