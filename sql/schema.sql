--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.4

-- Started on 2025-09-21 14:29:11

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 155684)
-- Name: rides_ola; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rides_ola (
    id integer NOT NULL,
    date timestamp without time zone,
    "time" time without time zone,
    booking_id character varying(50),
    booking_status character varying(50),
    customer_id character varying(50),
    vehicle_type character varying(50),
    pickup_location character varying(100),
    drop_location character varying(100),
    v_tat double precision,
    c_tat double precision,
    canceled_rides_by_customer text,
    canceled_rides_by_driver text,
    incomplete_rides text,
    incomplete_rides_reason text,
    booking_value double precision,
    payment_method character varying(50),
    ride_distance double precision,
    driver_ratings double precision,
    customer_rating double precision,
    vehicle_images text,
    is_completed boolean,
    is_canceled boolean,
    dayofweek character varying(20),
    month integer,
    hour integer
);


ALTER TABLE public.rides_ola OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 155683)
-- Name: rides_ola_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rides_ola_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rides_ola_id_seq OWNER TO postgres;

--
-- TOC entry 4938 (class 0 OID 0)
-- Dependencies: 217
-- Name: rides_ola_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rides_ola_id_seq OWNED BY public.rides_ola.id;


--
-- TOC entry 4774 (class 2604 OID 155687)
-- Name: rides_ola id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rides_ola ALTER COLUMN id SET DEFAULT nextval('public.rides_ola_id_seq'::regclass);


--
-- TOC entry 4776 (class 2606 OID 155691)
-- Name: rides_ola rides_ola_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rides_ola
    ADD CONSTRAINT rides_ola_pkey PRIMARY KEY (id);


-- Completed on 2025-09-21 14:29:11

--
-- PostgreSQL database dump complete
--

