/*
Start dates and rates for all exchange rates.

First column must be the time stamp relevant for subsequent columns.
Last column must be the country name with the title set to country_name.
*/
SELECT  e.start_date,
        e.rate,
        c.name AS country_name
        FROM countries AS c
        JOIN exchange_rates AS e
        ON c.currency_code = e.currency_code
        ORDER BY e.start_date