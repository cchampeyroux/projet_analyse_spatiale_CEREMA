#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 18:37:58 2025

@author: formation
"""



import os
import geopandas as gpd
import rasterio
import multiprocessing
from rasterio.mask import mask
from shapely.geometry import shape
from tqdm import tqdm
from rtree import index  # Utilisation d'un index spatial pour accélérer les intersections

# Chemins des fichiers
dossier_flux = "/media/formation/T7 Shield/ENSG/IGAST/Haies/flux_trie"  # Nouveau dossier contenant les fichiers TIFF
fichier_trous = "/media/formation/JEANNE/trou_5m_parcelles/trou_5m_sans_route_et_parcelle.shp"
fichier_sortie = "/media/formation/JEANNE/trou_intersecte_flux_attribut_plus_haut_pixel/trous_intersecte_flux.shp"

# Charger les trous et créer un index spatial
trous = gpd.read_file(fichier_trous)
spatial_index = index.Index()
for i, geom in enumerate(trous.geometry):
    if geom and not geom.is_empty and geom.is_valid:
        spatial_index.insert(i, geom.bounds)

# Récupérer tous les fichiers TIFF du dossier flux
fichiers_tiff = [os.path.join(dossier_flux, f) for f in os.listdir(dossier_flux) if f.endswith(".tif")]

# Seuils à tester
seuils = [i for i in range(0, 7001, 10)]

# Fonction pour traiter un seul fichier TIFF (avec lecture par blocs)
def traiter_tiff(chemin_tiff):
    geometries_valides = {}

    with rasterio.open(chemin_tiff) as src:
        bounds = src.bounds  # 🔍 Récupérer les limites du raster
        
        # Sélectionner uniquement les trous qui intersectent ce raster
        indices_potentiels = list(spatial_index.intersection((bounds.left, bounds.bottom, bounds.right, bounds.top)))
        trous_filtres = trous.iloc[indices_potentiels]
        
        # Parcourir les trous sélectionnés
        for _, row in trous_filtres.iterrows():
            geom = row.geometry
            if geom.is_empty or not geom.is_valid:
                continue
            
            try:
                # Lire seulement la zone concernée du raster (évite de charger tout le fichier)
                image, transform = mask(src, [geom], crop=True)
                
                # Trouver le seuil le plus élevé atteint
                seuil_max = None
                for seuil in seuils:
                    if (image >= seuil).any():
                        seuil_max = seuil
                
                if seuil_max is not None:
                    geometries_valides[geom.wkt] = (geom, seuil_max)
            except Exception as e:
                print(f"Problème avec un trou : {e}")
    
    return list(geometries_valides.values())

# Exécution en parallèle avec multiprocessing
if __name__ == "__main__":
    with multiprocessing.Pool(processes=os.cpu_count()) as pool:
        resultats = list(tqdm(pool.imap(traiter_tiff, fichiers_tiff), total=len(fichiers_tiff), desc="Traitement en parallèle", unit="tiff"))

    # Fusionner tous les résultats
    geometries_conservees = {}
    for sublist in resultats:
        for geom, seuil in sublist:
            if geom.wkt not in geometries_conservees or seuil > geometries_conservees[geom.wkt][1]:
                geometries_conservees[geom.wkt] = (geom, seuil)

    # Sauvegarde des résultats
    if geometries_conservees:
        gdf_resultat = gpd.GeoDataFrame(
            list(geometries_conservees.values()),
            columns=["geometry", "seuil"],
            crs=trous.crs
        )
        gdf_resultat.to_file(fichier_sortie)
        print(f"\nFichier sauvegardé : {fichier_sortie}")
    else:
        print("\nAucun trou ne correspond aux pixels des seuils donnés dans les rasters de 'flux'")