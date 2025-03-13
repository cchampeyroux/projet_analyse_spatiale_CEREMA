# projet_analyse_spatiale_CEREMA

**Etapes du traitement :**  
1. Détecter les discontinuités le long des routes  
2. Prioriser les replantations en fonctions des espaces protégés  
3. Hiérarchiser en fonction des pentes (ruissellement)

## 1. Sélection des discontinuités dans les haies
### Découpage des routes en segments de 5 mètres
La première étape consiste à diviser l’ensemble du réseau de routes départementales du département de la Manche en segments de 5 mètres. Ce découpage permet d’analyser précisément la présence ou l’absence de haies sur de très courtes distances, garantissant ainsi une meilleure finesse d’interprétation des résultats. Cette étape est effectuée avec la fonction ***Division des lignes par longueur maximale*** de QGIS en choisissant 5 mètres pour longueur et la couche des routes départementales en entrée.

