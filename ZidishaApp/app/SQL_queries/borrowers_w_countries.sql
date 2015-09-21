SELECT  b.created_at AS created_at,
        c.name AS country_name
        FROM borrowers AS b
        JOIN countries AS c
        ON c.id = b.country_id AND b.activation_status != 4