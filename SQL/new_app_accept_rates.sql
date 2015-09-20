/*
Calculate the number of loan requests per month
*/
SELECT	EXTRACT(YEAR FROM created_at) AS year,		-- year
		EXTRACT(MONTH FROM created_at) AS month,	-- month
		COUNT(id) AS new_loans_per_month			-- loan count per month
		FROM borrowers								-- 
		WHERE activation_status != 4	-- status of 4 means rejected
		GROUP BY year, month