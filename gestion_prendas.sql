--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: prendas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.prendas (
    id integer NOT NULL,
    tipo_prenda character varying(50),
    propietario character varying(50),
    color_material character varying(50),
    departamento character varying(50),
    id_propietario character varying(50),
    codigo_inventario character varying(50),
    alertas text,
    ciclo_preferido character varying(20),
    restricciones text,
    temperatura character varying(20),
    ciclos_realizados integer,
    fecha_ultimo_lavado date,
    tipo_ciclo character varying(50),
    nivel_desgaste character varying(50),
    id_usuario character varying(50),
    preferencias_lavado text,
    tipo_detergente character varying(50),
    alergias text,
    ubicacion character varying(50),
    datos_desinfeccion text,
    certificacion_limpieza character varying(50),
    rfcid character varying(50)
);


ALTER TABLE public.prendas OWNER TO postgres;

--
-- Name: prendas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.prendas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.prendas_id_seq OWNER TO postgres;

--
-- Name: prendas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.prendas_id_seq OWNED BY public.prendas.id;


--
-- Name: prendas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prendas ALTER COLUMN id SET DEFAULT nextval('public.prendas_id_seq'::regclass);


--
-- Data for Name: prendas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.prendas (id, tipo_prenda, propietario, color_material, departamento, id_propietario, codigo_inventario, alertas, ciclo_preferido, restricciones, temperatura, ciclos_realizados, fecha_ultimo_lavado, tipo_ciclo, nivel_desgaste, id_usuario, preferencias_lavado, tipo_detergente, alergias, ubicacion, datos_desinfeccion, certificacion_limpieza, rfcid) FROM stdin;
1	camisa	Juan Pérez	azul, algodón	Administración	JP001	INV12345	Sin alertas	delicado	no centrifugar	frío	10	2024-10-25	suave	medio	JP001	Nada	detergente hipoalergénico	ninguna	Almacén A	Desinfección hospitalaria	Certificado 2024	RFC12345
2	pantalón	María López	negro, poliéster	Producción	ML002	INV67890	Sin alertas	intensivo	no usar suavizante	caliente	25	2024-10-15	intensivo	alto	ML002	Nada	detergente común	sensibilidad a suavizantes	Almacén B	Desinfección de laboratorio	Certificado 2024	RFC67890
3	\N	\N	\N	\N	\N	INV63545	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
4	camisa	Juan Pérez	azul, algodón	Administración	\N	Prueba323214	Sin alertas	delicado	no centrifugar	frío	10	2024-10-25	suave	medio	JP001	Nada	detergente hipoalergénico	ninguna	Almacén A	Desinfección hospitalaria	Certificado 2024	\N
\.


--
-- Name: prendas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.prendas_id_seq', 4, true);


--
-- Name: prendas prendas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prendas
    ADD CONSTRAINT prendas_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

