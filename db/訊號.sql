-- Table: public.block_code3_deatil

DROP TABLE IF EXISTS public.block_code3_deatil;

CREATE TABLE IF NOT EXISTS public.block_code3_deatil
(
    da timestamp without time zone NOT NULL,
    code character varying(50) COLLATE pg_catalog."default",
    direction character varying(50),
    strategy character varying(50)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.block_code3_deatil
    OWNER to postgres;

GRANT ALL ON TABLE public.block_code3_deatil TO postgres;