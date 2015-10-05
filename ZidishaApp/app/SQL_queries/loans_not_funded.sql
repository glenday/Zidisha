/*
Loans that were not fully funded.

First column must be the time stamp relevant for subsequent columns.
Last column must be the country name with the title set to country_name.
*/
SELECT  l.expired_at,
		TIMESTAMPDIFF(SECOND, l.created_at, l.expired_at)/86400.0 AS time_to_expire, -- fractional days
		l.raised_percentage,
        c.name AS country_name
 		FROM loans AS l
        JOIN borrowers AS b
        ON b.id = l.borrower_id
        JOIN countries AS c
        ON b.country_id = c.id
		WHERE raised_percentage < 100 AND expired_at IS NOT NULL -- AND TIMESTAMPDIFF(SECOND, created_at, expired_at)/86400.0 > 3
