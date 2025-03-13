

---Attribution d'une pondération à chaque type d'espace
CREATE TABLE priorites (
    type VARCHAR,
    importance INTEGER
);


INSERT INTO priorites (type, importance) VALUES
('rncfs', 10),
('rnn', 10),
('rnr', 10),
('zps', 9),
('sic', 9),
('ramsar', 8),
('bios', 8),
('apb', 7),
('aphn', 7),
('bpm', 7),
('pnr', 6),
('znieff1', 6),
('znieff2', 4),
('cen', 4),
('cdl', 3),
('ospar', 3),
('ens', 4);



---Jointure des couches avec leurs scores pour avoir la geometrie et la pondération dans espaces pondérés
DROP TABLE if exists espaces_pondere;
SELECT 
    e.id AS espace_id,
    p.importance,
	e.type,
    e.geom
INTO espaces_pondere
FROM espaces_proteges50 e
JOIN priorites p ON e.type = p.type;

---Decouper pour garder ceux dans la manche

DROP TABLE if exists espaces_ponderes50;

CREATE TABLE espaces_ponderes50 AS
SELECT 
    ep.espace_id AS espace_id, 
	ep.importance,-- ID de l'espace protégé
    ep.type,
    ST_Intersection(ep.geom, d.geom) AS geom
FROM 
    espaces_pondere as ep, manche2154 as d



