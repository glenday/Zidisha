/*
Calculate the loan loss reserve fee
*/
SELECT	EXTRACT(YEAR FROM l.created_at) AS year,		-- year
		EXTRACT(MONTH FROM l.created_at) AS month,	-- month
		co.name AS country_name,
		COUNT(l.loan_loss_reserve_fee) AS number_of_llr_fees_paid,
		ROUND(MAX(l.loan_loss_reserve_fee/e.rate)*100)/100 AS max_llr_fee,
		ROUND(MIN(l.loan_loss_reserve_fee/e.rate)*100)/100 AS min_llr_fees
		FROM loans AS l
		JOIN borrowers AS b
		ON l.borrower_id = b.id AND l.loan_loss_reserve_fee > 0
		JOIN countries AS co
		ON b.country_id = co.id
		JOIN exchange_rates AS e
		ON l.currency_code = e.currency_code AND e.is_current = 1
		GROUP BY year, month, country_name
		ORDER BY country_name, year, month