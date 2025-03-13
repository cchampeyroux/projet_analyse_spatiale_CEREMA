# projet_analyse_spatiale_CEREMA

**Etapes du traitement :**  
1. Détecter les discontinuités le long des routes  
2. Prioriser les replantations en fonctions des espaces protégés  
3. Hiérarchiser en fonction des pentes (ruissellement)

## 1. Sélection des discontinuités dans les haies
### Découpage des routes en segments de 5 mètres
La première étape consiste à diviser l’ensemble du réseau de routes départementales du département de la Manche en segments de 5 mètres. Ce découpage permet d’analyser précisément la présence ou l’absence de haies sur de très courtes distances, garantissant ainsi une meilleure finesse d’interprétation des résultats. Cette étape est effectuée avec la fonction ***Division des lignes par longueur maximale*** de QGIS en choisissant 5 mètres pour longueur et la couche des routes départementales en entrée.

### Création d’une zone tampon de 20 mètres
Autour de chaque segment de 5 mètres, une zone tampon d’un rayon de 20 mètres est générée. Cette zone permet d’englober les haies situées à proximité immédiate de la route et d’assurer une précision d’analyse à 5 mètres près. Cette étape a été réalisée grâce à la requête SQL suivante :
```
CREATE TABLE buffer_haie AS (
    SELECT (ST_Dump(ST_Difference(ST_Buffer(r1.geom, 20), r2.geom))).geom AS geom
    FROM cd50_coupe100 r1
    JOIN cd50_coupe100 r2 ON ST_Intersects(ST_Buffer(r1.geom, 20), r2.geom)
);
```
et à la fonction ***Couper avec des lignes*** de QGIS avec les zones tampon en couche source et les routes départementales non découpées en couche de découpage.
