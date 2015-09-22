SELECT  e.start_date,
        e.rate,
        c.name AS country_name
        FROM countries AS c
        JOIN exchange_rates AS e
        ON c.currency_code = e.currency_code
        ORDER BY e.start_date