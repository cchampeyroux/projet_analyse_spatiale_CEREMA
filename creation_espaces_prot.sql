

DROP TABLE IF EXISTS espaces_proteges;

-- Créer la table espaces_proteges
CREATE TABLE espaces_proteges(
    id SERIAL PRIMARY KEY,
    geom Geometry(MultiPolygon, 2154),
    type VARCHAR,
    importance INTEGER
);

-- Boucle pour insérer les données des différentes tables
DO $$ 
DECLARE 
    table_name TEXT;
BEGIN
    FOR table_name IN 
        SELECT unnest(ARRAY['apb', 'aphn', 'bios', 'bpm', 'cdl', 'cen', 'ens', 'ospar', 'pnr', 'ramsar', 'rb', 'rncfs', 'rnn', 'rnr', 'sic', 'znieff1', 'znieff2', 'zps'])
    LOOP
        -- Exécution de l'insertion des données
        EXECUTE format(
            'INSERT INTO espaces_proteges (geom, type, importance)
             SELECT geom, %L AS type, NULL 
             FROM %I
             WHERE geom IS NOT NULL', 
             table_name, table_name
        );
    END LOOP;
END $$;

-- Création de la table espaces_proteges50bis avec découpage sur le département de la Manche
DROP TABLE IF EXISTS espaces_proteges50bis;
CREATE TABLE espaces_proteges50bis AS
SELECT 
    e.id, 
    ST_Intersection(e.geom, m.geom) AS geom,  -- Découpage des espaces protégés selon la Manche
    e.type, 
    e.importance
FROM espaces_proteges AS e
JOIN manche2154 AS m 
ON ST_Intersects(e.geom, m.geom)
WHERE ST_Intersection(e.geom, m.geom) IS NOT NULL;


