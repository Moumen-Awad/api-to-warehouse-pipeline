select
    coin_id, 
    name, 
    date_trunc('day', loaded_at) as metric_date,
    avg (current_price_usd) as avg_price_usd,
    max (market_cap_usd) as market_cap_usd,
    avg (price_change_pct_24h) as avg_price_change_pct_24h
from {{ref('stg_coins_markets')}}
group by coin_id, name, date_trunc('day', loaded_at)