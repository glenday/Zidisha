SELECT  l.applied_at,
        TIMESTAMPDIFF(SECOND, l.applied_at, l.accepted_at)/86400.0 AS time_to, -- fractional days
        c.name AS country_name
        FROM loans AS l
        JOIN borrowers AS b
        ON b.id = l.borrower_id
        JOIN countries AS c
        ON c.id = b.country_id
        WHERE disbursed_at IS NOT NULL
        ORDER BY applied_at