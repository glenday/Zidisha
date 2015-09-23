SELECT  l.created_at,
        l.usd_amount,
        l.raised_percentage,
        c.name AS country_name
        FROM loans AS l
        JOIN borrowers AS b
        ON b.id = l.borrower_id
        JOIN countries AS c
        ON b.country_id = c.id
        ORDER BY l.created_at
