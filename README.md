# SIR model based epidemiology curve generator in Matplotlib
"Who needs Geogebra(no offense), when we got python!" - Me

A simple script developed by me to simulate an epidemic using the SIR model for epidemiology.
I have optimised the script to the best of my knowledge. I have included some basic comments at important parts so as to not leave those who need it, hanging.

Note: I initially decided to leave the optimisation as is but then changed my mind. With the help of reddit users such [u/vlovero](https://www.reddit.com/user/vlovero) and [u/kokoistheway](https://www.reddit.com/user/kokoistheway) who helped me improve the code and speed up things by introducing me to [numba](http://numba.pydata.org/) (special thanks to u/vlovero for that!). Also some of you [scipy](https://docs.scipy.org/doc/scipy/reference/index.html) fans maybe wondering why I didn't use scipy's [integrate.solve\_ivp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html), well I tried that (again all thanks to u/vlovero for bringing that to my attention) but I was not satisfied with it as it generated data that caused a curve that was less smooth to be generated(Don't get me wrong but the solution was still correct as both my original solution and that of scipy's were similar), so I ended up sticking with my original solution.

Here is the original reddit thread of me asking for help on optimisation if you are interested in that... [Click here!](https://www.reddit.com/r/learnpython/comments/fropmx/very_poor_performance_in_my_matplotlib_script_at/)

Also I am leaving here both versions, my own optimised version (SIRmodel\_cl\_op.py) and that with the help I mentioned above (SIRmodel\_cl\_op\_sn.py) for those who are interested in the differences and who would love to learn from and play around with both!

This project was inspired by the Numberphile video on explaining an epidemic's mathematical
modeling. I suggest anybody who doesn't already know what this is about to check the video out!

Video link: [Click here!](https://www.youtube.com/watch?v=k6nLfCbAzgo)

So enjoy and feel free to play around with my script! Also stay safe! (For anybody from the future, this was made during the Coronavirus Pandemic)

(You looking for a license? Well there wasn't any until a Reddit user told me to put one... So here it is MIT LICENSE, Enjoy!)
