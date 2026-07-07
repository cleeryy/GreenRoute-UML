## **EXAMEN FINAL : PROJET AVEC SOUTENANCE ORALE** 

**Cours :** ESGI - Modélisation UML2 

**Année scolaire:** 2025-2026 

**Modalité :** Travail en groupe de 3 ou 4 étudiants 

**Livrable attendu :** Dossier PDF, code source et maquettes d’IHM. A envoyer par retour de mail au plus tard le 09 juillet 2026 à 23H59 en mettant en copie tous les étudiants du groupe. 

## **PROJET & CONTEXTE OPÉRATIONNEL** 

## **1. Genèse du projet et vision stratégique** 

La start-up _GreenRoute_ vient de remporter un important appel d’offres auprès de la métropole de Toulouse pour fluidifier et décarboner les livraisons du “dernier kilomètre” en centre-ville. Le constat de départ est simple : les camionnettes thermiques traditionnelles saturent l’espace urbain et génèrent une pollution atmosphérique majeure. 

_GreenRoute_ se positionne comme un intermédiaire technologique éco-responsable. L’entreprise s’appuie sur une flotte de livreurs indépendants utilisant exclusivement des modes de transport doux (vélos-cargos, triporteurs, et petites camionnettes électriques). L’objectif est de concevoir une plateforme logicielle complète capable d’orchestrer les demandes des expéditeurs, de répartir intelligemment la charge de travail entre les livreurs, et de prouver scientifiquement l’impact écologique de chaque trajet. 

## **2. Description détaillée des flux et des processus métiers** 

## **A. Le parcours de l’Expéditeur (espace client)** 

Tout commence lorsqu’un client (une boutique locale, un e-commerçant ou un particulier) souhaite expédier une marchandise. Pour accéder aux services, le client doit obligatoirement s’authentifier sur la plateforme web de GreenRoute. Une fois connecté, il accède à un tableau de bord lui permettant d’initier une demande de prise en charge. 

Le client doit obligatoirement renseigner les informations suivantes : 

- L’adresse physique complète de collecte (départ). 

- L’adresse physique complète de destination (arrivée). 

- Les caractéristiques physiques du colis : son poids précis (en kg) et ses dimensions (longueur, largeur, hauteur en cm) afin d’éviter la surcharge des vélos-cargos. Le niveau d’urgence de la livraison : **Standard** (livraison sous 24 heures) ou **Express** (livraison requise dans les 2 heures). 

Dès que ces informations sont saisies, le système interagit en tâche de fond avec ToulouseMap, une API de cartographie pour évaluer la distance réelle et la faisabilité du trajet. Le système calcule alors instantanément deux indicateurs clés pour le client : 

1. Le **coût financier de la prestation** , calculé selon une règle stricte : un tarif de base fixe indexé sur le poids, auquel s’ajoute un coût kilométrique dépendant de la distance et une majoration de 30% si le niveau d’urgence est configuré en _Express_ . 

2. L’ **empreinte carbone économisée** (exprimée en grammes de CO₂), calculée par différentiel par rapport à un trajet équivalent effectué par un véhicule diesel thermique standard. 

Si le client valide le devis, il est redirigé vers un module de paiement sécurisé en ligne. 

- **Scénario nominal :** Le paiement est accepté par la banque externe. La commande est enregistrée avec le statut A_ATTRIBUER , et un ticket d’expédition contenant un identifiant unique et un **QR Code de traçabilité** est généré automatiquement. Le client peut alors imprimer ce document pour le coller sur le colis. **Scénario d’exception :** Si la transaction financière échoue (fonds insuffisants, rejet de la banque…), le système suspend immédiatement le processus, la commande est créée sous le statut VERROUILLEE_FRAUDE et un message clair invite le client à modifier son moyen de paiement. 

## **B. La dynamique opérationnelle des Livreurs (application mobile)** 

Les livreurs en circulation gèrent leur activité directement via une application mobile dédiée. Après s’être connectés de manière sécurisée, ils doivent déclarer leur état de disponibilité à l’aide d’un commutateur logique ( Disponible ou En Tournée ). 

Lorsqu’un livreur se déclare Disponible , son smartphone transmet à intervalles réguliers (toutes les 30 secondes) ses coordonnées géographiques précises (Latitude / 

Longitude) au système central de GreenRoute. Le moteur d’attribution de la plateforme analyse alors la file d’attente des commandes au statut A_ATTRIBUER . Dès qu’un colis se trouve dans un rayon d’action de moins de 3 kilomètres autour de la position actuelle du livreur, une notification contextuelle apparaît sur son écran, détaillant le type de colis, le volume, et la distance à parcourir. 

Le livreur dispose d’un compte à rebours de 60 secondes pour réagir : 

- S’il **refuse** la proposition ou si le chrono expire, le colis est immédiatement 

- proposé à un autre livreur à proximité. 

- S’il **accepte** , le statut de la commande bascule instantanément à 

- EN_COURS_D_ATTRIBUTION . Le système verrouille temporairement le colis pour 

- ce livreur et sollicite l’API cartographique externe pour générer une feuille de route optimisée, privilégiant les pistes cyclables. 

Le livreur se rend au point de collecte initial pour récupérer physiquement la marchandise auprès de l’expéditeur. Lorsqu’il prend possession du colis, il valide la collecte sur son application : le statut de la commande bascule alors à 

**EN_COURS_DE_LIVRAISON** et le livreur passe en état En Tournée . L’application affiche l’itinéraire en temps réel jusqu’au point de destination finale. 

Une fois face au destinataire final, pour prouver la bonne exécution de sa mission, le livreur doit obligatoirement utiliser l’appareil photo de son smartphone pour scanner le **QR Code** imprimé sur le colis. 

- Si le scan est validé par le système, la commande passe définitivement au statut LIVRE . L’application affiche un récapitulatif du trajet et le livreur repasse 

- automatiquement en statut Disponible . 

- Si le QR Code est physiquement endommagé ou illisible, l’application doit proposer une procédure de secours : la saisie manuelle du code alphanumérique unique à 12 caractères situé sous le graphique. 

## **3. Contraintes techniques, systèmes externes & résilience** 

## **A. Interactions avec les systèmes tierces** 

La plateforme GreenRoute ne peut pas fonctionner en autarcie. Elle s’appuie structurellement sur deux systèmes externes majeurs : 

1. **ToulouseMap, l’API de cartographie externe :** Ce système fournit le référentiel 

géographique mondial, calcule les distances réelles entre deux adresses, estime les 

temps de trajet en tenant compte du trafic des cycles et renvoie le tracé géométrique des itinéraires sous forme de coordonnées vectorielles. 

2. **ToulousePay, la passerelle de paiement bancaire :** Un service hautement sécurisé chargé de valider ou rejeter les transactions par carte bancaire ou portefeuille virtuel. 

## **B. Exigences non fonctionnelles et résilience** 

En tant qu’application critique pour la logistique urbaine, GreenRoute doit respecter des indicateurs de performance stricts : 

- **Performance algorithmique :** Le moteur de calcul d’itinéraire et d’optimisation des tournées doit renvoyer une réponse à l’interface en **moins de 2 secondes** , même en cas de forte charge réseau. 

- **Résilience et tolérance aux pannes :** En fin de journée ou lors des pics de livraison, les réseaux mobiles en centre-ville peuvent saturer, entraînant des pertes de connexion momentanées pour les livreurs. Si l’application mobile du livreur ne capte plus de réseau au moment du scan final du QR Code, le système doit être capable de stocker temporairement l’événement de livraison dans un **cache local chiffré** sur le smartphone. Dès que le réseau est restauré, l’application doit synchroniser les données en tâche de fond avec le serveur central pour mettre à jour le statut du colis sans bloquer l’activité du livreur. 

## **LIVRABLES ATTENDUS** 

Le Dossier d’Analyse Fonctionnelle (DAF) doit être structuré de manière rigoureuse et professionnelle, sans omission. Il doit comporter : 

## **Bloc 1 : Ingénierie des besoins & spécifications** 

1. **Diagramme de contexte :** Délimitation claire des frontières de l’application, identification des acteurs humains et des systèmes externes, avec flèches légendées par la nature exacte des flux de données. 

2. **Diagramme de cas d’utilisation :** Vue d’ensemble du périmètre fonctionnel. Contraintes : utilisation formalisée et justifiée d’au moins une relation d’inclusion et d’une relation d’extension. 

3. **Descriptions textuelles détaillées :** Rédaction exhaustive des **deux cas** 

   - **d’utilisation principaux** décrits dans l’énoncé. Le rendu doit respecter le gabarit standard : identifiant, acteurs, préconditions, postconditions, scénario nominal étape par étape et scénarios alternatifs/exceptions. 

## **Bloc 2 : Architecture des données & dynamique** 

4. **Diagramme de classes d’analyse :** Modélisation conceptuelle des entités du domaine. Sont attendus : les attributs typés, le respect de l’encapsulation, les multiplicités exactes sur les associations, et l’usage documenté des concepts avancés (composition, héritage si pertinent, classes d’énumérations…). 

5. **Diagrammes de séquence système (DSS) :** Conception de deux DSS modélisant la dimension temporelle des deux cas d’utilisation rédigés au Bloc 1. Le système doit être traité comme une **boîte noire** . Usage obligatoire des fragments combinés ( alt pour les choix conditionnels, loop pour la gestion des saisies répétitives, opt pour les actions facultatives). 

## **Bloc 3 : Interface utilisateur (Maquettage)** 

6. **Maquettes UI :** Réalisation des wireframes ou mockups de **deux écrans stratégiques** de l’application. Les maquettes doivent illustrer l’agencement visuel lors du scénario nominal mais également lors du déclenchement d’un scénario d’exception (affichage d’une alerte ou d’un message d’erreur ergonomique). Le respect des critères de Bastien & Scapin doit être argumenté. 

## **Bloc 4 : Implémentation technique (Code OOP)** 

7. **Code source du modèle :** Traduction stricte du diagramme de classes d’analyse dans le langage orienté objet au choix du groupe (Java, Python, PHP, C#…). L’encapsulation doit être rigoureusement implémentée (propriétés privées, getters/setters ou constructeurs adéquats). Les relations un-à-plusieurs doivent être matérialisées par des structures de collections adaptées (listes, tableaux, map…). _Note : Aucun code d’IHM graphique ni de requêtes de base de données (SQL/NoSQL) n’est demandé dans ce bloc ; seul le modèle métier est évalué._ 

## **BARÈME DE CORRECTION (sur 20 points)** 

|**Composant évalué**|**Critères d’évaluation**|**Points**|
|---|---|---|
|**Ingénierie des**<br>**besoins (Bloc 1)**|Justesse du diagramme de contexte et sens des fux.<br>Rigueur syntaxique du diagramme de cas d’utilisation<br>(frontière, acteurs externes). Absence de jargon<br>d’implémentation technique ou graphique dans les<br>scénarios textuels.|**/ 4 pts**|



|**Architecture &**<br>**dynamique (Bloc 2)**|Cohérence du diagramme de classes (multiplicités<br>logiques, distinction composition vs association<br>simple, présence du cycle de statuts complet). Syntaxe<br>du DSS (lignes de vie acteur/système, nommage des<br>messages avec arguments, positionnement des<br>gardes).|**/ 5 pts**|
|---|---|---|
|**IHM &**<br>**implémentation**<br>**(Blocs 3 & 4)**|Application des critères d’ergonomie sur les<br>maquettes (guidage, charge de travail réduite). Fidélité<br>et propreté du code source orienté objet par rapport<br>aux types et relations du diagramme de classes.|**/ 5 pts**|
|**Qualité du livrable**<br>**(Forme & Bonus)**|Structure générale du document d’analyse, présence<br>d’un glossaire métier et qualité du document (les<br>éléments des diagrammes se répondent<br>mutuellement).|**/ 2 pts**|
|**Soutenance orale**<br>**& posture**|Clarté et dynamisme du pitch, qualité des supports<br>visuels projetés, répartition équitable du temps de<br>parole au sein du groupe et qualité des réponses aux<br>questions (5 min).|**/ 4 pts**|



## **MODALITÉS DE LA SOUTENANCE ORALE (30 min)** 

La soutenance se déroule dans les conditions réelles d’une **revue d’architecture technique** (Design Review) devant un comité de direction de l’ingénierie logicielle. 

## **Présentation (20 min) Session de Questions / Réponses (1O min)** 

