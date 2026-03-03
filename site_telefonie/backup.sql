-- PostgreSQL database dump
--

\restrict fyV4QQEuB5OxwRd1dgzdrLbPavAgPrIVhPcxPclJjlXtd3HkGjOYEvGO0ujqQUO

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: site_telefonie_produs; Type: TABLE DATA; Schema: django; Owner: ilinca
--

INSERT INTO django.site_telefonie_produs (id_produs, nume, pret) VALUES (5, 'TV Standard', 20.00);
INSERT INTO django.site_telefonie_produs (id_produs, nume, pret) VALUES (4, 'Internet Basic', 25.00);
INSERT INTO django.site_telefonie_produs (id_produs, nume, pret) VALUES (3, 'Telefonie Nelimitată', 15.00);
INSERT INTO django.site_telefonie_produs (id_produs, nume, pret) VALUES (2, 'TV Premium', 35.00);
INSERT INTO django.site_telefonie_produs (id_produs, nume, pret) VALUES (1, 'Internet Gigabit', 50.00);
INSERT INTO django.site_telefonie_produs (id_produs, nume, pret) VALUES (10, 'OnePlus 12', 3799.00);
INSERT INTO django.site_telefonie_produs (id_produs, nume, pret) VALUES (9, 'Xiaomi 14', 2999.00);
INSERT INTO django.site_telefonie_produs (id_produs, nume, pret) VALUES (8, 'Google Pixel 8', 3499.00);
INSERT INTO django.site_telefonie_produs (id_produs, nume, pret) VALUES (7, 'Samsung Galaxy S24', 4299.00);
INSERT INTO django.site_telefonie_produs (id_produs, nume, pret) VALUES (6, 'iPhone 15 Pro', 5499.00);
INSERT INTO django.site_telefonie_produs (id_produs, nume, pret) VALUES (11, 'ilinca', 28.00);


--
-- Name: site_telefonie_produs_id_produs_seq; Type: SEQUENCE SET; Schema: django; Owner: ilinca
--

SELECT pg_catalog.setval('django.site_telefonie_produs_id_produs_seq', 11, true);


--
-- PostgreSQL database dump complete
--

\unrestrict fyV4QQEuB5OxwRd1dgzdrLbPavAgPrIVhPcxPclJjlXtd3HkGjOYEvGO0ujqQUO

--
-- PostgreSQL database dump
--

\restrict H5HF1frrzqfBwSWCdY7kjD7bFg5wwDUtTh7w1chGy2Df5ANRN33Iqy4e1AWCo1s

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: site_telefonie_serviciu; Type: TABLE DATA; Schema: django; Owner: ilinca
--

INSERT INTO django.site_telefonie_serviciu (produs_ptr_id, id_serviciu, descriere_serviciu, imagine, tip, status, taxa_activare) VALUES (5, 5, '80 canale TV', 'servicii/istockphoto-1221240798-612x612.jpg', 'cablu', 'activ', 0.00);
INSERT INTO django.site_telefonie_serviciu (produs_ptr_id, id_serviciu, descriere_serviciu, imagine, tip, status, taxa_activare) VALUES (4, 4, 'Internet 300 Mbps', 'servicii/internet-banner.png', 'internet', 'activ', 0.00);
INSERT INTO django.site_telefonie_serviciu (produs_ptr_id, id_serviciu, descriere_serviciu, imagine, tip, status, taxa_activare) VALUES (3, 3, 'Minute nelimitate', 'servicii/collection-of-ringing-phones-vector.jpg', 'telefonie', 'activ', 0.00);
INSERT INTO django.site_telefonie_serviciu (produs_ptr_id, id_serviciu, descriere_serviciu, imagine, tip, status, taxa_activare) VALUES (2, 2, '150+ canale TV HD', 'servicii/microsite-buying-guide-2025-hub-02-feature-cta-d-4.avif', 'cablu', 'activ', 0.00);
INSERT INTO django.site_telefonie_serviciu (produs_ptr_id, id_serviciu, descriere_serviciu, imagine, tip, status, taxa_activare) VALUES (1, 1, 'Internet 1000 Mbps', 'servicii/gigabit-router.avif', 'internet', 'activ', 0.00);


--
-- Name: site_telefonie_serviciu_id_serviciu_seq; Type: SEQUENCE SET; Schema: django; Owner: ilinca
--

SELECT pg_catalog.setval('django.site_telefonie_serviciu_id_serviciu_seq', 5, true);


--
-- PostgreSQL database dump complete
--

\unrestrict H5HF1frrzqfBwSWCdY7kjD7bFg5wwDUtTh7w1chGy2Df5ANRN33Iqy4e1AWCo1s

--
-- PostgreSQL database dump
--

\restrict sVL4VGlUYNgOyPulOykm9z29norF62yhOb7f7K0uuzBmWGZjjoaKE5xCx0YrWsu

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: site_telefonie_telefon; Type: TABLE DATA; Schema: django; Owner: ilinca
--

INSERT INTO django.site_telefonie_telefon (produs_ptr_id, id_telefon, descriere_telefon, imagine, brand, model, stoc, cg_status, cod_imei) VALUES (10, 5, 'bun', 'telefoane/b96848b7acd10dafde32203d12f6fea7.png', 'OnePlus', '12 256GB', 0, 'disponibil', '351234567890005');
INSERT INTO django.site_telefonie_telefon (produs_ptr_id, id_telefon, descriere_telefon, imagine, brand, model, stoc, cg_status, cod_imei) VALUES (9, 4, '.', 'telefoane/xiaomi_14.jpg', 'Xiaomi', '14 256GB', 0, 'disponibil', '351234567890004');
INSERT INTO django.site_telefonie_telefon (produs_ptr_id, id_telefon, descriere_telefon, imagine, brand, model, stoc, cg_status, cod_imei) VALUES (8, 3, '.', 'telefoane/maxresdefault.jpg', 'Google', 'Pixel 8 128GB', 0, 'disponibil', '351234567890003');
INSERT INTO django.site_telefonie_telefon (produs_ptr_id, id_telefon, descriere_telefon, imagine, brand, model, stoc, cg_status, cod_imei) VALUES (7, 2, '.', 'telefoane/mVRNO3WK-Samsung-Galaxy-S24-1200x799.jpg', 'Samsung', 'Galaxy S24 128GB', 0, 'disponibil', '351234567890002');
INSERT INTO django.site_telefonie_telefon (produs_ptr_id, id_telefon, descriere_telefon, imagine, brand, model, stoc, cg_status, cod_imei) VALUES (6, 1, '.', 'telefoane/iphone_15_pro.png', 'Apple', 'iPhone 15 Pro 256GB', 0, 'disponibil', '351234567890001');


--
-- Name: site_telefonie_telefon_id_telefon_seq; Type: SEQUENCE SET; Schema: django; Owner: ilinca
--

SELECT pg_catalog.setval('django.site_telefonie_telefon_id_telefon_seq', 5, true);


--
-- PostgreSQL database dump complete
--

\unrestrict sVL4VGlUYNgOyPulOykm9z29norF62yhOb7f7K0uuzBmWGZjjoaKE5xCx0YrWsu

--
-- PostgreSQL database dump
--

\restrict lL36g9bSy3BvP4dUNI37OvqetvEex0u1SHrJRAFH3yUhaSNCJXCr5yn7KaoSifo

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: site_telefonie_categoriepachet; Type: TABLE DATA; Schema: django; Owner: ilinca
--

INSERT INTO django.site_telefonie_categoriepachet (id_categorie, nume_categorie, durata_minima, icon) VALUES (1, 'Family', 12, 'fa-solid fa-users');
INSERT INTO django.site_telefonie_categoriepachet (id_categorie, nume_categorie, durata_minima, icon) VALUES (2, 'Business', 24, 'fa-solid fa-briefcase');
INSERT INTO django.site_telefonie_categoriepachet (id_categorie, nume_categorie, durata_minima, icon) VALUES (3, 'Student', 6, 'fa-solid fa-graduation-cap');


--
-- Name: site_telefonie_categoriepachet_id_categorie_seq; Type: SEQUENCE SET; Schema: django; Owner: ilinca
--

SELECT pg_catalog.setval('django.site_telefonie_categoriepachet_id_categorie_seq', 3, true);


--
-- PostgreSQL database dump complete
--

\unrestrict lL36g9bSy3BvP4dUNI37OvqetvEex0u1SHrJRAFH3yUhaSNCJXCr5yn7KaoSifo

--
-- PostgreSQL database dump
--

\restrict 8qeAv0u3MDwfTKJePAtT824fSA9baB33bOaeXtgiATfLvvsiJdbBq9mYgDlQF5C

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: site_telefonie_promotie; Type: TABLE DATA; Schema: django; Owner: ilinca
--

INSERT INTO django.site_telefonie_promotie (id_promotie, discount, data_inceput, data_sfarsit, descriere_promotie) VALUES (1, 20.00, '2025-10-28', '2025-11-27', 'Promoție de lansare - 20% reducere primul an');
INSERT INTO django.site_telefonie_promotie (id_promotie, discount, data_inceput, data_sfarsit, descriere_promotie) VALUES (2, 15.00, '2025-10-28', '2025-12-27', 'Ofertă Business - 15% reducere');


--
-- Name: site_telefonie_promotie_id_promotie_seq; Type: SEQUENCE SET; Schema: django; Owner: ilinca
--

SELECT pg_catalog.setval('django.site_telefonie_promotie_id_promotie_seq', 2, true);


--
-- PostgreSQL database dump complete
--

\unrestrict 8qeAv0u3MDwfTKJePAtT824fSA9baB33bOaeXtgiATfLvvsiJdbBq9mYgDlQF5C

--
-- PostgreSQL database dump
--

\restrict 7kbPUBrCIthKM78Bjay46evRb0h0LhhSS5m6XyB1Nbh2MXteVg58vth0gp5KQyM

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: site_telefonie_pachet; Type: TABLE DATA; Schema: django; Owner: ilinca
--

INSERT INTO django.site_telefonie_pachet (id_pachet, nume_pachet, descriere_pachet, data_crearii, tip, cod_promo, apartine_id, promotie_id) VALUES (2, 'Pachet Pro', '', '2025-10-28 15:38:02.690588+02', 'business', NULL, 2, 2);
INSERT INTO django.site_telefonie_pachet (id_pachet, nume_pachet, descriere_pachet, data_crearii, tip, cod_promo, apartine_id, promotie_id) VALUES (1, 'Pachet Complete', '', '2025-10-28 15:37:51.844084+02', 'complet', NULL, 1, 1);
INSERT INTO django.site_telefonie_pachet (id_pachet, nume_pachet, descriere_pachet, data_crearii, tip, cod_promo, apartine_id, promotie_id) VALUES (3, 'Pachet Smart', '', '2025-10-28 15:38:12.595265+02', 'student', NULL, 3, NULL);


--
-- Name: site_telefonie_pachet_id_pachet_seq; Type: SEQUENCE SET; Schema: django; Owner: ilinca
--

SELECT pg_catalog.setval('django.site_telefonie_pachet_id_pachet_seq', 3, true);


--
-- PostgreSQL database dump complete
--

\unrestrict 7kbPUBrCIthKM78Bjay46evRb0h0LhhSS5m6XyB1Nbh2MXteVg58vth0gp5KQyM

