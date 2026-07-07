"""Énumérations pour la plateforme de livraison GreenRoute."""

from enum import Enum


class OrderStatus(Enum):
    """Statuts possibles d'une commande tout au long de son cycle de vie.

    - A_ATTRIBUER : en attente d'attribution à un livreur
    - VERROUILLEE_FRAUDE : commande bloquée pour suspicion de fraude
    - EN_COURS_D_ATTRIBUTION : en cours d'attribution à un livreur
    - EN_COURS_DE_LIVRAISON : en cours de livraison
    - LIVRE : livrée avec succès
    """

    A_ATTRIBUER = "A_ATTRIBUER"
    VERROUILLEE_FRAUDE = "VERROUILLEE_FRAUDE"
    EN_COURS_D_ATTRIBUTION = "EN_COURS_D_ATTRIBUTION"
    EN_COURS_DE_LIVRAISON = "EN_COURS_DE_LIVRAISON"
    LIVRE = "LIVRE"


class UrgencyLevel(Enum):
    """Niveaux d'urgence pour une livraison.

    - STANDARD : livraison sous 24h (tarif de base)
    - EXPRESS : livraison sous 2h (supplément de 30 %)
    """

    STANDARD = "Standard"
    EXPRESS = "Express"


class DeliveryPersonState(Enum):
    """États opérationnels d'un livreur.

    - DISPONIBLE : disponible pour accepter des missions
    - EN_TOURNEE : actuellement en tournée de livraison
    """

    DISPONIBLE = "Disponible"
    EN_TOURNEE = "En Tournée"
