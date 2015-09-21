SELECT  c.name AS country_name
        FROM borrowers AS b
        JOIN countries AS c
        ON b.country_id = c.id
        GROUP BY country_name