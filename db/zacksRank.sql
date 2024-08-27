-- Table: public.zacksRank

DROP TABLE IF EXISTS public.zacksRank;

CREATE TABLE IF NOT EXISTS public.zacksRank
(
    da timestamp without time zone NOT NULL,
    code character varying(50) COLLATE pg_catalog."default",
    rank character varying(50)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.zacksRank
    OWNER to postgres;

GRANT ALL ON TABLE public.zacksRank TO postgres;