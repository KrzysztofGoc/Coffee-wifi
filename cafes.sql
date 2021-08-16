--
-- PostgreSQL database dump
--

-- Dumped from database version 13.3
-- Dumped by pg_dump version 13.3

-- Started on 2021-08-16 12:35:39

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
-- TOC entry 200 (class 1259 OID 16395)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 16402)
-- Name: cafe; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cafe (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    location character varying(250) NOT NULL,
    open_time time without time zone NOT NULL,
    close_time time without time zone NOT NULL,
    coffee_quality character varying(250) NOT NULL,
    wifi_speed character varying(250) NOT NULL,
    power_socket character varying(250) NOT NULL,
    user_id integer
);


ALTER TABLE public.cafe OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 16400)
-- Name: cafe_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cafe_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cafe_id_seq OWNER TO postgres;

--
-- TOC entry 3012 (class 0 OID 0)
-- Dependencies: 201
-- Name: cafe_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cafe_id_seq OWNED BY public.cafe.id;


--
-- TOC entry 204 (class 1259 OID 16413)
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    email character varying(100),
    password character varying(250),
    name character varying(100)
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 16411)
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO postgres;

--
-- TOC entry 3013 (class 0 OID 0)
-- Dependencies: 203
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- TOC entry 2861 (class 2604 OID 16405)
-- Name: cafe id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cafe ALTER COLUMN id SET DEFAULT nextval('public.cafe_id_seq'::regclass);


--
-- TOC entry 2862 (class 2604 OID 16416)
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- TOC entry 3002 (class 0 OID 16395)
-- Dependencies: 200
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.alembic_version (version_num) VALUES ('0ae1115f2bfb');


--
-- TOC entry 3004 (class 0 OID 16402)
-- Dependencies: 202
-- Data for Name: cafe; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.cafe (id, name, location, open_time, close_time, coffee_quality, wifi_speed, power_socket, user_id) VALUES (7, 'Lighthaus', 'https://goo.gl/maps/2EvhB4oq4gyUXKXx9', '11:00:00', '15:30:00', '☕☕☕☕', '💪💪', '🔌🔌🔌', 6);
INSERT INTO public.cafe (id, name, location, open_time, close_time, coffee_quality, wifi_speed, power_socket, user_id) VALUES (8, 'Esters', 'https://goo.gl/maps/13Tjc36HuPWLELaSA', '08:00:00', '15:00:00', '☕☕☕☕', '💪💪💪', '🔌', 6);
INSERT INTO public.cafe (id, name, location, open_time, close_time, coffee_quality, wifi_speed, power_socket, user_id) VALUES (9, 'Ginger & White', 'https://goo.gl/maps/DqMx2g5LiAqv3pJQ9', '07:30:00', '17:30:00', '☕☕☕', '✘', '🔌', 6);
INSERT INTO public.cafe (id, name, location, open_time, close_time, coffee_quality, wifi_speed, power_socket, user_id) VALUES (10, 'Mare Street Market', 'https://goo.gl/maps/ALR8iBiNN6tVfuAA8', '08:00:00', '13:00:00', '☕☕', '💪💪💪', '🔌🔌🔌', 6);


--
-- TOC entry 3006 (class 0 OID 16413)
-- Dependencies: 204
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public."user" (id, email, password, name) VALUES (6, 'User@gmail.com', '$2b$14$7obBBT4VYWmEcEMujKUThOOyqCNwaCXN3AwinxDvdKO6V30D91sxe', 'User');


--
-- TOC entry 3014 (class 0 OID 0)
-- Dependencies: 201
-- Name: cafe_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cafe_id_seq', 10, true);


--
-- TOC entry 3015 (class 0 OID 0)
-- Dependencies: 203
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 6, true);


--
-- TOC entry 2864 (class 2606 OID 16399)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 2866 (class 2606 OID 16410)
-- Name: cafe cafe_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cafe
    ADD CONSTRAINT cafe_pkey PRIMARY KEY (id);


--
-- TOC entry 2868 (class 2606 OID 16420)
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- TOC entry 2870 (class 2606 OID 16418)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 2871 (class 2606 OID 16421)
-- Name: cafe cafe_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cafe
    ADD CONSTRAINT cafe_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


-- Completed on 2021-08-16 12:35:39

--
-- PostgreSQL database dump complete
--

