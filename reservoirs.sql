
DROP TABLE if exists reservoirs;
CREATE TABLE reservoirs(
    id SERIAL PRIMARY KEY,
    geom Geometry(MultiPolygon, 2154),
    type VARCHAR,
    importance INTEGER
);

---Convertir la couche lineaire des cours d'eau en polygone
CREATE TABLE reservoir_cours_eau_polygone AS
SELECT 
    ce.id, 
    ST_Multi(ST_Buffer(ce.geom, 5)) AS geom, 
    'cours_eau' AS type, 
    10 AS importance
FROM reservoirs_courseau as ce
JOIN manche2154 d ON ST_Intersects(ce.geom, d.geom);



INSERT INTO reservoirs (geom, type, importance)
SELECT ST_Multi(ST_CollectionExtract(geom, 3)), 'reservoirs littoraux', 10 FROM reservoirs_littoraux
UNION ALL
SELECT ST_Multi(ST_CollectionExtract(geom, 3)), 'reservoirs cours_eau', 10 FROM reservoir_cours_eau_polygone
UNION ALL
SELECT ST_Multi(ST_CollectionExtract(geom, 3)), 'reservoirs boises', 10 FROM reservoirs_boises
UNION ALL
SELECT ST_Multi(ST_CollectionExtract(geom, 3)), 'reservoirs boises et ouverts', 10 FROM reservoirs_boises_ouverts_corr
UNION ALL
SELECT ST_Multi(ST_CollectionExtract(geom, 3)), 'reservoirs milieux ouverts', 10 FROM reservoirs_milieux_ouverts
UNION ALL
SELECT ST_Multi(ST_CollectionExtract(geom, 3)), 'reservoirs zones humides', 10 FROM reservoirs_zones_humides;


DROP TABLE if exists reservoirs_50;
CREATE TABLE reservoirs_50 AS
SELECT 
    r.id, 
    ST_Intersection(r.geom, d.geom) AS geom, 
    r.type, 
    r.importance
FROM reservoirs r
JOIN manche2154 d ON ST_Intersects(r.geom, d.geom);





CREATE TABLE espaces_proteges_et_reservoirs(
    id SERIAL PRIMARY KEY,
    geom Geometry(MultiPolygon, 2154),
    type VARCHAR,
    importance INTEGER
	);
	
INSERT INTO espaces_proteges_et_reservoirs (geom, type, importance)
SELECT ST_Multi(ST_CollectionExtract(geom, 3)), type, importance FROM reservoirs_50
UNION ALL
SELECT ST_Multi(ST_CollectionExtract(geom, 3)), type, importance FROM espaces_proteges_importance_final
