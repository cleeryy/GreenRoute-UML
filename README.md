# GreenRoute 🌿🚲

**Plateforme de livraison éco-responsable du dernier kilomètre**

Projet d'examen final — ESGI Modélisation UML2 (2025–2026)

## Présentation

GreenRoute est une start-up toulousaine qui orchestre les livraisons du dernier kilomètre en centre-ville via des livreurs indépendants utilisant exclusivement des modes de transport doux (vélos-cargos, triporteurs, camionnettes électriques).

Ce dépôt contient l'intégralité du dossier d'analyse fonctionnelle et de l'implémentation : diagrammes UML, maquettes UI, et code source Python.

## Structure du projet

```
📦 GreenRoute-UML
├── DAF_GreenRoute.md              ← Dossier d'Analyse Fonctionnelle complet
├── diagrams/                      ← Diagrammes UML (sources .puml + PNG)
│   ├── contexte.puml/png          ← Diagramme de contexte
│   ├── usecase.puml/png           ← Diagramme de cas d'utilisation
│   ├── classe.puml/png            ← Diagramme de classes
│   ├── dss_expediteur.puml/png    ← DSS n°1 — Parcours expéditeur
│   └── dss_livreur.puml/png       ← DSS n°2 — Parcours livreur
├── mockups/                       ← Maquettes UI interactives
│   ├── expediteur.html            ← Interface web expéditeur
│   └── livreur.html               ← Application mobile livreur
└── src/                           ← Code source Python OOP
    ├── main.py                    ← Démonstration end-to-end
    ├── model/                     ← Entités métier (Client, Order, Package, DeliveryPerson)
    └── services/                  ← Services (Pricing, Routing, Payment, Assignment)
```

## Blocs fonctionnels

| Bloc | Livrable | Statut |
|------|----------|--------|
| **Bloc 1** — Ingénierie des besoins | Diagramme de contexte, cas d'utilisation, descriptions textuelles | ✅ |
| **Bloc 2** — Architecture & dynamique | Diagramme de classes, diagrammes de séquence système (DSS) | ✅ |
| **Bloc 3** — UI/UX | Maquettes HTML (nominal + exception), critères Bastien & Scapin | ✅ |
| **Bloc 4** — Implémentation | Code Python OOP, encapsulation stricte, 13 fichiers | ✅ |

## Exécution du code

```bash
python3 -m src.main
```

La démo exécute le scénario complet : inscription client → création colis → commande → calcul devis → paiement → attribution livreur → collecte → livraison → scan QR Code.

## Génération des diagrammes

```bash
plantuml diagrams/*.puml
```

## Licence

Projet académique — ESGI 2025-2026
