/*
Calculate the maximum number of invitees allowed using two month counts
*/
SELECT	year,
		bi_month,
		MAX(count_invites) AS max_invites
		FROM(
			SELECT	EXTRACT(YEAR FROM created_at) AS year,		-- year
					FLOOR(EXTRACT(MONTH FROM created_at)/2) AS bi_month,	-- month
					borrower_id,
					count(*) AS count_invites
					FROM borrower_invites
			--		WHERE activation_status != 4	-- status of 4 means rejected
					GROUP BY year, bi_month, borrower_id
		) sub
		GROUP BY year, bi_month