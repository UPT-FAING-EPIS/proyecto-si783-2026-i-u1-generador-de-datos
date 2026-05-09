--
-- PostgreSQL database dump
--

\restrict HECumAX5E8vaC3hKCov7VF30yRwRFNv6IjSfmu4X48OKllViLKwAgcpm3GNwbIq

-- Dumped from database version 16.13 (Debian 16.13-1.pgdg13+1)
-- Dumped by pg_dump version 16.13 (Debian 16.13-1.pgdg13+1)

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

DROP DATABASE IF EXISTS smartgen_db;
--
-- Name: smartgen_db; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE smartgen_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE smartgen_db OWNER TO admin;

\unrestrict HECumAX5E8vaC3hKCov7VF30yRwRFNv6IjSfmu4X48OKllViLKwAgcpm3GNwbIq
\connect smartgen_db
\restrict HECumAX5E8vaC3hKCov7VF30yRwRFNv6IjSfmu4X48OKllViLKwAgcpm3GNwbIq

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

--
-- Name: roleenum; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public.roleenum AS ENUM (
    'admin',
    'user'
);


ALTER TYPE public.roleenum OWNER TO admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activity_logs; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.activity_logs (
    id uuid NOT NULL,
    user_id uuid,
    action character varying(200) NOT NULL,
    detail text,
    ip_address character varying(50),
    user_agent character varying(500),
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.activity_logs OWNER TO admin;

--
-- Name: db_connections; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.db_connections (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    name character varying(200) NOT NULL,
    engine character varying(50) NOT NULL,
    host character varying(500) NOT NULL,
    port integer NOT NULL,
    username character varying(200),
    encrypted_password text,
    database_name character varying(200),
    extra_params json,
    is_active boolean,
    last_used_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.db_connections OWNER TO admin;

--
-- Name: sessions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.sessions (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    token_jti character varying(200) NOT NULL,
    ip_address character varying(50),
    user_agent character varying(500),
    login_method character varying(50),
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    expires_at timestamp with time zone NOT NULL
);


ALTER TABLE public.sessions OWNER TO admin;

--
-- Name: users; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    email character varying(255) NOT NULL,
    username character varying(100) NOT NULL,
    hashed_password character varying(255),
    full_name character varying(200),
    role public.roleenum NOT NULL,
    is_active boolean,
    is_verified boolean,
    avatar_url character varying(500),
    oauth_provider character varying(50),
    oauth_id character varying(200),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.users OWNER TO admin;

--
-- Data for Name: activity_logs; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.activity_logs (id, user_id, action, detail, ip_address, user_agent, created_at) FROM stdin;
36c19c03-7356-4a69-9316-c88866f1a754	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	REGISTER	Registro con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-07 18:43:24.03509+00
dfeabca9-748f-444c-b594-19282bd5a9fd	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-07 18:45:22.416963+00
fb63a3da-5332-4558-ad0c-fa09cbc6cd78	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-07 19:05:10.501567+00
d6b665dd-4f90-4e50-90cb-2556881b3c0e	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-07 19:15:04.192482+00
ffff1f7c-3af9-4115-8cf3-4d9b70074a62	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-07 19:57:51.159317+00
785a16f6-bb59-44df-a2b3-1a4101e58d7f	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-07 20:18:56.47181+00
b16fbd21-306b-4394-95a6-41a0083903ca	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-07 20:25:47.559776+00
19b0bae1-036d-4601-93bb-6aeb77b29669	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-07 20:30:19.803551+00
571da6af-96bb-4071-a4c0-7d6505f030a1	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-07 20:59:18.620878+00
5e70e3b3-15b6-42c3-9503-3f8d1c2e31ce	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-07 21:08:48.068939+00
176541f0-ddc7-4291-a7fb-c8fbf8e15750	567a1072-4a3d-4a4d-97a0-be064e40cb44	REGISTER	Registro con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-07 21:37:09.693241+00
55e5a985-3500-4e28-b29a-d10a523a71ca	567a1072-4a3d-4a4d-97a0-be064e40cb44	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-07 21:37:24.012411+00
bf4ad91b-c9ed-41b4-9a4b-104c0c847b31	567a1072-4a3d-4a4d-97a0-be064e40cb44	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-07 21:55:35.927652+00
06a2e960-c466-46c7-be80-04aa2462dd57	567a1072-4a3d-4a4d-97a0-be064e40cb44	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-07 22:02:52.142986+00
964c4e2c-0db3-4f55-ad58-694595c33324	567a1072-4a3d-4a4d-97a0-be064e40cb44	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-07 23:14:02.557354+00
c77616da-b195-47f4-8305-dbbfe7873091	567a1072-4a3d-4a4d-97a0-be064e40cb44	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-08 01:26:10.728713+00
6acdff79-e1d0-47b1-b348-24afffec0b47	567a1072-4a3d-4a4d-97a0-be064e40cb44	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-08 01:39:52.356964+00
18572055-c273-4d84-a537-b2350d4ba1a8	567a1072-4a3d-4a4d-97a0-be064e40cb44	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-08 01:46:20.482828+00
31960d9a-f785-4b0a-a45b-e429ada25622	442ecc1c-24f2-4c3b-907e-cfec79bef8f3	REGISTER	Registro con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-08 02:01:24.523735+00
272002a0-66dd-49f5-a773-718fc1635bbb	442ecc1c-24f2-4c3b-907e-cfec79bef8f3	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-08 02:01:41.388755+00
23a1b192-4716-4691-b690-8a69b63635f0	567a1072-4a3d-4a4d-97a0-be064e40cb44	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-08 02:02:02.284221+00
41505002-6f29-4aa6-9c4d-c1b25ae35c99	567a1072-4a3d-4a4d-97a0-be064e40cb44	LOGIN	Login con email/password	179.6.57.0	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-08 20:08:05.60374+00
3f2672d4-2756-469b-8d99-28fff5887f38	567a1072-4a3d-4a4d-97a0-be064e40cb44	LOGIN	Login con email/password	179.6.57.0	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-08 20:09:49.851585+00
03e98b7d-09e5-4e43-9120-93399c7037bc	567a1072-4a3d-4a4d-97a0-be064e40cb44	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-08 20:28:08.581722+00
27dba68c-ea23-49f1-ab19-fa9e6dcd2ba1	567a1072-4a3d-4a4d-97a0-be064e40cb44	LOGIN	Login con email/password	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	2026-05-08 21:11:25.256146+00
\.


--
-- Data for Name: db_connections; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.db_connections (id, user_id, name, engine, host, port, username, encrypted_password, database_name, extra_params, is_active, last_used_at, created_at, updated_at) FROM stdin;
6e8cb2e2-8adf-4a8e-8833-1d164424ee61	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	mongodb_test	mongodb	localhost	27017	\N	\N	testdb	null	t	\N	2026-05-07 20:40:20.163644+00	\N
3e99f78a-6657-4855-8df9-6ee3d37371b4	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	mongodb_test	mongodb	localhost	27017	admin	gAAAAABp_PjU0Y6Xnj2CUMBviBp2KfLiyVLXBml6W2rQS_7hfIuDdpFp_gLoMGzo45BOv8wAkZBAINk7_mj4AqcftXWumKE9UQ==	testdb	null	t	\N	2026-05-07 20:40:52.004161+00	\N
b2ae410b-d1b4-47d4-bdf8-af14483c75ab	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	mysql_test	mysql	localhost	3306	testuser	gAAAAABp_PqpDV5C-2Z2m6-Q8TKcDOWtB2HWlnT4BAOoknJBC3tz1StYYqiUyAqa4nsWuZ6idLtgvIgSGFCSWqovGi7JwOSE2w==	testdb	null	t	2026-05-07 20:49:53.121837+00	2026-05-07 20:48:41.098795+00	2026-05-07 20:49:52.558862+00
61f2a0ea-b29c-45fc-964b-be04408ee7f7	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	mongodb_test	mongodb	localhost	27017	\N	\N	testdb	null	t	2026-05-07 20:57:00.384822+00	2026-05-07 20:51:18.774956+00	2026-05-07 20:57:00.339636+00
1ffc69c5-6d91-4405-bda6-a2ad640c41ca	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	mongodb_test	mongodb	localhost	27017	\N	\N	testdb	null	t	2026-05-07 20:57:14.873537+00	2026-05-07 20:57:05.808474+00	2026-05-07 20:57:14.835085+00
121ad6f0-6659-4c77-a2da-202540cc4922	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	mongodb_test	mongodb	localhost	27017	\N	\N	testdb	null	t	\N	2026-05-07 20:58:13.944542+00	\N
3ca87bfa-56f1-4f5f-b4b3-f7f5a375b9b3	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	mongodb_test	mongodb	localhost	27017	\N	\N	testdb	null	t	2026-05-07 20:58:49.939325+00	2026-05-07 20:58:37.779264+00	2026-05-07 20:58:49.909269+00
85ffa306-12c1-4c91-bf84-25fea127ec12	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	mongodb_test	mongodb	localhost	27017	\N	\N	testdb	null	t	2026-05-07 21:05:25.096421+00	2026-05-07 21:00:31.462679+00	2026-05-07 21:05:24.857041+00
7863e423-6652-428e-b611-99faf794c57e	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	mysql_test	mysql	localhost	3306	testuser	gAAAAABp_P_eX2UOZBg-BvxOCvxSr3mqS7EfAyXT_-bQRaloM6lDBNEHPwOC5bzNBMio8-T1QK3XZKfRE83UxUH8sacyruPyTQ==	testdb	null	t	2026-05-07 21:17:08.711569+00	2026-05-07 21:10:54.524574+00	2026-05-07 21:17:08.644771+00
87b6f721-8d0f-419d-acf7-e270751f4855	567a1072-4a3d-4a4d-97a0-be064e40cb44	mysql_test	mysql	localhost	3306	testuser	gAAAAABp_QZ46Bv3b0EPbocCgybxsJY17c4X_zlko19gbFkAKN08-WS1k2V80vc6CbKSZauVu1rdKfKaHmFpwQOhz0VEJ8VSMA==	testdb	null	t	2026-05-07 22:25:11.730731+00	2026-05-07 21:39:04.313354+00	2026-05-07 22:25:11.614458+00
1c71b37e-bd3e-4e8a-94e2-a81f9e632cc7	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	mysql_test	mysql	localhost	3306	testuser	gAAAAABp_QIJEmrkAdR8GY4d2e4s4bQ0oSd9RbSnA0GYbnFJ7S_jA2n9vs-I2Ca74-sRAp9RltX8J_iGQB2doGNdoGWNhdHsJA==	testdb	null	t	2026-05-07 21:21:30.125068+00	2026-05-07 21:20:09.873951+00	2026-05-07 21:21:30.05316+00
0ca402d0-de76-4c73-81c6-462fa2ed9410	567a1072-4a3d-4a4d-97a0-be064e40cb44	mongodb_test	mongodb	localhost	27017	test	gAAAAABp_R0NOlbyo3QjGi2ETKO9VwzNGGMTMjgTMTkfxdC24ZLQ74aCA3fLKAoUiMwC57mj7EoLcHLRtmtfyppPSilJ_y9SLQ==	mongodb_test	null	f	\N	2026-05-07 23:15:25.950415+00	2026-05-07 23:15:59.429402+00
69d1a688-b570-43b7-9d38-c25f798a965a	567a1072-4a3d-4a4d-97a0-be064e40cb44	mongodb_test	mongodb	localhost	27017		\N	mongodb_test	null	t	2026-05-08 01:26:35.534691+00	2026-05-07 23:18:43.695667+00	2026-05-08 01:26:35.147505+00
59b508cf-40d3-4efd-a7d4-b544e0593ca7	567a1072-4a3d-4a4d-97a0-be064e40cb44	neo4j_test	neo4j	localhost	7687	neo4j	gAAAAABp_T4xVxUum4lNpizJbyUYtjSISVmSTjoNNpaubuEZ_kr5xsO_IP6xm76o8eY0PQNfbAuisSJYwaQBww77z65Tt_GRtw==	neo4j	null	t	2026-05-08 21:15:28.239852+00	2026-05-08 01:36:49.47553+00	2026-05-08 21:15:25.680056+00
9906a710-364c-45bd-820f-449379c3fcd4	567a1072-4a3d-4a4d-97a0-be064e40cb44	mongodb_shop	mongodb	localhost	27017		\N	shopdb	null	t	2026-05-08 22:06:37.517721+00	2026-05-07 23:19:23.379604+00	2026-05-08 22:06:37.459512+00
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.sessions (id, user_id, token_jti, ip_address, user_agent, login_method, is_active, created_at, expires_at) FROM stdin;
bb503f31-05d3-4b91-913c-ef96e37bcbd3	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	8af1dff8-724e-40e8-b15b-0f13ff340dc6	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-07 18:45:22.416963+00	2026-05-07 19:45:22.77848+00
49d9a856-9442-43e2-b066-12dfcf544b12	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	d14bd9e7-657d-4009-bb61-13acf64eeceb	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-07 19:05:10.501567+00	2026-05-07 20:05:11.071553+00
6e30a8d3-840e-49b1-bd42-ae86660f3966	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	c81313b0-6a9f-494e-a02e-536a2d88302e	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-07 19:15:04.192482+00	2026-05-07 20:15:04.679814+00
a0cafb7f-a501-4184-8e4a-5a81c9ff3d74	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	a5de250f-6f6f-485e-9ff3-1f2e6a743113	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-07 19:57:51.159317+00	2026-05-07 20:57:52.448592+00
52dbf42e-7912-4150-b560-83999e1c4737	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	37cbe3f8-69d0-4292-96e2-00ca1f87393f	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-07 20:18:56.47181+00	2026-05-07 21:18:57.38255+00
6b3e32e3-ba9b-424f-998f-1bb509538c3f	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	a0293ff2-d895-4d08-8808-1ad9f3ce08d7	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-07 20:25:47.559776+00	2026-05-07 21:25:48.709047+00
b060fc38-96ae-4eae-b7af-d5a5351fa2d7	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	c3f91183-0862-4544-9b53-e476cf58d717	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-07 20:30:19.803551+00	2026-05-07 21:30:20.982904+00
cf5f2f68-070d-4d1a-8d3e-e4ef0bab3084	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	b2c513b4-cfdd-4102-94e2-f9ec9349d283	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-07 20:59:18.620878+00	2026-05-07 21:59:19.138741+00
0f3c1e20-7d76-4720-a96b-9f96ce960106	36e2b04b-9d3e-4cdb-83dd-9c58339ba672	110eaac5-e4b9-428f-8035-1ff8f265f912	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-07 21:08:48.068939+00	2026-05-07 22:08:48.536684+00
51067899-3869-417b-9f84-4d6b49870106	567a1072-4a3d-4a4d-97a0-be064e40cb44	d0fe6e42-eb4d-4d2f-9542-aaa78976c445	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-07 21:37:24.012411+00	2026-05-07 22:37:24.542993+00
52a6bf1f-1c1f-45e6-9426-a9734cd94509	567a1072-4a3d-4a4d-97a0-be064e40cb44	76c622d6-1fa6-43ea-a896-947f153a9fa8	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-07 21:55:35.927652+00	2026-05-07 22:55:36.525845+00
23bea75c-3e2e-4379-9baf-c2b492337f16	567a1072-4a3d-4a4d-97a0-be064e40cb44	fff2ac9c-7d72-4fea-824f-05d83f9b761d	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-07 22:02:52.142986+00	2026-05-07 23:02:52.607911+00
359bc948-e9a9-4a45-a57b-d007c539e240	567a1072-4a3d-4a4d-97a0-be064e40cb44	26e4f525-a159-4624-9efe-6433678a94c5	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-07 23:14:02.557354+00	2026-05-08 00:14:03.627593+00
4510860d-4e00-4d96-b765-585ed74b6c37	567a1072-4a3d-4a4d-97a0-be064e40cb44	5f117f8f-0399-4b72-8375-d1d0950e29ef	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-08 01:26:10.728713+00	2026-05-08 02:26:11.979535+00
d94703f1-bd25-4833-a21e-fd3ba54643ed	567a1072-4a3d-4a4d-97a0-be064e40cb44	b1e66833-123e-4b68-aaae-7f2c4143ba3e	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-08 01:39:52.356964+00	2026-05-08 02:39:52.797725+00
93a50cfe-d52d-4b27-be57-a899ffbd50ca	567a1072-4a3d-4a4d-97a0-be064e40cb44	a6f545a5-2240-4371-b8b3-82cedcfd14ea	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	f	2026-05-08 01:46:20.482828+00	2026-05-08 02:46:21.059159+00
4ff59039-07f4-4ae8-a8c8-3aa76d33f69c	442ecc1c-24f2-4c3b-907e-cfec79bef8f3	af12c966-45a2-4a19-90e8-1c1cceff9242	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	f	2026-05-08 02:01:41.388755+00	2026-05-08 03:01:41.747582+00
ad2bfe94-b235-45dc-93b6-0ba2a618421e	567a1072-4a3d-4a4d-97a0-be064e40cb44	693adb3e-acab-4a67-8508-7474a0b42e92	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-08 02:02:02.284221+00	2026-05-08 03:02:02.626903+00
ab3443de-c9e0-4177-a17a-5555f38d9b17	567a1072-4a3d-4a4d-97a0-be064e40cb44	115df7ab-9679-4965-9c49-c5d8b5842e83	179.6.57.0	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-08 20:08:05.60374+00	2026-05-08 21:08:06.912292+00
2ae0de01-8bf4-45ce-be1f-fc776e79cfc2	567a1072-4a3d-4a4d-97a0-be064e40cb44	74ed5857-f27b-48aa-99a3-db56c8dc3af3	179.6.57.0	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-08 20:09:49.851585+00	2026-05-08 21:09:50.744032+00
f94ad73f-1dae-4f9b-9d13-e1ce83c80281	567a1072-4a3d-4a4d-97a0-be064e40cb44	c5bf190c-c586-436c-94a8-17ee2229334d	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-08 20:28:08.581722+00	2026-05-08 21:28:09.587348+00
629d3606-284e-491f-a13a-ebe9621a4757	567a1072-4a3d-4a4d-97a0-be064e40cb44	5d60933b-6731-4747-9e25-8928096f98fd	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36	email	t	2026-05-08 21:11:25.256146+00	2026-05-08 22:11:25.879534+00
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users (id, email, username, hashed_password, full_name, role, is_active, is_verified, avatar_url, oauth_provider, oauth_id, created_at, updated_at) FROM stdin;
36e2b04b-9d3e-4cdb-83dd-9c58339ba672	mary@example.com	mary	$2b$12$igMaaiURRiBF7XGl7P/JXOxIrEYz5QrXV.kup.bVHZ1tK26SQ/6cC	Mary	user	t	f	\N	\N	\N	2026-05-07 18:43:24.03509+00	\N
567a1072-4a3d-4a4d-97a0-be064e40cb44	maranyramos7@gmail.com	mari_09	$2b$12$zv8Q8OfC3biPhGhuPyGdfuIg1iG2p5HnRvRl2Yb0YW7rrIvmpNqbW	Mariela Ramos	admin	t	f	\N	\N	\N	2026-05-07 21:37:09.693241+00	\N
442ecc1c-24f2-4c3b-907e-cfec79bef8f3	marymar@gmail.com	mary_30	$2b$12$iUG2ER3VKbNKfscl/Ll5au0G55plHjy7Hml7lQx3VCwPfJw1LF0uq	marymar	user	t	f	\N	\N	\N	2026-05-08 02:01:24.523735+00	\N
\.


--
-- Name: activity_logs activity_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.activity_logs
    ADD CONSTRAINT activity_logs_pkey PRIMARY KEY (id);


--
-- Name: db_connections db_connections_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.db_connections
    ADD CONSTRAINT db_connections_pkey PRIMARY KEY (id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: sessions sessions_token_jti_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_token_jti_key UNIQUE (token_jti);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: ix_activity_logs_user_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_activity_logs_user_id ON public.activity_logs USING btree (user_id);


--
-- Name: ix_db_connections_user_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_db_connections_user_id ON public.db_connections USING btree (user_id);


--
-- Name: ix_sessions_user_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_sessions_user_id ON public.sessions USING btree (user_id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: admin
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- PostgreSQL database dump complete
--

\unrestrict HECumAX5E8vaC3hKCov7VF30yRwRFNv6IjSfmu4X48OKllViLKwAgcpm3GNwbIq

