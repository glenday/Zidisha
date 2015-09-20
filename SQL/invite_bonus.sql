/*
Calculate the invitation bonus
*/
SELECT	EXTRACT(YEAR FROM c.created_at) AS year,		-- year
		EXTRACT(MONTH FROM c.created_at) AS month,	-- month
		co.name AS country_name,
		COUNT(c.credit) AS number_of_credits,
		MAX(c.credit/e.rate) AS max_credit,
		MIN(c.credit/e.rate) AS min_credit
--		AVG(c.credit/e.rate) AS avg_credit
		FROM credits_earned_new AS c
		JOIN borrowers AS b
		ON c.credit_to = b.id AND c.credit_type = 3
		JOIN countries AS co
		ON b.country_id = co.id
		JOIN exchange_rates AS e
		ON co.currency_code = e.currency_code AND e.is_current = 1		-- 
--		WHERE activation_status != 4	-- status of 4 means rejected
		GROUP BY year, month, country_name
		ORDER BY country_name, year, month