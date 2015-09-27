/*
Account creation dates for borrowers who were accepted.

First column must be the time stamp relevant for subsequent columns.
Last column must be the country name with the title set to country_name.
*/
SELECT  b.created_at,
        c.name AS country_name
        FROM borrowers AS b
        JOIN countries AS c
        ON c.id = b.country_id AND b.activation_status != 4
        ORDER BY b.created_at