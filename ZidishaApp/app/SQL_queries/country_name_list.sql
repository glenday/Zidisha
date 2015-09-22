SELECT  c.name AS country_name
        FROM borrowers AS b
        JOIN countries AS c
        ON b.country_id = c.id AND b.activation_status != 4
        GROUP BY country_name
        ORDER BY country_name