/*
Calculate the number of loan requests per month by country
*/
SELECT	EXTRACT(YEAR FROM b.created_at) AS year,		-- year
		EXTRACT(MONTH FROM b.created_at) AS month,	-- month
		COUNT(
			CASE WHEN c.name = 'Kenya' THEN 1
			ELSE NULL
			END
			) AS kenya,
		COUNT(
			CASE WHEN c.name = 'Burkina Faso' THEN 1
			ELSE NULL
			END
			) AS burkina_faso,
		COUNT(
			CASE WHEN c.name = 'Indonesia' THEN 1
			ELSE NULL
			END
			) AS indonesia,
		COUNT(
			CASE WHEN c.name = 'Ghana' THEN 1
			ELSE NULL
			END
			) AS ghana,
		COUNT(
			CASE WHEN c.name = 'Senegal' THEN 1
			ELSE NULL
			END
			) AS senegal
		FROM borrowers AS b
		JOIN countries AS c
		ON b.country_id = c.id								-- 
		WHERE b.activation_status != 4	-- status of 4 means rejected
		GROUP BY year, month	