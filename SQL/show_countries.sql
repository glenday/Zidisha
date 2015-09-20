/*
Shows the dates each country first enters database
*/
SELECT	c.name,
		MIN(b.created_at) AS first_date,
		MAX(b.created_at) AS last_date,
		COUNT(b.id) AS number_borrowers
		
	FROM borrowers AS b
	JOIN countries AS c
	ON b.country_id = c.id
	WHERE b.activation_status != 4
	GROUP BY c.name
	ORDER BY first_date