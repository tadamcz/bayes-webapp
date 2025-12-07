import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
import mpld3
import numpy as np
from scipy import stats

from bayes_continuous.posterior import Posterior as _Posterior
from bayes_continuous.utils import intersect_intervals, extremities_intervals


class Posterior(_Posterior):
	def graph_out(self, user_inputs):
		plt.rcParams.update({'font.size': 16})
		override_graph_range = user_inputs['override_graph_range']

		# Plot
		if override_graph_range:
			x_from, x_to = override_graph_range
		else:
			x_from, x_to = intelligently_set_graph_domain(self.prior_distribution, self.likelihood_function)

		plot = plot_pdfs_bayes_update(self.prior_distribution, self.likelihood_function, self, x_from=x_from, x_to=x_to)
		plot = mpld3.fig_to_html(plot)

		return plot

	def distribution_information_out(self, user_inputs):
		# expected value
		ev = self.expect(epsrel=1 / 100)  # epsrel is the relative tolerance passed to the integration routine
		ev_string = '<br>Expected value: ' + str(np.around(ev, 2)) + '<br>'

		# percentiles
		percentiles_exact_string = 'Percentiles:<br>'  # todo use a list instead of line breaks

		if user_inputs['custom_percentiles']:
			p = user_inputs['custom_percentiles']
		else:
			p = [0.1, 0.25, 0.5, 0.75, 0.9]
		percentiles_exact = self.compute_percentiles(p)

		for x in percentiles_exact['result']:
			percentiles_exact_string += str(x) + ', ' + str(np.around(percentiles_exact['result'][x], 2)) + '<br>'
		percentiles_exact_string += percentiles_exact['runtime']
		return ev_string + percentiles_exact_string

def plot_pdfs(dict_of_dists,x_from,x_to):
	x_from ,x_to = float(x_from),float(x_to)
	x = np.linspace(x_from,x_to,100)

	figure, axes = plt.subplots()
	for dist in dict_of_dists:
		try:
			axes.plot(x,dict_of_dists[dist].pdf(x),label=dist)
		except AttributeError:
			axes.plot(x, dict_of_dists[dist].function(x), label=dist)
	axes.legend()
	axes.set_xlabel("θ")
	axes.set_ylabel("Probability density")
	return figure

def plot_pdfs_bayes_update(prior,likelihood,posterior,x_from=-50,x_to=50):
	prior_string = "f₀(θ) = P(θ)"
	likelihood_string = "f₁(θ) = P(E|θ)"
	posterior_string = "P(θ|E)"

	plot = plot_pdfs({prior_string:prior, likelihood_string:likelihood, posterior_string:posterior},
					x_from,
					x_to)
	return plot

def intelligently_set_graph_domain(prior,likelihood):
	p = 0.1
	prior_range = prior.ppf(p), prior.ppf(1-p)

	posterior_support = intersect_intervals([prior.support(),likelihood.domain])

	domain = intersect_intervals([posterior_support,prior_range])

	buffer = 0.1
	buffer = abs(buffer*(domain[1]-domain[0]))
	domain = domain[0]-buffer,domain[1]+buffer

	return domain
