/*
Calculate the invitation bonus
*/
SELECT	year,
		month,
		MAX(count_invites) AS max_invites
		FROM(
			SELECT	EXTRACT(YEAR FROM created_at) AS year,		-- year
					EXTRACT(MONTH FROM created_at) AS month,	-- month
					borrower_id,
					count(*) AS count_invites
					FROM borrower_invites
			--		WHERE activation_status != 4	-- status of 4 means rejected
					GROUP BY year, month, borrower_id
		) sub
		GROUP BY year, month