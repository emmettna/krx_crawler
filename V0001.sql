CREATE TABLE IF NOT EXISTS "korean_stock"
(
    id                   TEXT        PRIMARY KEY,
    date                 DATE        NOT NULL,
    isu                  TEXT        NOT NULL,
    name                 TEXT        NOT NULL,
    market               TEXT        NOT NULL,
    sector               TEXT        ,
    end_price            BIGINT      NOT NULL,
    change_price         BIGINT      NOT NULL,
    change_rate          REAL        NOT NULL,
    start_price          BIGINT      NOT NULL,
    highest_price        BIGINT      NOT NULL,
    lowest_price         BIGINT      NOT NULL,
    trade_volume         BIGINT      NOT NULL,
    trade_amount         BIGINT      NOT NULL,
    market_cap           BIGINT      NOT NULL,
    number_of_share      BIGINT      NOT NULL,
    updated_at           TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    created_at           TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

CREATE TABLE IF NOT EXISTS "korean_stock_base_value"
(
    id                   TEXT        PRIMARY KEY,
    date                 DATE        NOT NULL,
    isu                  TEXT        NOT NULL,
    name                 TEXT        NOT NULL,
    end_price            BIGINT      NOT NULL,
    eps                  BIGINT      NOT NULL,
    per                  REAL        NOT NULL,
    forward_eps          BIGINT      NOT NULL,
    forward_per          REAL        NOT NULL,
    bps                  BIGINT      NOT NULL,
    pbr                  REAL        NOT NULL,
    dps                  BIGINT      NOT NULL,
    dividen_yield        REAL        NOT NULL,
    updated_at           TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    created_at           TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

CREATE TABLE IF NOT EXISTS "korean_etf"
(
    id                      TEXT        PRIMARY KEY,
    date                    DATE        NOT NULL,
    isu                     TEXT        NOT NULL,
    name                    TEXT        NOT NULL,
    end_price               BIGINT      NOT NULL,
    change_price            BIGINT      NOT NULL,
    change_rate             REAL        NOT NULL,
    net_value               FLOAT       NOT NULL,
    start_price             BIGINT      NOT NULL,
    highest_price           BIGINT      NOT NULL,
    lowest_price            BIGINT      NOT NULL,
    trade_volume            BIGINT      NOT NULL,
    trade_amount            BIGINT      NOT NULL,
    market_cap              BIGINT      NOT NULL,
    net_cap_value           BIGINT      NOT NULL,
    number_of_share         BIGINT      NOT NULL,
    base_index_name         TEXT        NOT NULL,
    base_index_end_point    FLOAT       NOT NULL,
    base_index_change_point FLOAT       NOT NULL,
    base_index_change_rate  REAL        NOT NULL,
    updated_at              TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    created_at              TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);