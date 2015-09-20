/*
Calculate the size of first time loans
*/
SELECT	EXTRACT(YEAR FROM l.created_at) AS year,		-- year
		EXTRACT(MONTH FROM l.created_at) AS month,	-- month
		MAX(l.usd_amount) AS max_first_loans,
		MAX(
			CASE WHEN c.name = 'Kenya' THEN l.usd_amount
			ELSE NULL
			END
			) AS kenya,
		MAX(
			CASE WHEN c.name = 'Burkina Faso' THEN l.usd_amount
			ELSE NULL
			END
			) AS burkina_faso,
		MAX(
			CASE WHEN c.name = 'Indonesia' THEN l.usd_amount
			ELSE NULL
			END
			) AS indonesia,
		MAX(
			CASE WHEN c.name = 'Ghana' THEN l.usd_amount
			ELSE NULL
			END
			) AS ghana,
		MAX(
			CASE WHEN c.name = 'Senegal' THEN l.usd_amount
			ELSE NULL
			END
			) AS senegal
		FROM loans AS l
		JOIN borrowers AS b
		ON l.borrower_id = b.id
		JOIN countries AS c
		ON b.country_id = c.id
		WHERE l.registration_fee > 0
		GROUP BY year, month
		
		