def f(forecast, observe_window, date, backtest: boolean, ): # score of single site on a date
	'''
	forecast: every site, every forecast
	observe_window: 
	Return: a vector of score of all sites on one date
	'''
	# class.f = computed f

def f_variance(penalty_term):
	# class.f = f*exp(penalty)



def F(baseline_matrix, weights, include_variance, variance_penalty_term): 
	'''
		Return: a list of F, each entry is the total score of sites on one date
	'''
	F_vector = []
	for day in range(10):
		F = compute f * weights
		F_vector.append(F)
	# class.F = computed F vector




def optimize(F_vector,date_range, k: number of days left, SortOrDP, discount_term):
	'''
		Input: a list of F
		Return: path and score, second best path, 
	'''

	If Sort: discount multiplier: (1+r)^D 
	If DP: penalty for each day
