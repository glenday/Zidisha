/*
Calculate the loan loss reserve fee
*/
SELECT	EXTRACT(YEAR FROM created_at) AS year,		-- year
		EXTRACT(MONTH FROM created_at) AS month,	-- month
		COUNT(l.loan_loss_reserve_fee) AS count_llr_fee,	-- count of usd loan loss reserve fee
		AVG(l.loan_loss_reserve_fee/e.rate) AS avg_llr_fee,		-- avg usd loan loss reserve fee
		MAX(l.loan_loss_reserve_fee/e.rate) AS max_llr_fee,		-- maximum usd loan loss reserve fee
		MIN(l.loan_loss_reserve_fee/e.rate) AS min_llr_fee		-- minimum usd loan loss reserve fee
		FROM loans AS l
		JOIN exchange_rates AS e
		ON l.currency_code = e.currency_code
		WHERE l.loan_loss_reserve_fee > 0 AND e.is_current = 1
		GROUP BY year, month
		
		