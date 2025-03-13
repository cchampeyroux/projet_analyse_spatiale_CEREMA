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











## 2. Hiérarchisation des zones avec les espaces protégés et réservoirs de biodiversité

Reprojection et harmonisation des couches d'espaces protégés en 2154 pour rendre les données homogènes.
- **`creation_espaces_prot.sql`** : Regroupe l’ensemble des espaces protégés dans une même couche, en précisant leur type en attribut, et effectue un découpage par le département de la Manche.  
- **`importance.sql`** : Associe une valeur d’importance aux espaces protégés.  
- **`réservoirs.sql`** : Crée une nouvelle couche combinant les espaces protégés et les réservoirs, en leur attribuant une valeur d’importance sur 10.  
- **`associe_importance_trous.sql`** : Affecte aux discontinuités de haies la valeur maximale d’importance, en fonction de l’espace protégé ou du réservoir dans lequel elles se trouvent. 

## 3.Étude sur les pentes des terrains agricoles en bordure de route


## 4. Identification des zones prioritaires pour la plantation de haies avec les critères écologiques et hydrologiques

- Jointure des couches de bords de route sans haie avec les données d'importance de zones protégées et les données de ruissellement créant la couche "trou_flux_et_proteges".
- Normalisation des indices d'importance écologique (attribut : "importance") et d'écoulement (attribut : "ecoulement"), donne les résultats dans l'attribut : "norm_prot" et "norm_ecoul"
- Pondération pour créer un indice global de priorité : Priorité = (écoulement normalisé × 0.5) + (importance espaces normalisée × 0.5), attribut : "param50_50"
