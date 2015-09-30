/*
Calculate the registration fee size
*/
SELECT	EXTRACT(YEAR FROM l.created_at) AS year,		-- year
		EXTRACT(MONTH FROM l.created_at) AS month,	-- month
		co.name AS country_name,
		COUNT(l.registration_fee) AS number_of_reg_fees_paid,
		ROUND(AVG(l.registration_fee/e.rate)*100)/100 AS avg_reg_fee,
		ROUND(MAX(l.registration_fee/e.rate)*100)/100 AS max_reg_fee,
		ROUND(MIN(l.registration_fee/e.rate)*100)/100 AS min_reg_fees
		FROM loans AS l
		JOIN borrowers AS b
		ON l.borrower_id = b.id AND l.registration_fee > 0
		JOIN countries AS co
		ON b.country_id = co.id
		JOIN exchange_rates AS e
		ON l.currency_code = e.currency_code AND e.is_current = 1
		GROUP BY year, month, country_name
		ORDER BY country_name, year, month