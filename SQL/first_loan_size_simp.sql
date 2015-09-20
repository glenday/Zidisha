/*
Calculate the size of first time loans
*/
SELECT	EXTRACT(YEAR FROM created_at) AS year,		-- year
		EXTRACT(MONTH FROM created_at) AS month,	-- month
		MAX(usd_amount) AS max_new_loan_size		-- maximum new loan size per month
		FROM loans
		WHERE registration_fee > 0
		GROUP BY year, month
		
		