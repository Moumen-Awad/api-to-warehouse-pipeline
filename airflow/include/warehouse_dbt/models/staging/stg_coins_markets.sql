select 
    (payload->>'id')::text as coin_id,
    (payload->>'symbol')::text as symbol,
    (payload->>'name')::text as name,
    (payload->>'current_price')::numeric as current_price_usd,
    (payload->>'market_cap')::numeric as market_cap_usd,
    (payload->>'total_volume')::numeric as total_volume_usd,
    (payload->>'price_change_percentage_24h')::numeric as price_change_pct_24h,
    loaded_at
from {{source('staging','coins_markets_raw')}}
