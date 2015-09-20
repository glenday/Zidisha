/*
Calculate the size of first time loans
*/
SELECT	EXTRACT(YEAR FROM created_at) AS year,		-- year
		EXTRACT(MONTH FROM created_at) AS month,	-- month
		usd_amount,			-- loan size in USD
		registration_fee,	-- month
		loan_loss_reserve_fee
--		category_id,
--		secondary_category_id
		FROM loans
		WHERE EXTRACT(YEAR FROM created_at) >= 2015 AND EXTRACT(MONTH FROM created_at) >= 1
		LIMIT 100
		
		