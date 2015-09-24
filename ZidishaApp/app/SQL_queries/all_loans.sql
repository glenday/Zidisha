SELECT  l.created_at,
        l.usd_amount AS usd_requested,
        l.raised_percentage/100.0 AS raised_fraction,
        l.usd_amount * l.raised_percentage/100.0 AS usd_inflow,
        CASE    WHEN l.raised_percentage = 100 THEN l.usd_amount
                ELSE 0
                END AS usd_secured,
        c.name AS country_name
        FROM loans AS l
        JOIN borrowers AS b
        ON b.id = l.borrower_id
        JOIN countries AS c
        ON b.country_id = c.id
        ORDER BY l.created_at
