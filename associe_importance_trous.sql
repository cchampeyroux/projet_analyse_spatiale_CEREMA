--- Affecte aux discintinuités de haies, la valeur maximale d'importance
--selon dans quel espace protégé ou réservoir elle se trouve
DROP TABLE IF EXISTS trou_parcelles_espaces_proteges_reservoirs;
CREATE TABLE trou_parcelles_espaces_proteges_reservoirs AS
SELECT 
    t.id AS id, 
    t.geom, 
    COALESCE(MAX(e.importance), 0) AS importance  -- Prend la valeur max ou 0 si aucun recouvrement
FROM trou_5m_sans_route_et_parcelle AS t
LEFT JOIN espaces_proteges_et_reservoirs AS e 
ON ST_Intersects(t.geom, e.geom)  -- Vérifie si un espace protégé recouvre le polygone trou
GROUP BY t.id, t.geom;
/*

DROP TABLE IF EXISTS trou_espaces_proteges_reservoirs;
CREATE TABLE trou_espaces_proteges_reservoirs AS
SELECT 
    t.id AS id, 
    t.geom, 
    COALESCE(MAX(e.importance), 0) AS importance  -- Prend la valeur max ou 0 si aucun recouvrement
FROM trou_5m_sans_route_split_final AS t
LEFT JOIN espaces_proteges_et_reservoirs AS e 
ON ST_Intersects(t.geom, e.geom)  -- Vérifie si un espace protégé recouvre le polygone trou
GROUP BY t.id, t.geom;
*/