/*
Loans that were fully funded.

First column must be the time stamp relevant for subsequent columns.
Last column must be the country name with the title set to country_name.
*/
SELECT  l.created_at,
        c.name AS country_name
        FROM loans AS l
        JOIN borrowers AS b
        ON b.id = l.borrower_id
        JOIN countries AS c
        ON b.country_id = c.id
        WHERE l.raised_percentage = 100
        ORDER BY l.created_at
