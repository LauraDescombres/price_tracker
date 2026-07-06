from dataclasses import dataclass

@dataclass
class Produit:
    id: int
    nom: str
    url: str
    actif: int
    prix_cible: float | None

@dataclass
class Releve:
    id: int
    produit_id: int
    prix: float
    date_releve: str