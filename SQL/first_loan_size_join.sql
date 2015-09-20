/*
Calculate the size of first time loans
*/
SELECT	EXTRACT(YEAR FROM ln.created_at) AS year,	-- year
		EXTRACT(MONTH FROM ln.created_at) AS month,	-- month
		MAX(
			CASE 	WHEN ln.registration_fee > 0 THEN ln.usd_amount
					ELSE NULL
					END
			) AS max_new_loan_size,		-- maximum new loan size per month
		COUNT(
				CASE WHEN br.activation_status != 4 THEN br.id
				ELSE NULL
				END
			) AS new_loans_per_month
		FROM loans AS ln
		INNER JOIN borrowers AS br
		ON br.id = ln.borrower_id
		GROUP BY year, month
		
		