"""Démonstration complète de la plateforme GreenRoute — Bloc 4 UML.

Ce script exécute un scénario de bout en bout :
  1. Création d'un client
  2. Création d'un colis
  3. Passage de commande
  4. Calcul du prix via PricingService
  5. Paiement via ToulousePay (PaymentService)
  6. Enregistrement d'un livreur disponible
  7. Attribution via AssignmentEngine
  8. Acceptation et ramassage
  9. Livraison avec vérification QR code
 10. Affichage des statuts à chaque étape
"""

from datetime import datetime, timezone

from src.model import (
    Client,
    DeliveryPerson,
    Order,
    OrderStatus,
    Package,
    UrgencyLevel,
)
from src.services import (
    AssignmentEngine,
    PaymentService,
    PricingService,
    RoutingService,
)


def print_separator(title: str) -> None:
    """Affiche un titre de section formaté."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def main() -> None:
    """Scénario complet de démonstration GreenRoute."""

    # ── 1. Création d'un client ──────────────────────────────────────
    print_separator("1. Création d'un client")
    client = Client(
        name="Sophie Martin",
        email="sophie.martin@example.com",
        phone="+33 6 12 34 56 78",
    )
    print(f"Client créé : {client}")
    print(f"  ID        : {client.client_id}")
    print(f"  Email     : {client.email}")
    print(f"  Inscrit le: {client.registered_on.strftime('%d/%m/%Y à %H:%M')}")

    # ── 2. Création d'un colis ───────────────────────────────────────
    print_separator("2. Création d'un colis")
    package = Package(
        weight=3.5,
        length=30.0,
        width=20.0,
        height=15.0,
    )
    print(f"Colis créé : {package}")
    print(f"  Volume : {package.volume:.0f} cm³")

    # ── 3. Passage de commande ───────────────────────────────────────
    print_separator("3. Passage de commande")
    order = client.place_order(
        package=package,
        pickup_address="10 Rue du Rempart, 31000 Toulouse",
        delivery_address="45 Allées Jean Jaurès, 31000 Toulouse",
        urgency=UrgencyLevel.EXPRESS,
    )
    print(f"Commande créée : {order}")
    print(f"  ID         : {order.order_id}")
    print(f"  Urgence    : {order.urgency.value}")
    print(f"  Statut     : {order.status.value}")
    print(f"  Adresse    : {order.pickup_address} → {order.delivery_address}")
    print(f"  Code QR    : {order.qr_code}")
    print(f"  Créée le   : {order.created_at.strftime('%d/%m/%Y à %H:%M:%S')}")

    # ── 4. Calcul du prix via PricingService ─────────────────────────
    print_separator("4. Calcul du prix")
    distance_km = RoutingService.calculate_distance(
        order.pickup_address,
        order.delivery_address,
    )
    print(f"Distance estimée : {distance_km} km")

    pricing = PricingService.calculate_cost(
        package=order.package,
        distance_km=distance_km,
        urgency=order.urgency,
    )
    order.total_cost = pricing["total_cost"]
    order.carbon_savings = pricing["carbon_savings"]

    print(f"Coût total      : {order.total_cost:.2f} €")
    print(f"CO₂ économisé   : {order.carbon_savings:.0f} g")
    print(f"  (vs livreur diesel : {distance_km * 150:.0f} g CO₂)")

    # ── 5. Paiement ──────────────────────────────────────────────────
    print_separator("5. Paiement via ToulousePay")
    payment_success = PaymentService.process_payment(client, order.total_cost)
    if payment_success:
        order.paid_at = datetime.now(timezone.utc)
        print(f"Paiement accepté ✅ — {order.total_cost:.2f} € débités")
        print(f"Payé le : {order.paid_at.strftime('%d/%m/%Y à %H:%M:%S')}")
    else:
        print(f"Paiement refusé ❌ — {order.total_cost:.2f} €")
        order.mark_fraud()
        print(f"Commande verrouillée (statut : {order.status.value})")
        # Fin du scénario en cas d'échec de paiement
        return

    # ── 6. Enregistrement d'un livreur ───────────────────────────────
    print_separator("6. Enregistrement d'un livreur")
    delivery_person = DeliveryPerson(
        name="Lucas Dubois",
        email="lucas.dubois@greenroute.io",
        phone="+33 7 98 76 54 32",
        transport_mode="Vélo cargo électrique",
        latitude=43.6050,  # Proche du point de ramassage
        longitude=1.4450,
    )
    print(f"Livreur créé : {delivery_person}")
    print(f"  ID        : {delivery_person.delivery_person_id}")
    print(f"  Transport : {delivery_person.transport_mode}")
    print(f"  Position  : ({delivery_person.latitude}, {delivery_person.longitude})")
    print(f"  État      : {delivery_person.current_state.value}")

    # ── 7. Attribution via AssignmentEngine ──────────────────────────
    print_separator("7. Attribution de la commande")
    engine = AssignmentEngine()
    engine.register_order(order)
    engine.register_delivery_person(delivery_person)

    print(f"Commandes en attente : {len(engine.pending_orders)}")
    print(f"Livreurs disponibles  : {len(engine.available_delivery_persons)}")

    assigned_order = engine.assign_order_to_nearest(order)
    if assigned_order is None:
        print("Aucun livreur trouvé dans le rayon de 3 km 😞")
        return

    print(f"Commande assignée à {delivery_person.name} !")
    print(f"  Statut commande : {order.status.value}")
    print(f"  Livreur         : {order.delivery_person}")

    # ── 8. Acceptation et ramassage ──────────────────────────────────
    print_separator("8. Acceptation et ramassage")
    delivery_person.accept_order(order)
    print(f"Livreur a accepté la commande")
    print(f"  Statut commande : {order.status.value}")
    print(f"  État livreur    : {delivery_person.current_state.value}")

    # Le livreur se déplace vers le point de ramassage
    delivery_person.update_location(43.6047, 1.4442)
    order.confirm_pickup()
    print(f"Colis ramassé !")
    print(f"  Statut commande : {order.status.value}")
    print(f"  État livreur    : {delivery_person.current_state.value}")

    # ── 9. Livraison avec vérification QR code ──────────────────────
    print_separator("9. Livraison et vérification QR code")
    print(f"Code QR attendu : {order.qr_code}")

    # Tentative avec un mauvais code (doit échouer)
    try:
        order.confirm_delivery(qr_code="MAUVAIS-CODE-QR")
    except ValueError as e:
        print(f"  → Tentative avec mauvais code rejetée : {e}")

    # Tentative avec le bon code
    order.confirm_delivery(qr_code=order.qr_code)
    print(f"  → Code QR correct ! Livraison confirmée ✅")
    print(f"  Statut        : {order.status.value}")
    delivered_str = order.delivered_at.strftime('%d/%m/%Y à %H:%M:%S') if order.delivered_at else "N/A"
    print(f"  Livré le      : {delivered_str}")
    print(f"  État livreur  : {delivery_person.current_state.value}")

    # ── 10. Récapitulatif final ─────────────────────────────────────
    print_separator("10. Récapitulatif final")
    print(f"  Client       : {client.name} ({client.email})")
    print(f"  Colis        : {package.weight} kg — {package.volume:.0f} cm³")
    print(f"  Trajet       : {order.pickup_address}")
    print(f"               → {order.delivery_address}")
    print(f"  Distance     : {distance_km} km")
    print(f"  Urgence      : {order.urgency.value}")
    print(f"  Coût total   : {order.total_cost:.2f} €")
    print(f"  CO₂ évité    : {order.carbon_savings:.0f} g")
    print(f"  Livreur      : {delivery_person.name} ({delivery_person.transport_mode})")
    print(f"  Statut final : {order.status.value}")

    # Vérification que la commande est bien dans l'historique du client
    print(f"\n  Commandes du client : {len(client.orders)}")
    for o in client.orders:
        print(f"    • {o}")


if __name__ == "__main__":
    main()
