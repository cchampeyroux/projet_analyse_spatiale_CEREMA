import os
import subprocess
import grass.script as gs

# Définir le dossier contenant les tuiles MNT et celui contenant les résultats
mnt_folder = r"chemin\dossier\dalles\mnt"
output_folder = r"chemin\dossier\sortie\accumulation"

print("Traitement des tuiles du dossier...")

# Lister tous les fichiers .asc du dossier
mnt_files = [f for f in os.listdir(mnt_folder) if f.endswith(".asc")]

for mnt_file in mnt_files:
    mnt_path = os.path.join(mnt_folder, mnt_file)
    print(f"Traitement de la tuile : {mnt_file}")

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
    mnt_raster_name = os.path.splitext(mnt_file)[0]  # Nom basé sur le fichier
    gs.run_command("r.in.gdal", input=mnt_path, output=mnt_raster_name, overwrite=True, flags="o")

    # Fixer la région sur le raster importé
    gs.run_command("g.region", raster=mnt_raster_name)

    # Vérification des données importées
    print("Statistiques de la tuile:")
    gs.run_command("r.stats", flags="n", input=mnt_raster_name)
    gs.run_command("r.info", map=mnt_raster_name)  # Vérification des informations sur le raster

    # Exécution de r.flow pour récupérer l'accumulation
    flow_accum_raster_name = f"flow_accum_{mnt_raster_name}"
    gs.run_command("r.flow", elevation=mnt_raster_name, flowaccumulation=flow_accum_raster_name, overwrite=True)

    # Vérification de l'accumulation de flux
    gs.run_command("r.stats", flags="n", input=flow_accum_raster_name)

    # Exportation du résultat
    output_path = os.path.join(output_folder, f"flow_acc_{mnt_raster_name}.asc")
    gs.run_command("r.out.gdal", input=flow_accum_raster_name, output=output_path,
                   format="GTiff", type="Float64", overwrite=True)

    # Nettoyage des données temporaires
    gs.run_command("g.remove", type="raster", name=mnt_raster_name, flags="f")
    gs.run_command("g.remove", type="raster", name=flow_accum_raster_name, flags="f")

    print(f"Traitement terminé pour {mnt_file} !")

# Vérifier la liste des rasters restants
gs.run_command("g.list", type="raster")

print("Traitement de toutes les tuiles terminé !")
