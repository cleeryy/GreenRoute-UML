# Notes de soutenance — GreenRoute

## Organisation

| Intervenant | Slides | Durée | Blocs |
|---|---|---|---|
| **Intervenant 1** | 1 → 4 | ~6 min | Contexte, besoins, cas d'utilisation |
| **Intervenant 2** | 5 → 6 | ~7 min | Architecture, classes, DSS |
| **Intervenant 3** | 7 → 9 | ~7 min | Maquettes, critères, code |
| **Tous** | 10 → 11 | Q&A 10 min | Questions |

> ⏱ **Chronométrage conseillé** : chaque slide = ~1 min à 1 min 30.
> Ne lisez pas — racontez. Gardez un ton naturel, regardez le comité.

---

## Slide 1 — Accueil (Intervenant 1)

**⏱ ~1 min**

> _"Bonjour à tous, merci de votre présence. Nous sommes [Prénom] [Nom], [Prénom] [Nom] et [Prénom] [Nom], et nous allons vous présenter aujourd'hui notre projet **GreenRoute**._

_Bienvenue à cette revue d'architecture technique pour notre plateforme de livraison éco-responsable du dernier kilomètre._

_GreenRoute, c'est une start-up toulousaine qui vient de remporter un appel d'offres de la métropole de Toulouse pour repenser les livraisons en centre-ville."_

---

## Slide 2 — Problématique & Vision (Intervenant 1)

**⏱ ~1 min 30**

> _"Concrètement, aujourd'hui à Toulouse, les livraisons du dernier kilomètre sont assurées majoritairement par des camionnettes thermiques — qui saturent l'espace urbain, polluent, et représentent un coût environnemental énorme._

_GreenRoute se positionne comme l'alternative. Notre solution : orchestrer une flotte de livreurs indépendants utilisant uniquement des modes doux — vélos-cargos, triporteurs, et petites camionnettes électriques._

_L'objectif est triple :_

> _1. Offrir une plateforme aux expéditeurs pour gérer leurs livraisons simplement_
> _2. Répartir intelligemment la charge entre livreurs disponibles_
> _3. Prouver scientifiquement l'impact écologique de chaque trajet avec des métriques CO₂_

_Nous avons gagné un appel d'offres auprès de la métropole de Toulouse — c'est le point de départ du projet."_

---

## Slide 3 — Périmètre fonctionnel (Intervenant 1)

**⏱ ~1 min 30**

> _"Parlons maintenant du périmètre de notre système. Nous avons deux acteurs humains principaux._

_D'un côté, l'**expéditeur** — un client qui utilise la plateforme web pour envoyer un colis. Il s'authentifie, saisit les adresses, les caractéristiques du colis, choisit son niveau d'urgence, et paie. Il reçoit ensuite un ticket avec un QR Code unique._

_De l'autre côté, le **livreur** — qui utilise une application mobile. Il déclare sa disponibilité, son téléphone transmet sa position GPS en continu, et il reçoit des notifications quand un colis est disponible près de chez lui._

_Le système s'appuie aussi sur deux API externes : ToulouseMap pour la cartographie et les itinéraires, et ToulousePay pour le paiement sécurisé._

_Pour les relations entre cas d'utilisation :_

- _Le **include** signifie qu'un cas en déclenche obligatoirement un autre — par exemple, pour passer une commande, il faut **obligatoirement** être authentifié. C'est une inclusion._
- _Le **extend** est une extension conditionnelle — par exemple, la saisie manuelle du code n'est proposée que **si** le QR Code est illisible. C'est une extension, pas un chemin principal._

_Si vous voulez plus de détails, je vous invite à voir les descriptions textuelles complètes dans le DAF."_

---

## Slide 4 — Descriptions textuelles (Intervenant 1)

**⏱ ~1 min 30**

> _"Entrons dans le détail des deux cas d'utilisation principaux._

**_Premier cas : la demande de prise en charge._**
_Le client connecté saisit ses adresses, le poids et dimensions du colis, et choisit Standard ou Express. Le système interroge ToulouseMap pour la distance, calcule un devis — avec le coût financier et les grammes de CO₂ économisés. Si le client valide, il paie via ToulousePay. Si la banque accepte, la commande passe en statut **A_ATTRIBUER**, un QR Code est généré._

_Si le paiement est refusé → statut **VERROUILLEE_FRAUDE**, le client doit modifier son moyen de paiement._

**_Deuxième cas : la livraison._**
_Le livreur disponible reçoit une notification pour un colis dans un rayon de 3 km. Il a 60 secondes pour accepter. S'il accepte, il reçoit une feuille de route optimisée (via ToulouseMap), va chercher le colis, valide la collecte. Arrivé à destination, il scanne le QR Code — et c'est livré, statut **LIVRE**._

_Si le QR Code est abîmé ? Il saisit le code à 12 caractères manuellement. Pas de réseau ? L'app stocke en local et synchronise dès que possible._

_Je passe la parole à [Prénom Intervenant 2] pour l'architecture."_

---

## Slide 5 — Diagramme de classes (Intervenant 2)

**⏱ ~2 min 30**

> _"Merci. Je vais maintenant vous présenter l'architecture du modèle de données._

_Nous avons **quatre entités principales** :_

- _**Client** — avec identifiant unique, nom, email, etc. Un client peut passer plusieurs commandes._
- _**Order** — c'est la classe centrale. Elle porte le statut qui évolue tout au long du cycle de vie, le QR Code, les informations financières et écologiques. Elle est liée à un client et peut être assignée à un livreur._
- _**Package** — en composition forte avec Order. Un colis n'existe pas sans commande, et une commande a exactement un colis. On y trouve le poids et les dimensions._
- _**DeliveryPerson** — le livreur, avec son état (Disponible ou En Tournée), sa position GPS et son mode de transport._

_Le **cycle des statuts** est le suivant :_

- _A_ATTRIBUER → EN_COURS_D_ATTRIBUTION → EN_COURS_DE_LIVRAISON → LIVRE_
- _Et en cas d'échec de paiement : VERROUILLEE_FRAUDE_

_Nous avons aussi **quatre services** qui opèrent sur ces entités : PricingService pour les calculs de coût, RoutingService pour les itinéraires, PaymentService pour la validation bancaire, et AssignmentEngine — le moteur d'attribution qui utilise la formule de **Haversine** pour trouver le livreur le plus proche dans un rayon de 3 km._

_Tous les attributs sont privés, l'accès se fait uniquement par propriétés — une encapsulation stricte, comme demandé."_

---

## Slide 6 — DSS (Intervenant 2)

**⏱ ~2 min 30**

> _"Passons aux diagrammes de séquence système, qui montrent la dimension temporelle des échanges._

**_Premier DSS — le parcours expéditeur._**
_On commence par l'authentification, puis on entre dans une boucle. Le client peut recommencer la saisie s'il annule le devis. On utilise plusieurs fragments :_

- _Un **alt** pour modéliser la validation ou le refus du devis_
- _Un **break** pour sortir de la boucle quand le paiement est accepté_
- _Un **alt** pour la réponse de ToulousePay — acceptation ou refus_

_C'est important car ça montre les deux branches possibles à chaque étape clé._

**_Deuxième DSS — le parcours livreur._**
_On commence par une boucle de transmission GPS toutes les 30 secondes. Tant que le livreur est disponible, sa position est envoyée._

- _Un **opt** vérifie si un colis est dans le rayon de 3 km_
- _Un **alt** gère l'acceptation ou le refus avec le timeout de 60 secondes_
- _Un **alt** gère le scan du QR : soit il est lisible, soit on passe en saisie manuelle_

_Tous ces fragments combinés sont obligatoires dans le cadre du cours pour montrer la maîtrise des concepts UML._

_Je passe la parole à [Prénom Intervenant 3] pour la partie UI et code."_

---

## Slide 7 — Maquettes UI (Intervenant 3)

**⏱ ~2 min**

> _"Merci. Passons à la partie concrète : les maquettes d'interface._

_Nous avons réalisé **deux écrans stratégiques**, chacun avec son scénario nominal et son scénario d'exception._

**_Première maquette — l'interface web expéditeur._**
_À gauche : le formulaire de demande de livraison rempli, avec le **devis calculé** : 10,30 € et 570g de CO₂ économisés. On voit les champs d'adresse, les dimensions, le choix Standard/Express._

_À droite : le **scénario d'exception** — le paiement a été refusé. On affiche une alerte rouge avec le statut VERROUILLEE_FRAUDE et le bouton "Modifier mon moyen de paiement" pour redonner le contrôle à l'utilisateur._

**_Deuxième maquette — l'application mobile livreur._**
_À gauche : la notification de mission avec le compte à rebours à 47 secondes, les détails du colis, et les boutons Accepter/Refuser. En dessous, le scan QR Code._

_À droite : le **scénario d'exception** — le QR Code est illisible. On propose la **procédure de secours** : la saisie manuelle du code à 12 caractères, ici GR-7F3D-A2B9._

_Ces maquettes sont interactives — ouvrez les fichiers HTML dans un navigateur."_

---

## Slide 8 — Critères Bastien & Scapin (Intervenant 3)

**⏱ ~1 min**

> _"Pour valider la qualité ergonomique de nos maquettes, nous avons appliqué les **8 critères de Bastien & Scapin**._

_Je vais souligner les plus importants :_

- _**Guidage** : libellés explicites, code couleur vert/rouge, messages d'erreur avec actions possibles_
- _**Charge de travail réduite** : le niveau Standard est présélectionné, le scan QR évite la frappe_
- _**Gestion des erreurs** : c'est le point fort — QR illisible → saisie manuelle, paiement refusé → changer de carte, perte réseau → cache local_
- _**Contrôle utilisateur** : l'utilisateur peut toujours annuler, revenir en arrière, ou modifier ses choix_

_Tous les détails sont dans le DAF avec des exemples concrets pour chaque critère."_

---

## Slide 9 — Implémentation Python (Intervenant 3)

**⏱ ~2 min**

> _"Enfin, la partie code — l'implémentation Python du modèle._

_Nous avons **13 fichiers** structurés en deux packages : model et services._

_Le respect de l'**encapsulation** est strict :_

- _Tous les attributs sont privés (préfixe `_`)_
- _Tous les getters passent par `@property`_
- _Les setters sont réservés aux seules mutations autorisées_

_Les IDs sont des **UUID** — pas d'auto-incrément qui pose problème en production._

_Le **moteur d'attribution** utilise une approximation de la formule de **Haversine** pour calculer les distances entre les positions GPS et trouver le livreur le plus proche dans un rayon de 3 km._

_La **démonstration complète** est dans `main.py`. Elle exécute le scénario de bout en bout — de la création du client à la livraison avec scan QR — et affiche toutes les transitions de statut. Nous avons vérifié : **0 erreur de diagnostic**, le code tourne parfaitement._

_Tout le code est sur le dépôt GitHub : **github.com/cleeryy/GreenRoute-UML**"_

---

## Slide 10 — Répartition & Barème (Tous)

**⏱ ~1 min**

> _[Intervenant 1] : "Nous avons réparti le travail de manière équitable : cadrage et besoins pour moi, architecture pour [Prénom 2], UI et code pour [Prénom 3]."_

> _[Intervenant 2] : "Le barème se décompose ainsi : 4 points pour les besoins, 5 pour l'architecture, 5 pour l'IHM et le code, et 6 points pour la qualité du livrable et la soutenance."_

> _[Intervenant 3] : "Nous sommes prêts pour vos questions. Nous avons préparé des réponses sur les choix techniques, la résilience, et les mesures d'impact écologique."_

---

## Slide 11 — Questions / Réponses (Tous)

**⏱ 10 min**

### Questions potentielles et éléments de réponse

**Q : Pourquoi avoir choisi Python plutôt qu'un autre langage ?**
> Python permet une modélisation rapide et propre des concepts OOP. La syntaxe est lisible, ce qui est appréciable pour un projet académique où la clarté du code compte. Les propriétés `@property` rendent l'encapsulation élégante.

**Q : Comment le moteur d'attribution gère-t-il la montée en charge ?**
> Pour une version production, on pourrait passer à une file Redis avec géolocalisation en temps réel. La version actuelle avec Haversine est fonctionnelle pour un pilote à l'échelle toulousaine.

**Q : Comment garantissez-vous l'intégrité des données hors-ligne ?**
> Le cache local est chiffré sur le smartphone. Au retour du réseau, une synchronisation bidirectionnelle vérifie l'état des commandes avant mise à jour. En cas de conflit, le serveur central fait autorité.

**Q : Quelle est la différence entre un include et un extend dans vos diagrammes ?**
> L'include est obligatoire — on ne peut pas commander sans être authentifié. L'extend est optionnel et conditionnel — la saisie manuelle du code n'est proposée que si le scan échoue. C'est une extension du cas principal.

**Q : Comment avez-vous calculé l'empreinte carbone ?**
> On part d'une référence : un véhicule diesel standard émet environ 150g de CO₂ par km. Un vélo cargo ou triporteur : 0g. L'économie est donc de 150g × distance en km. Pour un trajet de 5 km, ça donne 750g de CO₂ évités.

**Q : Pourquoi le statut VERROUILLEE_FRAUDE plutôt que simplement "Annulé" ?**
> Ce statut déclenche des procédures spécifiques : blocage de la commande, notification au client, et traçabilité pour la conformité financière. "Annulé" serait trop vague et ne permettrait pas le suivi nécessaire.

**Q : Quels sont les points d'amélioration pour une V2 ?**
> Version 2 pourrait inclure : optimisation des tournées multi-colis, scoring des livreurs, dashboard analytics pour la métropole, et application web destinataire avec suivi en temps réel.

**Q : Concrètement, comment se passe l'attribution d'un colis ?**
> Le livreur déclare sa disponibilité, son GPS est transmis toutes les 30 secondes. Le moteur analyse la file d'attente des commandes A_ATTRIBUER. Dès qu'un colis est dans un rayon de 3 km, une notification est envoyée au livreur. Il a 60 secondes pour accepter. Si oui, la commande est verrouillée pour lui et une feuille de route est générée via ToulouseMap.

---

## Rappel : Structure des slides

| Slide | Titre | Qui |
|---|---|---|
| 1 | Accueil — GreenRoute | Intervenant 1 |
| 2 | Problématique & Vision | Intervenant 1 |
| 3 | Périmètre fonctionnel | Intervenant 1 |
| 4 | Descriptions textuelles | Intervenant 1 |
| 5 | Diagramme de classes | Intervenant 2 |
| 6 | DSS | Intervenant 2 |
| 7 | Maquettes UI | Intervenant 3 |
| 8 | Critères Bastien & Scapin | Intervenant 3 |
| 9 | Implémentation Python | Intervenant 3 |
| 10 | Répartition & Barème | Tous |
| 11 | Q&A | Tous |

---

_Bonne soutenance ! 🎯_
