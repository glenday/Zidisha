/*
Calculate the size of first time loans
*/
SELECT	EXTRACT(YEAR FROM created_at) AS year,		-- year
		EXTRACT(MONTH FROM created_at) AS month,	-- month
		DAYOFMONTH(created_at) AS day,
		MAX(
			CASE 	WHEN registration_fee > 0 THEN usd_amount
					ELSE NULL
					END
			) AS max_new_loan_size		-- maximum new loan size per month
		FROM loans
		WHERE created_at > '2015-01-01'
		GROUP BY year, month, day
		ORDER BY year, month, day
		
		