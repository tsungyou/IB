DROP TABLE IF EXISTS public.stock_price_5m;

CREATE TABLE IF NOT EXISTS public.stock_price_5m
(
    da timestamp without time zone NOT NULL,
    code character varying(25) COLLATE pg_catalog."default" NOT NULL,
    cl double precision,
    wap double precision,
    vol bigint,
    CONSTRAINT blp_stockprice_pkey_5m_us PRIMARY KEY (da, code)
)
WITH (
    OIDS = FALSE
)