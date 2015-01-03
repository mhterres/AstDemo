--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

ALTER TABLE ONLY public.phones DROP CONSTRAINT phones_pkey;
ALTER TABLE ONLY public.monitors_logs DROP CONSTRAINT monitors_logs_pkey;
ALTER TABLE ONLY public.monitors DROP CONSTRAINT monitorr_pkey;
ALTER TABLE ONLY public.logs DROP CONSTRAINT logs_pkey;
ALTER TABLE ONLY public.jids DROP CONSTRAINT jids_pkey;
ALTER TABLE ONLY public.jids_phones DROP CONSTRAINT jids_phones_pkey;
DROP TABLE public.phones;
DROP SEQUENCE public.phones_id_seq;
DROP TABLE public.monitors_logs;
DROP SEQUENCE public.monitors_logs_id_seq;
DROP TABLE public.monitors;
DROP SEQUENCE public.monitors_id_seq;
DROP TABLE public.logs;
DROP SEQUENCE public.logs_id_seq;
DROP TABLE public.jids_phones;
DROP SEQUENCE public.jids_phones_id_seq;
DROP TABLE public.jids;
DROP SEQUENCE public.jids_id_seq;
DROP EXTENSION plpgsql;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: jids_id_seq; Type: SEQUENCE; Schema: public; Owner: asterisk
--

CREATE SEQUENCE jids_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.jids_id_seq OWNER TO astdemo;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: jids; Type: TABLE; Schema: public; Owner: asterisk; Tablespace: 
--

CREATE TABLE jids (
    id bigint DEFAULT nextval('jids_id_seq'::regclass) NOT NULL,
    jid character varying(255) NOT NULL,
    obs text
);


ALTER TABLE public.jids OWNER TO astdemo;

--
-- Name: TABLE jids; Type: COMMENT; Schema: public; Owner: asterisk
--

COMMENT ON TABLE jids IS 'Tabela de jids para testcall';


--
-- Name: jids_phones_id_seq; Type: SEQUENCE; Schema: public; Owner: asterisk
--

CREATE SEQUENCE jids_phones_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.jids_phones_id_seq OWNER TO astdemo;

--
-- Name: jids_phones; Type: TABLE; Schema: public; Owner: asterisk; Tablespace: 
--

CREATE TABLE jids_phones (
    id bigint DEFAULT nextval('jids_phones_id_seq'::regclass) NOT NULL,
    jid_id bigint NOT NULL,
    phone_id bigint NOT NULL
);


ALTER TABLE public.jids_phones OWNER TO astdemo;

--
-- Name: TABLE jids_phones; Type: COMMENT; Schema: public; Owner: asterisk
--

COMMENT ON TABLE jids_phones IS 'Relation between jids and phones
';


--
-- Name: logs_id_seq; Type: SEQUENCE; Schema: public; Owner: asterisk
--

CREATE SEQUENCE logs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 10000000
    CACHE 1;


ALTER TABLE public.logs_id_seq OWNER TO astdemo;

--
-- Name: logs; Type: TABLE; Schema: public; Owner: asterisk; Tablespace: 
--

CREATE TABLE logs (
    id bigint DEFAULT nextval('logs_id_seq'::regclass) NOT NULL,
    date timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    "from" character varying(255) NOT NULL,
    "to" character varying(255) NOT NULL,
    message text NOT NULL
);


ALTER TABLE public.logs OWNER TO astdemo;

--
-- Name: TABLE logs; Type: COMMENT; Schema: public; Owner: asterisk
--

COMMENT ON TABLE logs IS 'Logs do astdemo';


--
-- Name: monitors_id_seq; Type: SEQUENCE; Schema: public; Owner: asterisk
--

CREATE SEQUENCE monitors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 10000000
    CACHE 1;


ALTER TABLE public.monitors_id_seq OWNER TO astdemo;

--
-- Name: monitors; Type: TABLE; Schema: public; Owner: asterisk; Tablespace: 
--

CREATE TABLE monitors (
    id bigint DEFAULT nextval('monitors_id_seq'::regclass) NOT NULL,
    date date DEFAULT now() NOT NULL,
    jid character varying(150) NOT NULL,
    operation character varying(20) NOT NULL,
    type character varying(10) NOT NULL,
    target character(50) NOT NULL,
    laststate character varying(50)
);


ALTER TABLE public.monitors OWNER TO astdemo;

--
-- Name: monitors_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: asterisk
--

CREATE SEQUENCE monitors_logs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 10000000
    CACHE 1;


ALTER TABLE public.monitors_logs_id_seq OWNER TO astdemo;

--
-- Name: monitors_logs; Type: TABLE; Schema: public; Owner: asterisk; Tablespace: 
--

CREATE TABLE monitors_logs (
    id bigint DEFAULT nextval('monitors_logs_id_seq'::regclass) NOT NULL,
    date timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    jid character varying(150),
    operation character varying(20) NOT NULL,
    type character varying(10) NOT NULL,
    target character varying(50) NOT NULL,
    result character varying(59)
);


ALTER TABLE public.monitors_logs OWNER TO astdemo;

--
-- Name: phones_id_seq; Type: SEQUENCE; Schema: public; Owner: asterisk
--

CREATE SEQUENCE phones_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.phones_id_seq OWNER TO astdemo;

--
-- Name: phones; Type: TABLE; Schema: public; Owner: asterisk; Tablespace: 
--

CREATE TABLE phones (
    id bigint DEFAULT nextval('phones_id_seq'::regclass) NOT NULL,
    phone character varying(30) NOT NULL,
    obs text,
    channel character varying(15) NOT NULL
);


ALTER TABLE public.phones OWNER TO astdemo;

--
-- Name: TABLE phones; Type: COMMENT; Schema: public; Owner: asterisk
--

COMMENT ON TABLE phones IS 'Phones for testcall';


--
-- Name: jids_phones_pkey; Type: CONSTRAINT; Schema: public; Owner: asterisk; Tablespace: 
--

ALTER TABLE ONLY jids_phones
    ADD CONSTRAINT jids_phones_pkey PRIMARY KEY (id);


--
-- Name: jids_pkey; Type: CONSTRAINT; Schema: public; Owner: asterisk; Tablespace: 
--

ALTER TABLE ONLY jids
    ADD CONSTRAINT jids_pkey PRIMARY KEY (id);


--
-- Name: logs_pkey; Type: CONSTRAINT; Schema: public; Owner: asterisk; Tablespace: 
--

ALTER TABLE ONLY logs
    ADD CONSTRAINT logs_pkey PRIMARY KEY (id);


--
-- Name: monitorr_pkey; Type: CONSTRAINT; Schema: public; Owner: asterisk; Tablespace: 
--

ALTER TABLE ONLY monitors
    ADD CONSTRAINT monitorr_pkey PRIMARY KEY (id);


--
-- Name: monitors_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: asterisk; Tablespace: 
--

ALTER TABLE ONLY monitors_logs
    ADD CONSTRAINT monitors_logs_pkey PRIMARY KEY (id);


--
-- Name: phones_pkey; Type: CONSTRAINT; Schema: public; Owner: asterisk; Tablespace: 
--

ALTER TABLE ONLY phones
    ADD CONSTRAINT phones_pkey PRIMARY KEY (id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

