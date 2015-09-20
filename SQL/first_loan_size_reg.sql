/*
Calculate the size of first time loans
*/
SELECT	EXTRACT(YEAR FROM l.created_at) AS year,		-- year
		EXTRACT(MONTH FROM l.created_at) AS month,	-- month
		MAX(
			CASE 	WHEN l.registration_fee > 0 THEN l.usd_amount
					ELSE NULL
					END
			) AS max_new_loan_size,		-- maximum new loan size per month
		MAX(
			CASE 	WHEN l.registration_fee > 0 THEN l.registration_fee/e.rate
					ELSE NULL
					END
			) AS max_reg_fee,
		MIN(
			CASE 	WHEN l.registration_fee > 0 THEN l.registration_fee/e.rate
					ELSE NULL
					END
			) AS min_reg_fee,
		AVG(
			CASE 	WHEN l.registration_fee > 0 THEN l.registration_fee/e.rate
					ELSE NULL
					END
			) AS avg_reg_fee,
		AVG(
			CASE 	WHEN l.registration_fee > 0 THEN l.registration_fee/e.rate
					ELSE NULL
					END
			) AS avg_reg_fee_frac,
		MAX(
			CASE 	WHEN l.registration_fee > 0 THEN l.total_amount/e.rate
					ELSE NULL
					END
			) AS max_loan_local
		FROM loans AS l
		JOIN exchange_rates AS e
		ON l.currency_code = e.currency_code
		WHERE e.is_current = 1
		GROUP BY year, month
		
		