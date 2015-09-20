/*
Calculate the rate that new loans are funded
*/
SELECT	year,
		month,
		num_loans_started,
		ROUND(num_loans_filled / num_loans_started * 100) AS percent_filled,
		total_usd_requested,
		ROUND(total_usd_inflow / total_usd_requested * 100) AS percent_of_requested
	FROM (
	SELECT	EXTRACT(YEAR FROM created_at) AS year,		-- year
			EXTRACT(MONTH FROM created_at) AS month,	-- month
			COUNT(id) AS num_loans_started,		-- count of new loans per month
			COUNT(
				CASE WHEN raised_percentage = 100 THEN 1
				ELSE NULL
				END
				) AS num_loans_filled,
			ROUND(SUM( raised_percentage/100 * usd_amount )) AS total_usd_inflow,
			ROUND(SUM( usd_amount )) AS total_usd_requested
			FROM loans
			GROUP BY year, month
	) sub
		
		