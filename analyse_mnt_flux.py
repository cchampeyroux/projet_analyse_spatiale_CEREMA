# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 12:00:43 2025

@author: Formation
"""


import os
import subprocess
import grass.script as gs

# Définir le chemin vers les tuiles MNT
mnt_path = r"C:\Users\bouna\Desktop\Etudes\ING3\Projet_Analyse_Spatiale\ruissellement\avec1image\RGEALTI_FXX_0388_6905_MNT_LAMB93_IGN69.asc"
output_folder = r"C:\Users\bouna\Desktop\Etudes\ING3\Projet_Analyse_Spatiale\ruissellement\avec1image\flux"

print("Traitement de la tuile")

# Vérifier si le fichier a une projection définie
print("Vérification de la projection du fichier MNT...")
cmd_gdalinfo = ["gdalinfo", mnt_path]
process = subprocess.run(cmd_gdalinfo, capture_output=True, text=True)

if "No SRS" in process.stdout or "Unknown projection" in process.stdout:
    print("Aucune projection trouvée, assignation de EPSG:2154...")
    subprocess.run(["gdal_edit.py", "-a_srs", "EPSG:2154", mnt_path])
else:
    print("Projection détectée, aucune modification nécessaire.")

# Vérifier la projection actuelle de la location GRASS
print("Projection actuelle de la location GRASS :")
gs.run_command("g.proj", flags="p")

# Importation de la tuile dans GRASS
mnt_raster_name = "mnt_tmp"  # Nom temporaire pour éviter les conflits
gs.run_command("r.in.gdal", input=mnt_path, output=mnt_raster_name, overwrite=True, flags="o")

# Fixer la région sur le raster importé
gs.run_command("g.region", raster=mnt_raster_name)

# Vérification des données importées
print("Statistiques de la tuile:")
gs.run_command("r.stats", flags="n", input=mnt_raster_name)
gs.run_command("r.info", map=mnt_raster_name)  # Vérification des informations sur le raster

# Exécution de r.flow pour récupérer l'accumulation
flow_accum_raster_name = "flow_accum_tmp"
gs.run_command("r.flow", elevation=mnt_raster_name, flowaccumulation=flow_accum_raster_name, overwrite=True)

# Vérification de l'accumulation de flux
gs.run_command("r.stats", flags="n", input=flow_accum_raster_name)

# Exportation du résultat
output_path = os.path.join(output_folder, "flow_acc_RGEALTI_FXX_0388_6905_MNT_LAMB93_IGN69.asc")
gs.run_command("r.out.gdal", input=flow_accum_raster_name, output=output_path,
               format="GTiff", type="Float64", overwrite=True)

# Nettoyage des données temporaires
gs.run_command("g.remove", type="raster", name=mnt_raster_name, flags="f")
gs.run_command("g.remove", type="raster", name=flow_accum_raster_name, flags="f")

# Vérifier la liste des rasters
gs.run_command("g.list", type="raster")

print("Traitement terminé !")
